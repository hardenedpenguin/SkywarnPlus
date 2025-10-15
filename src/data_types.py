"""
Type definitions and data structures for SkywarnPlus.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from enum import Enum


@dataclass
class AlertData:
    """Data structure for weather alert information."""
    county_code: str
    severity: int
    description: str
    end_time_utc: str
    event: str
    headline: Optional[str] = None
    instruction: Optional[str] = None


@dataclass
class CountyConfig:
    """Configuration for a county."""
    code: str
    wav_file: Optional[str] = None


@dataclass
class AudioConfig:
    """Audio processing configuration."""
    sounds_path: str
    audio_delay: int
    alert_sound: str
    all_clear_sound: str
    alert_separator: str
    say_alert_suffix: Optional[str] = None
    say_all_clear_suffix: Optional[str] = None


@dataclass
class AsteriskConfig:
    """Asterisk integration configuration."""
    nodes: List[int]
    audio_delay: int


@dataclass
class APIConfig:
    """API configuration."""
    timeout: int
    max_workers: int
    retry_attempts: int
    backoff_factor: float


@dataclass
class AppConfig:
    """Main application configuration."""
    enabled: bool
    max_alerts: int
    time_type: str
    with_multiples: bool
    say_alert: bool
    say_all_clear: bool
    say_alerts_changed: bool
    say_alert_all: bool


class TimeType(Enum):
    """Time type enumeration."""
    ONSET = "onset"
    EFFECTIVE = "effective"


class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# Type aliases
CountyCode = str
AlertType = str
StateData = Dict[str, Any]
ConfigDict = Dict[str, Any]
