"""
Configuration controller for SkywarnPlus.
"""

import os
import logging
import subprocess
from typing import Dict, Any, Optional, List
from pathlib import Path

from .exceptions import ConfigurationError, ValidationError
from .config import ConfigManager
from .asterisk_integration import AsteriskIntegration


class ConfigController:
    """Handles configuration management and control operations."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize config controller."""
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Get configurations
        self.asterisk_config = self.config_manager.get_asterisk_config()
        self.audio_config = self.config_manager.get_audio_config()
        
        # Initialize Asterisk integration
        self.asterisk_integration = AsteriskIntegration(self.asterisk_config)
        
        self._AudioSegment = None
    
    def _lazy_import_pydub(self):
        """Lazy import pydub."""
        if self._AudioSegment is None:
            try:
                from pydub import AudioSegment
                self._AudioSegment = AudioSegment
            except ImportError:
                raise ValidationError("pydub is required for audio processing")
        return self._AudioSegment
    
    def update_config_value(self, key_path: str, value: Any) -> bool:
        """
        Update a configuration value.
        
        Args:
            key_path: Dot-separated path to the config key (e.g., "Alerting.SayAlert")
            value: New value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Split the key path
            keys = key_path.split('.')
            
            # Get the current config
            config = self.config_manager.config.copy()
            
            # Navigate to the parent of the target key
            current = config
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the value
            current[keys[-1]] = value
            
            # Save the updated config
            self._save_config(config)
            
            self.logger.info(f"Updated config: {key_path} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update config {key_path}: {e}")
            return False
    
    def get_config_value(self, key_path: str) -> Any:
        """
        Get a configuration value.
        
        Args:
            key_path: Dot-separated path to the config key
            
        Returns:
            Configuration value or None if not found
        """
        try:
            keys = key_path.split('.')
            current = self.config_manager.config
            
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return None
            
            return current
            
        except Exception as e:
            self.logger.error(f"Failed to get config {key_path}: {e}")
            return None
    
    def change_courtesy_tone(self, ct_mode: str) -> bool:
        """
        Change courtesy tone mode.
        
        Args:
            ct_mode: Courtesy tone mode (e.g., "normal", "wx")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate mode
            valid_modes = ["normal", "wx"]
            if ct_mode.lower() not in valid_modes:
                self.logger.error(f"Invalid courtesy tone mode: {ct_mode}")
                return False
            
            # Use Asterisk integration
            success = self.asterisk_integration.change_ct(ct_mode)
            
            if success:
                self.logger.info(f"Courtesy tone changed to: {ct_mode}")
            else:
                self.logger.error(f"Failed to change courtesy tone to: {ct_mode}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error changing courtesy tone: {e}")
            return False
    
    def change_node_id(self, node_id: str) -> bool:
        """
        Change node ID.
        
        Args:
            node_id: New node ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate node ID format (basic validation)
            if not node_id or len(node_id.strip()) == 0:
                self.logger.error("Node ID cannot be empty")
                return False
            
            # Use Asterisk integration
            success = self.asterisk_integration.change_id(node_id)
            
            if success:
                self.logger.info(f"Node ID changed to: {node_id}")
            else:
                self.logger.error(f"Failed to change node ID to: {node_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error changing node ID: {e}")
            return False
    
    def generate_silent_audio(self, duration_ms: int, output_file: str) -> bool:
        """
        Generate silent audio file.
        
        Args:
            duration_ms: Duration in milliseconds
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            AudioSegment = self._lazy_import_pydub()
            
            # Create silent audio
            silence = AudioSegment.silent(duration=duration_ms)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Export audio
            silence.export(output_file, format="wav")
            
            self.logger.info(f"Generated silent audio: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate silent audio: {e}")
            return False
    
    def create_tail_message(self, alerts: List[Dict[str, Any]]) -> bool:
        """
        Create a tail message audio file.
        
        Args:
            alerts: List of alert dictionaries
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not alerts:
                self.logger.info("No alerts to create tail message for")
                return True
            
            # Generate tail message content
            tail_content = self._generate_tail_content(alerts)
            
            # Create audio file path
            output_file = os.path.join("/tmp", "SkywarnPlus", "tailmessage.wav")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Generate silent audio for now (would need TTS integration for full functionality)
            success = self.generate_silent_audio(1000, output_file)
            
            if success:
                self.logger.info(f"Tail message created: {output_file}")
                self.logger.info(f"Tail content: {tail_content}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to create tail message: {e}")
            return False
    
    def _generate_tail_content(self, alerts: List[Dict[str, Any]]) -> str:
        """Generate tail message content from alerts."""
        if not alerts:
            return "No active weather alerts."
        
        alert_types = []
        for alert in alerts:
            alert_type = alert.get("type", "Unknown")
            if alert_type not in alert_types:
                alert_types.append(alert_type)
        
        return f"Active weather alerts: {', '.join(alert_types)}"
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        try:
            config_path = self.config_manager.config_path
            yaml = self.config_manager._lazy_import_yaml()
            
            with open(config_path, "w") as config_file:
                yaml.dump(config, config_file)
            
            self.logger.debug(f"Configuration saved to: {config_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            raise ConfigurationError(f"Failed to save configuration: {e}")
    
    def validate_config(self) -> bool:
        """Validate current configuration."""
        try:
            # Check required sections
            required_sections = ["SKYWARNPLUS", "Alerting"]
            for section in required_sections:
                if section not in self.config_manager.config:
                    self.logger.error(f"Missing required config section: {section}")
                    return False
            
            # Check Alerting section
            alerting = self.config_manager.config["Alerting"]
            if "CountyCodes" not in alerting:
                self.logger.error("Missing CountyCodes in Alerting section")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False
