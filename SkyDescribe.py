#!/usr/bin/python3

"""
SkyDescribe.py v0.8.0 by Mason Nelson
==================================================
Text to Speech conversion for Weather Descriptions

This script converts the descriptions of weather alerts to an audio format using 
the VoiceRSS Text-to-Speech API. It first modifies the description to replace 
abbreviations and certain symbols to make the text more suitable for audio conversion.
The script then sends this text to the VoiceRSS API to get the audio data, which 
it saves to a WAV file. Finally, it uses the Asterisk PBX system to play this audio 
file over a radio transmission system.

The script can be run from the command line with an index or a title of an alert as argument.

This file is part of SkywarnPlus.
SkywarnPlus is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version. SkywarnPlus is distributed in the hope
that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with SkywarnPlus. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import sys
import requests
import json
import urllib.parse
import subprocess
import wave
import contextlib
import re
import logging
from functools import lru_cache
from collections import OrderedDict

# Lazy imports for performance
def _lazy_import_yaml():
    """Lazy import YAML to avoid loading unless needed."""
    try:
        from ruamel.yaml import YAML
        return YAML()
    except ImportError:
        raise ImportError("ruamel.yaml is required")

# Use ruamel.yaml instead of PyYAML
YAML = _lazy_import_yaml()

# Directories and Paths
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

# Optimized configuration loading with caching
@lru_cache(maxsize=1)
def _load_config():
    """Load configuration with caching."""
    with open(CONFIG_PATH, "r") as config_file:
        return YAML.load(config_file)

# Load configuration with caching
CONFIG = _load_config()

# Define tmp_dir
TMP_DIR = CONFIG.get("DEV", []).get("TmpDir", "/tmp/SkywarnPlus")

# Define VoiceRSS settings
# get api key, fellback 150
API_KEY = CONFIG.get("SkyDescribe", []).get("APIKey", "")
LANGUAGE = CONFIG.get("SkyDescribe", []).get("Language", "en-us")
SPEED = CONFIG.get("SkyDescribe", []).get("Speed", 0)
VOICE = CONFIG.get("SkyDescribe", []).get("Voice", "John")
MAX_WORDS = CONFIG.get("SkyDescribe", []).get("MaxWords", 150)

# Path to the data file
DATA_FILE = os.path.join(TMP_DIR, "data.json")

# Define logger
LOGGER = logging.getLogger(__name__)
if CONFIG.get("Logging", []).get("Debug", False):
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)

# Define formatter
FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

# Define and attach console handler
CH = logging.StreamHandler()
CH.setLevel(logging.DEBUG)
CH.setFormatter(FORMATTER)
LOGGER.addHandler(CH)

# Define and attach file handler
LOG_PATH = os.path.join(TMP_DIR, "SkyDescribe.log")
FH = logging.FileHandler(LOG_PATH)
FH.setLevel(logging.DEBUG)
FH.setFormatter(FORMATTER)
LOGGER.addHandler(FH)

if not API_KEY:
    LOGGER.error("SkyDescribe: No VoiceRSS API key found in config.yaml")
    sys.exit(1)


def load_state():
    """
    Load the state from the state file if it exists, else return an initial state.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            state = json.load(file)
            state["alertscript_alerts"] = state.get("alertscript_alerts", [])

            # Process 'last_alerts' and maintain the order of alerts
            last_alerts = state.get("last_alerts", [])
            state["last_alerts"] = OrderedDict((x[0], x[1]) for x in last_alerts)

            state["last_sayalert"] = state.get("last_sayalert", [])
            state["active_alerts"] = state.get("active_alerts", [])
            return state
    else:
        return {
            "ct": None,
            "id": None,
            "alertscript_alerts": [],
            "last_alerts": OrderedDict(),
            "last_sayalert": [],
            "active_alerts": [],
        }


def modify_description(description):
    """
    Modify the description to make it more suitable for conversion to audio.

    Args:
        description (str): The description text.
        alert_title (str): The title of the alert.

    Returns:
        str: The modified description text.
    """
    # Remove newline characters and replace multiple spaces with a single space
    description = description.replace("\n", " ")
    description = re.sub(r"\s+", " ", description)

    # Replace some common weather abbreviations and symbols
    abbreviations = {
        r"\bmph\b": "miles per hour",
        r"\bknots\b": "nautical miles per hour",
        r"\bNm\b": "nautical miles",
        r"\bnm\b": "nautical miles",
        r"\bft\.\b": "feet",
        r"\bin\.\b": "inches",
        r"\bm\b": "meter",
        r"\bkm\b": "kilometer",
        r"\bmi\b": "mile",
        r"\b%\b": "percent",
        r"\bN\b": "north",
        r"\bS\b": "south",
        r"\bE\b": "east",
        r"\bW\b": "west",
        r"\bNE\b": "northeast",
        r"\bNW\b": "northwest",
        r"\bSE\b": "southeast",
        r"\bSW\b": "southwest",
        r"\bF\b": "Fahrenheit",
        r"\bC\b": "Celsius",
        r"\bUV\b": "ultraviolet",
        r"\bgusts up to\b": "gusts of up to",
        r"\bhrs\b": "hours",
        r"\bhr\b": "hour",
        r"\bmin\b": "minute",
        r"\bsec\b": "second",
        r"\bsq\b": "square",
        r"\bw/\b": "with",
        r"\bc/o\b": "care of",
        r"\bblw\b": "below",
        r"\babv\b": "above",
        r"\bavg\b": "average",
        r"\bfr\b": "from",
        r"\bto\b": "to",
        r"\btill\b": "until",
        r"\bb/w\b": "between",
        r"\bbtwn\b": "between",
        r"\bN/A\b": "not available",
        r"\b&\b": "and",
        r"\b\+\b": "plus",
        r"\be\.g\.\b": "for example",
        r"\bi\.e\.\b": "that is",
        r"\best\.\b": "estimated",
        r"\b\.\.\.\b": ".",
        r"\b\n\n\b": ".",
        r"\b\n\b": ".",
        r"\bEDT\b": "eastern daylight time",
        r"\bEST\b": "eastern standard time",
        r"\bCST\b": "central standard time",
        r"\bCDT\b": "central daylight time",
        r"\bMST\b": "mountain standard time",
        r"\bMDT\b": "mountain daylight time",
        r"\bPST\b": "pacific standard time",
        r"\bPDT\b": "pacific daylight time",
        r"\bAKST\b": "Alaska standard time",
        r"\bAKDT\b": "Alaska daylight time",
        r"\bHST\b": "Hawaii standard time",
        r"\bHDT\b": "Hawaii daylight time",
    }
    for abbr, full in abbreviations.items():
        description = re.sub(abbr, full, description)

    # Remove '*' characters
    description = description.replace("*", "")

    # Replace '  ' with a single space
    description = re.sub(r"\s\s+", " ", description)

    # Replace '. . . ' with a single space. The \s* takes care of any number of spaces.
    description = re.sub(r"\.\s*\.\s*\.\s*", " ", description)

    # Correctly format time mentions in 12-hour format (add colon) and avoid adding spaces in these
    description = re.sub(r"(\b\d{1,2})(\d{2}\s*[AP]M)", r"\1:\2", description)

    # Remove spaces between numbers and "pm" or "am"
    description = re.sub(r"(\d) (\s*[AP]M)", r"\1\2", description)

    # Only separate numerical sequences followed by a letter, and avoid adding spaces in multi-digit numbers
    description = re.sub(r"(\d)(?=[A-Za-z])", r"\1 ", description)

    # Replace any remaining ... with a single period
    description = re.sub(r"\.\s*", ". ", description).strip()

    # Limit the description to a maximum number of words
    words = description.split()
    LOGGER.debug("SkyDescribe: Description has %d words.", len(words))
    if len(words) > MAX_WORDS:
        description = " ".join(words[:MAX_WORDS])
        LOGGER.info("SkyDescribe: Description has been limited to %d words.", MAX_WORDS)

    return description


def convert_to_audio(api_key, text):
    """
    Convert the given text to audio using the Voice RSS Text-to-Speech API.

    Args:
        api_key (str): The API key.
        text (str): The text to convert.

    Returns:
        str: The path to the audio file.
    """
    base_url = "http://api.voicerss.org/"
    params = {
        "key": api_key,
        "hl": str(LANGUAGE),
        "src": text,
        "c": "WAV",
        "f": "8khz_16bit_mono",
        "r": str(SPEED),
        "v": str(VOICE),
    }

    LOGGER.debug(
        "SkyDescribe: Voice RSS API URL: %s",
        base_url + "?" + urllib.parse.urlencode(params),
    )

    # Use session for connection pooling
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'SkywarnPlus/0.8.0 (Weather Alert System)',
        'Accept': 'audio/wav',
        'Accept-Encoding': 'gzip, deflate'
    })
    
    response = session.get(base_url, params=params, timeout=30)
    response.raise_for_status()
    # if responce text contains "ERROR" then log it and exit
    if "ERROR" in response.text:
        LOGGER.error("SkyDescribe: %s", response.text)
        sys.exit(1)

    audio_file_path = os.path.join(TMP_DIR, "describe.wav")
    LOGGER.debug("SkyDescribe: Saving audio file to %s", audio_file_path)
    with open(audio_file_path, "wb") as file:
        file.write(response.content)
    return audio_file_path


def main(index_or_title):
    state = load_state()
    alerts = list(state["last_alerts"].items())

    # list the alerts in order as a numbered list
    LOGGER.debug("SkyDescribe: List of alerts:")
    for i, alert in enumerate(alerts):
        LOGGER.debug("SkyDescribe: %d. %s", i + 1, alert[0])

    # Determine if the argument is an index or a title
    if str(index_or_title).isdigit():
        index = int(index_or_title) - 1
        if index >= len(alerts):
            LOGGER.error("SkyDescribe: No alert found at index %d.", index + 1)
            description = "Sky Describe error, no alert found at index {}.".format(
                index + 1
            )
        else:
            alert, alert_data = alerts[index]

            # Count the unique instances of the alert
            unique_instances = len(
                set((data["description"], data["end_time_utc"]) for data in alert_data)
            )

            # Modify the description
            if unique_instances == 1:
                description = alert_data[0]["description"]
            else:
                description = "There are {} unique instances of {}. Describing the first one. {}".format(
                    unique_instances, alert, alert_data[0]["description"]
                )

    else:
        # Argument is not an index, assume it's a title
        title = index_or_title
        for alert, alert_data in alerts:
            if alert == title:  # Assuming alert is a title
                # Count the unique instances of the alert
                unique_instances = len(
                    set(
                        (data["description"], data["end_time_utc"])
                        for data in alert_data
                    )
                )

                # Modify the description
                if unique_instances == 1:
                    description = alert_data[0]["description"]
                else:
                    description = "There are {} unique instances of {}. Describing the first one. {}".format(
                        unique_instances, alert, alert_data[0]["description"]
                    )
                break
        else:
            LOGGER.error("SkyDescribe: No alert with title %s found.", title)
            description = "Sky Describe error, no alert found with title {}.".format(
                title
            )

    LOGGER.debug("\n\nSkyDescribe: Original description: %s", description)

    # If the description is not an error message, extract the alert title
    if not "Sky Describe error" in description:
        alert_title = alert  # As alert itself is the title now
        LOGGER.info("SkyDescribe: Generating description for alert: %s", alert_title)
        # Add the alert title at the beginning
        description = "Detailed alert information for {}. {}".format(
            alert_title, description
        )
        description = modify_description(description)

    LOGGER.debug("\n\nSkyDescribe: Modified description: %s\n\n", description)

    audio_file = convert_to_audio(API_KEY, description)

    with contextlib.closing(wave.open(audio_file, "r")) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    LOGGER.debug("SkyDescribe: Length of the audio file in seconds: %s", duration)

    nodes = CONFIG["Asterisk"]["Nodes"]
    for node in nodes:
        LOGGER.info("SkyDescribe: Broadcasting description on node %s.", node)
        command = "/usr/sbin/asterisk -rx 'rpt localplay {} {}'".format(
            node, audio_file.rsplit(".", 1)[0]
        )
        LOGGER.debug("SkyDescribe: Running command: %s", command)
        try:
            subprocess.run(command, shell=True, timeout=30, check=False)
        except subprocess.TimeoutExpired:
            LOGGER.error(f"Subprocess timeout for command: {command}")
        except Exception as e:
            LOGGER.error(f"Subprocess error for command {command}: {e}")


# Script entry point
if __name__ == "__main__":
    if len(sys.argv) != 2:
        LOGGER.error("Usage: SkyDescribe.py <alert index or title>")
        sys.exit(1)
    main(sys.argv[1])
