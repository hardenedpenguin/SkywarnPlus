"""
Alert processing and management functionality.
"""

import logging
import fnmatch
from typing import Dict, List, Optional, Set, Any
from datetime import datetime, timezone
from collections import OrderedDict

from .constants import API_SEVERITY_MAPPING, WORD_SEVERITY_MAPPING, ALERT_STRINGS, ALERT_INDEXES
from .exceptions import ValidationError
from .data_types import AlertData, CountyCode, AlertType, StateData


class AlertProcessor:
    """Processes and manages weather alerts."""
    
    def __init__(self):
        """Initialize alert processor."""
        self.logger = logging.getLogger(__name__)
    
    def parse_alert_data(self, api_data: Dict[str, Any], county_code: CountyCode) -> List[AlertData]:
        """Parse API response data into AlertData objects."""
        alerts = []
        
        if not api_data or 'features' not in api_data:
            return alerts
        
        try:
            for feature in api_data['features']:
                properties = feature.get('properties', {})
                
                # Extract basic alert information
                event = properties.get('event', 'Unknown Event')
                description = properties.get('description', '')
                headline = properties.get('headline', '')
                instruction = properties.get('instruction', '')
                
                # Parse end time
                end_time_str = properties.get('ends')
                if end_time_str:
                    try:
                        from dateutil import parser
                        end_time = parser.parse(end_time_str)
                        end_time_utc = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    except Exception as e:
                        self.logger.warning(f"Failed to parse end time '{end_time_str}': {e}")
                        end_time_utc = ""
                else:
                    end_time_utc = ""
                
                # Determine severity
                severity = self._determine_severity(properties)
                
                alert = AlertData(
                    county_code=county_code,
                    severity=severity,
                    description=description,
                    end_time_utc=end_time_utc,
                    event=event,
                    headline=headline,
                    instruction=instruction
                )
                
                alerts.append(alert)
        
        except Exception as e:
            self.logger.error(f"Error parsing alert data for {county_code}: {e}")
        
        return alerts
    
    def _determine_severity(self, properties: Dict[str, Any]) -> int:
        """Determine alert severity from properties."""
        # Try API severity first
        api_severity = properties.get('severity')
        if api_severity in API_SEVERITY_MAPPING:
            return API_SEVERITY_MAPPING[api_severity].value
        
        # Try word-based severity
        event = properties.get('event', '')
        for word, severity in WORD_SEVERITY_MAPPING.items():
            if word in event:
                return severity.value
        
        # Default to unknown
        return 0
    
    def filter_blocked_alerts(self, alerts: Dict[AlertType, List[AlertData]], 
                            blocked_events: List[str]) -> Dict[AlertType, List[AlertData]]:
        """Filter out blocked alerts."""
        filtered_alerts = {}
        
        for alert_type, alert_list in alerts.items():
            is_blocked = any(
                fnmatch.fnmatch(alert_type, blocked_event)
                for blocked_event in blocked_events
            )
            
            if not is_blocked:
                filtered_alerts[alert_type] = alert_list
        
        return filtered_alerts
    
    def sort_alerts_by_severity(self, alerts: Dict[AlertType, List[AlertData]]) -> OrderedDict:
        """Sort alerts by severity (highest first)."""
        # Create list of (alert_type, max_severity) tuples
        alert_severities = []
        for alert_type, alert_list in alerts.items():
            max_severity = max(alert.severity for alert in alert_list)
            alert_severities.append((alert_type, max_severity))
        
        # Sort by severity (descending)
        alert_severities.sort(key=lambda x: x[1], reverse=True)
        
        # Create ordered dictionary
        sorted_alerts = OrderedDict()
        for alert_type, _ in alert_severities:
            sorted_alerts[alert_type] = alerts[alert_type]
        
        return sorted_alerts
    
    def get_alert_index(self, alert_string: str) -> Optional[int]:
        """Get the index of an alert string."""
        try:
            return ALERT_STRINGS.index(alert_string) + 1
        except ValueError:
            return None
    
    def detect_county_changes(self, old_alerts: Dict[str, List[Dict]], 
                            new_alerts: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Detect changes in county coverage for alerts."""
        changes_detected = {}
        alerts_with_changed_counties = {}
        
        for alert_name, alert_info in new_alerts.items():
            if alert_name not in old_alerts:
                continue
            
            old_alert_info = old_alerts.get(alert_name, [])
            old_county_codes = {info["county_code"] for info in old_alert_info}
            new_county_codes = {info["county_code"] for info in alert_info}
            
            added_counties = new_county_codes - old_county_codes
            removed_counties = old_county_codes - new_county_codes
            
            # Clean county codes
            import re
            clean_pattern = re.compile(r'[{}"]')
            added_counties = {clean_pattern.sub("", code) for code in added_counties}
            removed_counties = {clean_pattern.sub("", code) for code in removed_counties}
            
            if added_counties or removed_counties:
                alerts_with_changed_counties[alert_name] = new_alerts[alert_name]
                changes_detected[alert_name] = {
                    "old": old_county_codes,
                    "added": added_counties,
                    "removed": removed_counties,
                }
        
        return {
            "changes_detected": changes_detected,
            "alerts_with_changed_counties": alerts_with_changed_counties
        }
    
    def time_until(self, start_time_utc: str, current_time: Optional[datetime] = None) -> int:
        """Calculate minutes until start time."""
        if current_time is None:
            current_time = datetime.now(timezone.utc)
        
        try:
            from dateutil import parser
            start_time = parser.parse(start_time_utc)
            
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
            
            time_diff = start_time - current_time
            return int(time_diff.total_seconds() / 60)
        except Exception as e:
            self.logger.error(f"Error calculating time until {start_time_utc}: {e}")
            return 0
