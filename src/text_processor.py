"""
Text processing utilities for SkywarnPlus.
"""

import re
import logging
from typing import Dict, List, Any, Optional
from collections import OrderedDict

from .exceptions import ValidationError
from .data_types import AlertData


class TextProcessor:
    """Handles text processing and formatting operations."""
    
    def __init__(self):
        """Initialize text processor."""
        self.logger = logging.getLogger(__name__)
    
    def clean_alert_text(self, text: str) -> str:
        """
        Clean and normalize alert text for better readability.
        
        Args:
            text: Raw alert text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove HTML tags if present
        text = re.sub(r'<[^>]+>', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Clean up punctuation
        text = re.sub(r'\.+', '.', text)
        text = re.sub(r'\?+', '?', text)
        text = re.sub(r'!+', '!', text)
        
        return text.strip()
    
    def extract_key_info(self, alert_data: AlertData) -> Dict[str, str]:
        """
        Extract key information from alert data for text processing.
        
        Args:
            alert_data: Alert data object
            
        Returns:
            Dictionary with extracted information
        """
        info = {
            "event": alert_data.event,
            "description": self.clean_alert_text(alert_data.description),
            "headline": self.clean_alert_text(alert_data.headline or ""),
            "instruction": self.clean_alert_text(alert_data.instruction or ""),
            "county_code": alert_data.county_code,
            "severity": str(alert_data.severity),
            "end_time": alert_data.end_time_utc
        }
        
        return info
    
    def format_alert_summary(self, alerts: Dict[str, List[AlertData]], 
                           county_data: Dict[str, str]) -> str:
        """
        Format alert summary for display or TTS.
        
        Args:
            alerts: Dictionary of alert types and their data
            county_data: County code to name mapping
            
        Returns:
            Formatted alert summary
        """
        if not alerts:
            return "No active weather alerts."
        
        summary_parts = []
        
        for alert_type, alert_list in alerts.items():
            counties = []
            for alert in alert_list:
                county_name = county_data.get(alert.county_code, alert.county_code)
                if county_name not in counties:
                    counties.append(county_name)
            
            county_str = ", ".join(sorted(counties))
            summary_parts.append(f"{alert_type} for {county_str}")
        
        return ". ".join(summary_parts) + "."
    
    def generate_title_string(self, alerts: Dict[str, List[AlertData]], 
                            county_data: Dict[str, str]) -> List[str]:
        """
        Generate title strings for alerts with county information.
        
        Args:
            alerts: Dictionary of alert types and their data
            county_data: County code to name mapping
            
        Returns:
            List of formatted title strings
        """
        alert_titles_with_counties = []
        
        for alert_type, alert_list in alerts.items():
            counties = []
            for alert in alert_list:
                county_name = county_data.get(alert.county_code, alert.county_code)
                if county_name not in counties:
                    counties.append(county_name)
            
            counties_str = ", ".join(sorted(counties))
            title = f"{alert_type} [{counties_str}]"
            alert_titles_with_counties.append(title)
        
        self.logger.info(f"Generated titles: {alert_titles_with_counties}")
        return alert_titles_with_counties
    
    def truncate_text(self, text: str, max_length: int = 1000) -> str:
        """
        Truncate text to specified length while preserving word boundaries.
        
        Args:
            text: Text to truncate
            max_length: Maximum length in characters
            
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        
        # Find the last space before the limit
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # If we can find a good break point
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    def sanitize_for_filename(self, text: str) -> str:
        """
        Sanitize text for use in filenames.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text safe for filenames
        """
        # Remove or replace invalid filename characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', text)
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = re.sub(r'_+', '_', sanitized)
        sanitized = sanitized.strip('_')
        
        # Limit length
        if len(sanitized) > 100:
            sanitized = sanitized[:100].rstrip('_')
        
        return sanitized
    
    def extract_time_info(self, time_str: str) -> Dict[str, Any]:
        """
        Extract time information from time string.
        
        Args:
            time_str: Time string in various formats
            
        Returns:
            Dictionary with time information
        """
        try:
            from dateutil import parser
            dt = parser.parse(time_str)
            
            return {
                "datetime": dt,
                "formatted": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "timezone": str(dt.tzinfo) if dt.tzinfo else "UTC",
                "is_valid": True
            }
        except Exception as e:
            self.logger.warning(f"Failed to parse time string '{time_str}': {e}")
            return {
                "datetime": None,
                "formatted": time_str,
                "timezone": "Unknown",
                "is_valid": False
            }
