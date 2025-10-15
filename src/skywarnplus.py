"""
Main SkywarnPlus application class.
"""

import os
import logging
import threading
from typing import Dict, List, Optional
from pathlib import Path

from .config import ConfigManager
from .api_client import NWSAPIClient
from .audio_processor import AudioProcessor
from .alert_processor import AlertProcessor
from .state_manager import StateManager
from .alert_announcer import AlertAnnouncer
from .notification_service import NotificationService
from .exceptions import ConfigurationError, APIError


class SkywarnPlus:
    """Main SkywarnPlus application class."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize SkywarnPlus application."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.config_manager = ConfigManager(config_path)
        self.state_manager = StateManager()
        self.api_client = NWSAPIClient()
        self.alert_processor = AlertProcessor()
        
        # Load configurations
        self.app_config = self.config_manager.get_app_config()
        self.audio_config = self.config_manager.get_audio_config()
        self.asterisk_config = self.config_manager.get_asterisk_config()
        self.county_configs = self.config_manager.get_county_configs()
        
        # Initialize processors
        self.audio_processor = AudioProcessor(self.audio_config)
        self.alert_announcer = AlertAnnouncer(
            self.audio_config, 
            self.asterisk_config, 
            self.county_configs
        )
        
        # Initialize notification service
        self.notification_service = NotificationService(self.config_manager.config)
        
        # Initialize state
        self.state = self.state_manager.load_state()
        
        self.logger.info("SkywarnPlus initialized successfully")
    
    def run(self) -> None:
        """Run the main application loop."""
        if not self.app_config.enabled:
            self.logger.info("SkywarnPlus is disabled in configuration")
            return
        
        try:
            # Get county configurations
            if not self.county_configs:
                self.logger.warning("No county codes configured")
                return
            
            county_codes = [config.code for config in self.county_configs]
            
            # Fetch alerts
            self.logger.info(f"Fetching alerts for counties: {county_codes}")
            alerts_data = self.api_client.fetch_alerts_for_counties(county_codes)
            
            # Process alerts
            all_alerts = {}
            for county_code, data in alerts_data.items():
                if data:
                    alerts = self.alert_processor.parse_alert_data(data, county_code)
                    for alert in alerts:
                        if alert.event not in all_alerts:
                            all_alerts[alert.event] = []
                        all_alerts[alert.event].append(alert)
            
            # Filter blocked alerts
            blocked_events = self.config_manager.get_blocked_events("Global")
            filtered_alerts = self.alert_processor.filter_blocked_alerts(all_alerts, blocked_events)
            
            # Sort by severity
            sorted_alerts = self.alert_processor.sort_alerts_by_severity(filtered_alerts)
            
            # Check for changes
            old_alerts = self.state.get("last_alerts", {})
            changes = self.alert_processor.detect_county_changes(old_alerts, sorted_alerts)
            
            # Handle alerts
            if sorted_alerts:
                self._handle_active_alerts(sorted_alerts, changes)
            else:
                self._handle_all_clear(old_alerts)
            
            # Update state
            self.state["last_alerts"] = sorted_alerts
            self.state_manager.save_state(self.state)
            
            self.logger.info(f"Processed {len(sorted_alerts)} alert types")
            
        except Exception as e:
            self.logger.error(f"Error in main application loop: {e}")
            raise
        finally:
            # Cleanup
            self.cleanup()
    
    def _handle_active_alerts(self, alerts: Dict, changes: Dict) -> None:
        """Handle active weather alerts."""
        try:
            # Say alerts if enabled
            if self.app_config.say_alert:
                if changes.get("changes_detected") or not self.state.get("last_sayalert"):
                    self.logger.info("Announcing new/changed alerts")
                    self.alert_announcer.say_alerts(alerts, self.app_config.max_alerts)
                    self.state["last_sayalert"] = alerts
            
            # Send notifications
            for alert_type, alert_list in alerts.items():
                counties = [alert.county_code for alert in alert_list]
                severity = max(alert.severity for alert in alert_list)
                self.notification_service.send_alert_notification(alert_type, counties, severity)
            
        except Exception as e:
            self.logger.error(f"Error handling active alerts: {e}")
    
    def _handle_all_clear(self, old_alerts: Dict) -> None:
        """Handle all clear situation."""
        try:
            if old_alerts and self.app_config.say_all_clear:
                self.logger.info("Announcing all clear")
                self.alert_announcer.say_all_clear()
                
                # Send all clear notification
                counties = []
                for alert_list in old_alerts.values():
                    counties.extend([alert["county_code"] for alert in alert_list])
                self.notification_service.send_all_clear_notification(counties)
                
                self.state["last_allclear"] = {}
                
        except Exception as e:
            self.logger.error(f"Error handling all clear: {e}")
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        try:
            # Flush state to disk
            self.state_manager.flush_state()
            
            # Cleanup audio cache
            self.audio_processor.cleanup_cache()
            
            # Close API client
            self.api_client.close()
            
            self.logger.debug("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
