"""
Configuration management for SkywarnPlus.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from functools import lru_cache

from .exceptions import ConfigurationError
from .data_types import CountyConfig, AudioConfig, AsteriskConfig, APIConfig, AppConfig


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "config.yaml"
        )
        self._config: Optional[Dict[str, Any]] = None
    
    @lru_cache(maxsize=1)
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file with caching."""
        try:
            from ruamel.yaml import YAML
            
            yaml = YAML()
            with open(self.config_path, "r") as config_file:
                config = yaml.load(config_file)
                # Convert to normal dictionary for JSON serialization
                return json.loads(json.dumps(config))
        except ImportError:
            raise ConfigurationError("ruamel.yaml is required for configuration loading")
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {self.config_path}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {e}")
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get configuration dictionary."""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def get_county_configs(self) -> List[CountyConfig]:
        """Get county configurations."""
        county_codes = self.config.get("Alerting", {}).get("CountyCodes", [])
        configs = []
        
        for item in county_codes:
            if isinstance(item, dict):
                for code, wav_file in item.items():
                    configs.append(CountyConfig(code=code, wav_file=wav_file))
            else:
                configs.append(CountyConfig(code=item))
        
        return configs
    
    def get_audio_config(self) -> AudioConfig:
        """Get audio configuration."""
        alerting = self.config.get("Alerting", {})
        
        return AudioConfig(
            sounds_path=alerting.get("SoundsPath", "SOUNDS"),
            audio_delay=self.config.get("Asterisk", {}).get("AudioDelay", 0),
            alert_sound=alerting.get("AlertSound", "Duncecap.wav"),
            all_clear_sound=alerting.get("AllClearSound", "Triangles.wav"),
            alert_separator=alerting.get("AlertSeperator", "Woodblock.wav"),
            say_alert_suffix=alerting.get("SayAlertSuffix"),
            say_all_clear_suffix=alerting.get("SayAllClearSuffix")
        )
    
    def get_asterisk_config(self) -> AsteriskConfig:
        """Get Asterisk configuration."""
        asterisk = self.config.get("Asterisk", {})
        
        return AsteriskConfig(
            nodes=asterisk.get("Nodes", []),
            audio_delay=asterisk.get("AudioDelay", 0)
        )
    
    def get_api_config(self) -> APIConfig:
        """Get API configuration."""
        return APIConfig(
            timeout=10,
            max_workers=10,
            retry_attempts=3,
            backoff_factor=1.0
        )
    
    def get_app_config(self) -> AppConfig:
        """Get main application configuration."""
        app = self.config.get("SKYWARNPLUS", {})
        alerting = self.config.get("Alerting", {})
        
        return AppConfig(
            enabled=app.get("Enable", True),
            max_alerts=alerting.get("MaxAlerts", 99),
            time_type=alerting.get("TimeType", "onset"),
            with_multiples=alerting.get("WithMultiples", True),
            say_alert=alerting.get("SayAlert", True),
            say_all_clear=alerting.get("SayAllClear", True),
            say_alerts_changed=alerting.get("SayAlertsChanged", True),
            say_alert_all=alerting.get("SayAlertAll", False)
        )
    
    def get_blocked_events(self, event_type: str) -> List[str]:
        """Get blocked events for a specific type."""
        return self.config.get("BlockedEvents", {}).get(event_type, [])
    
    def get_pushover_config(self) -> Optional[Dict[str, Any]]:
        """Get Pushover configuration."""
        return self.config.get("Pushover")
    
    def get_tts_config(self) -> Optional[Dict[str, Any]]:
        """Get TTS configuration."""
        return self.config.get("TTS")
    
    def get_sky_control_config(self) -> Optional[Dict[str, Any]]:
        """Get SkyControl configuration."""
        return self.config.get("SkyControl")


# Global configuration instance
config_manager = ConfigManager()
