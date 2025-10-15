"""
Notification services for SkywarnPlus.
"""

import logging
import requests
from typing import Dict, Any, Optional

from .exceptions import NetworkError, ValidationError


class PushoverService:
    """Pushover notification service."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Pushover service."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://api.pushover.net/1/messages.json"
    
    def send_notification(self, message: str, title: Optional[str] = None, 
                         priority: int = 0) -> bool:
        """Send Pushover notification."""
        if not self.config:
            self.logger.warning("Pushover not configured")
            return False
        
        try:
            data = {
                "token": self.config.get("token"),
                "user": self.config.get("user"),
                "message": message,
                "priority": priority
            }
            
            if title:
                data["title"] = title
            
            response = requests.post(
                self.base_url,
                data=data,
                timeout=30
            )
            
            response.raise_for_status()
            
            result = response.json()
            if result.get("status") == 1:
                self.logger.debug("Pushover notification sent successfully")
                return True
            else:
                self.logger.error(f"Pushover API error: {result.get('errors', 'Unknown error')}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Pushover request failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Pushover notification error: {e}")
            return False


class NotificationService:
    """Main notification service coordinator."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize notification service."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize available services
        self.pushover = None
        if config.get("Pushover"):
            self.pushover = PushoverService(config["Pushover"])
    
    def send_alert_notification(self, alert_type: str, counties: list, 
                               severity: int) -> bool:
        """Send alert notification through available services."""
        message = f"Weather Alert: {alert_type}"
        if counties:
            message += f" for {', '.join(counties)}"
        
        title = f"Weather Alert - Severity {severity}"
        
        success = True
        
        if self.pushover:
            if not self.pushover.send_notification(message, title, priority=severity):
                success = False
        
        return success
    
    def send_all_clear_notification(self, counties: list) -> bool:
        """Send all clear notification."""
        message = f"All Clear - Weather alerts cleared"
        if counties:
            message += f" for {', '.join(counties)}"
        
        title = "Weather Alert - All Clear"
        
        success = True
        
        if self.pushover:
            if not self.pushover.send_notification(message, title, priority=0):
                success = False
        
        return success
