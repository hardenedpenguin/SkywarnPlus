"""
Constants and configuration values for SkywarnPlus.
"""

from enum import Enum
from typing import Dict, List

# API Configuration
NWS_API_BASE_URL = "https://api.weather.gov"
NWS_ALERTS_ENDPOINT = "/alerts/active"

# HTTP Configuration
DEFAULT_TIMEOUT = 10
MAX_WORKERS = 10
RETRY_ATTEMPTS = 3
BACKOFF_FACTOR = 1

# Audio Configuration
DEFAULT_AUDIO_DELAY = 0
DEFAULT_SILENCE_DURATION = 600
DEFAULT_WORD_SPACE = 400

# File Configuration
DEFAULT_TMP_DIR = "/tmp/SkywarnPlus"
DEFAULT_SOUNDS_PATH = "SOUNDS"
DEFAULT_CONFIG_FILE = "config.yaml"
DEFAULT_DATA_FILE = "data.json"

# Alert Severity Mapping
class AlertSeverity(Enum):
    """Alert severity levels."""
    UNKNOWN = 0
    MINOR = 1
    MODERATE = 2
    SEVERE = 3
    EXTREME = 4

# API Severity Mapping
API_SEVERITY_MAPPING = {
    "Extreme": AlertSeverity.EXTREME,
    "Severe": AlertSeverity.SEVERE,
    "Moderate": AlertSeverity.MODERATE,
    "Minor": AlertSeverity.MINOR,
    "Unknown": AlertSeverity.UNKNOWN,
}

# Word-based Severity Mapping
WORD_SEVERITY_MAPPING = {
    "Warning": AlertSeverity.EXTREME,
    "Watch": AlertSeverity.SEVERE,
    "Advisory": AlertSeverity.MODERATE,
    "Statement": AlertSeverity.MINOR,
}

# Default HTTP Headers
DEFAULT_HEADERS = {
    'User-Agent': 'SkywarnPlus/0.8.0 (Weather Alert System) - Contact: mason@example.com',
    'Accept': 'application/geo+json, application/json',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US, en;q=0.9'
}

# Alert Types
ALERT_STRINGS = [
    "Flash Flood Warning", "Flash Flood Watch", "Flood Warning", "Flood Watch",
    "Severe Thunderstorm Warning", "Severe Thunderstorm Watch",
    "Tornado Warning", "Tornado Watch",
    "Winter Storm Warning", "Winter Storm Watch",
    "Blizzard Warning", "Ice Storm Warning",
    "Wind Chill Warning", "Wind Chill Advisory",
    "Heat Warning", "Heat Advisory",
    "Dense Fog Advisory", "Freezing Rain Advisory",
    "Frost Advisory", "Freeze Warning",
    "Hurricane Warning", "Hurricane Watch",
    "Tropical Storm Warning", "Tropical Storm Watch",
    "High Wind Warning", "Wind Advisory",
    "Dust Storm Warning", "Blowing Dust Advisory",
    "Fire Weather Warning", "Red Flag Warning",
    "Avalanche Warning", "Avalanche Watch",
    "Tsunami Warning", "Tsunami Watch",
    "Coastal Flood Warning", "Coastal Flood Watch",
    "Lakeshore Flood Warning", "Lakeshore Flood Watch",
    "Rip Current Statement", "High Surf Warning",
    "High Surf Advisory", "Beach Hazards Statement",
    "Small Craft Advisory", "Gale Warning",
    "Storm Warning", "Hurricane Force Wind Warning",
    "Dense Smoke Advisory", "Air Quality Alert",
    "Ashfall Warning", "Volcanic Ash Advisory",
    "Freezing Spray Warning", "Freezing Spray Advisory",
    "Hard Freeze Warning", "Hard Freeze Watch",
    "Frost Advisory", "Freeze Watch",
    "Excessive Heat Warning", "Excessive Heat Watch",
    "Heat Advisory", "Wind Chill Warning",
    "Wind Chill Watch", "Wind Chill Advisory",
    "Lake Effect Snow Warning", "Lake Effect Snow Watch",
    "Lake Effect Snow Advisory", "Winter Weather Advisory",
    "Snow Squall Warning", "Blowing Snow Advisory",
    "Blizzard Warning", "Winter Storm Warning",
    "Winter Storm Watch", "Ice Storm Warning",
    "Freezing Rain Advisory", "Freezing Drizzle Advisory",
    "Sleet Advisory", "Heavy Sleet Warning",
    "Heavy Sleet Watch", "Heavy Sleet Advisory",
    "Heavy Snow Warning", "Heavy Snow Watch",
    "Heavy Snow Advisory", "Snow Advisory",
    "Heavy Freezing Spray Warning", "Heavy Freezing Spray Watch",
    "Heavy Freezing Spray Advisory", "Freezing Spray Warning",
    "Freezing Spray Watch", "Freezing Spray Advisory",
    "Heavy Freezing Rain Warning", "Heavy Freezing Rain Watch",
    "Heavy Freezing Rain Advisory", "Freezing Rain Warning",
    "Freezing Rain Watch", "Freezing Rain Advisory",
    "Heavy Freezing Drizzle Warning", "Heavy Freezing Drizzle Watch",
    "Heavy Freezing Drizzle Advisory", "Freezing Drizzle Warning",
    "Freezing Drizzle Watch", "Freezing Drizzle Advisory",
    "Heavy Sleet Warning", "Heavy Sleet Watch",
    "Heavy Sleet Advisory", "Sleet Warning",
    "Sleet Watch", "Sleet Advisory",
    "Heavy Snow Warning", "Heavy Snow Watch",
    "Heavy Snow Advisory", "Snow Warning",
    "Snow Watch", "Snow Advisory",
    "Heavy Freezing Spray Warning", "Heavy Freezing Spray Watch",
    "Heavy Freezing Spray Advisory", "Freezing Spray Warning",
    "Freezing Spray Watch", "Freezing Spray Advisory",
    "Heavy Freezing Rain Warning", "Heavy Freezing Rain Watch",
    "Heavy Freezing Rain Advisory", "Freezing Rain Warning",
    "Freezing Rain Watch", "Freezing Rain Advisory",
    "Heavy Freezing Drizzle Warning", "Heavy Freezing Drizzle Watch",
    "Heavy Freezing Drizzle Advisory", "Freezing Drizzle Warning",
    "Freezing Drizzle Watch", "Freezing Drizzle Advisory",
    "Heavy Sleet Warning", "Heavy Sleet Watch",
    "Heavy Sleet Advisory", "Sleet Warning",
    "Sleet Watch", "Sleet Advisory",
    "Heavy Snow Warning", "Heavy Snow Watch",
    "Heavy Snow Advisory", "Snow Warning",
    "Snow Watch", "Snow Advisory"
]

# Alert Indexes (corresponding to ALERT_STRINGS)
ALERT_INDEXES = list(range(1, len(ALERT_STRINGS) + 1))
