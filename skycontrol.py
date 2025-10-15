#!/usr/bin/env python3
"""
SkyControl - Configuration control script for SkywarnPlus
Modernized version using the new modular architecture.
"""

import sys
import os
import logging
import argparse
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.config import ConfigManager
from src.config_controller import ConfigController
from src.exceptions import SkywarnPlusError


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('skycontrol.log')
        ]
    )


class SkyControlApp:
    """Main SkyControl application class."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize SkyControl application."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.config_manager = ConfigManager(config_path)
        self.config_controller = ConfigController(self.config_manager)
        
        self.logger.info("SkyControl initialized successfully")
    
    def set_config_value(self, key: str, value: str) -> bool:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key (case-insensitive)
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert value to appropriate type
            converted_value = self._convert_value(value)
            
            # Map common keys to their full paths
            key_mapping = {
                'sayalert': 'Alerting.SayAlert',
                'sayallclear': 'Alerting.SayAllClear',
                'sayalertschanged': 'Alerting.SayAlertsChanged',
                'sayalertall': 'Alerting.SayAlertAll',
                'withmultiples': 'Alerting.WithMultiples',
                'maxalerts': 'Alerting.MaxAlerts',
                'timetype': 'Alerting.TimeType',
                'alertsound': 'Alerting.AlertSound',
                'allclearsound': 'Alerting.AllClearSound',
                'alertseparator': 'Alerting.AlertSeperator',
                'enabled': 'SKYWARNPLUS.Enable',
                'enable': 'SKYWARNPLUS.Enable',
                'audiodelay': 'Asterisk.AudioDelay'
            }
            
            # Get the full key path
            full_key = key_mapping.get(key.lower(), key)
            
            # Update the configuration
            success = self.config_controller.update_config_value(full_key, converted_value)
            
            if success:
                self.logger.info(f"Configuration updated: {key} = {value}")
                return True
            else:
                self.logger.error(f"Failed to update configuration: {key}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting config value: {e}")
            return False
    
    def get_config_value(self, key: str) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (case-insensitive)
            
        Returns:
            Configuration value or None if not found
        """
        try:
            # Map common keys to their full paths
            key_mapping = {
                'sayalert': 'Alerting.SayAlert',
                'sayallclear': 'Alerting.SayAllClear',
                'sayalertschanged': 'Alerting.SayAlertsChanged',
                'sayalertall': 'Alerting.SayAlertAll',
                'withmultiples': 'Alerting.WithMultiples',
                'maxalerts': 'Alerting.MaxAlerts',
                'timetype': 'Alerting.TimeType',
                'alertsound': 'Alerting.AlertSound',
                'allclearsound': 'Alerting.AllClearSound',
                'alertseparator': 'Alerting.AlertSeperator',
                'enabled': 'SKYWARNPLUS.Enable',
                'enable': 'SKYWARNPLUS.Enable',
                'audiodelay': 'Asterisk.AudioDelay'
            }
            
            # Get the full key path
            full_key = key_mapping.get(key.lower(), key)
            
            value = self.config_controller.get_config_value(full_key)
            
            if value is not None:
                self.logger.info(f"Configuration value: {key} = {value}")
                return value
            else:
                self.logger.warning(f"Configuration key not found: {key}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting config value: {e}")
            return None
    
    def change_courtesy_tone(self, mode: str) -> bool:
        """
        Change courtesy tone mode.
        
        Args:
            mode: Courtesy tone mode (normal/wx)
            
        Returns:
            True if successful, False otherwise
        """
        return self.config_controller.change_courtesy_tone(mode)
    
    def change_node_id(self, node_id: str) -> bool:
        """
        Change node ID.
        
        Args:
            node_id: New node ID
            
        Returns:
            True if successful, False otherwise
        """
        return self.config_controller.change_node_id(node_id)
    
    def _convert_value(self, value: str) -> Any:
        """
        Convert string value to appropriate type.
        
        Args:
            value: String value to convert
            
        Returns:
            Converted value
        """
        # Boolean conversion
        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        
        # Integer conversion
        try:
            return int(value)
        except ValueError:
            pass
        
        # Float conversion
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def list_available_keys(self) -> None:
        """List available configuration keys."""
        keys = [
            'enabled', 'sayalert', 'sayallclear', 'sayalertschanged',
            'sayalertall', 'withmultiples', 'maxalerts', 'timetype',
            'alertsound', 'allclearsound', 'alertseparator', 'audiodelay'
        ]
        
        print("Available configuration keys:")
        for key in keys:
            current_value = self.get_config_value(key)
            print(f"  {key}: {current_value}")
    
    def run(self, command: str, args: List[str]) -> bool:
        """
        Run SkyControl command.
        
        Args:
            command: Command to execute
            args: Command arguments
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if command.lower() == 'set':
                if len(args) < 2:
                    self.logger.error("Usage: set <key> <value>")
                    return False
                
                key, value = args[0], args[1]
                return self.set_config_value(key, value)
            
            elif command.lower() == 'get':
                if len(args) < 1:
                    self.logger.error("Usage: get <key>")
                    return False
                
                key = args[0]
                return self.get_config_value(key) is not None
            
            elif command.lower() == 'list':
                self.list_available_keys()
                return True
            
            elif command.lower() == 'ct':
                if len(args) < 1:
                    self.logger.error("Usage: ct <mode>")
                    return False
                
                mode = args[0]
                return self.change_courtesy_tone(mode)
            
            elif command.lower() == 'id':
                if len(args) < 1:
                    self.logger.error("Usage: id <node_id>")
                    return False
                
                node_id = args[0]
                return self.change_node_id(node_id)
            
            else:
                self.logger.error(f"Unknown command: {command}")
                self.logger.info("Available commands: set, get, list, ct, id")
                return False
                
        except Exception as e:
            self.logger.error(f"Error running command: {e}")
            return False


def main():
    """Main entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="SkyControl - Configuration control for SkywarnPlus")
    parser.add_argument("command", help="Command to execute (set, get, list, ct, id)")
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--config", help="Path to config file")
    
    args = parser.parse_args()
    
    try:
        with SkyControlApp(args.config) as app:
            success = app.run(args.command, args.args)
            sys.exit(0 if success else 1)
            
    except SkywarnPlusError as e:
        logger.error(f"SkyControl error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
