#!/usr/bin/python3

"""
SkyControl.py v0.8.0 by Mason Nelson
==================================
A Control Script for SkywarnPlus

This script allows you to change the value of specific keys in the SkywarnPlus config.yaml file.
It's designed to enable or disable certain features of SkywarnPlus from the command line.
It is case-insensitive, accepting both upper and lower case parameters.

Usage: SkyControl.py <key> <value>
Example: SkyControl.py sayalert false
This will set 'SayAlert' to 'False' in the config.yaml file.

This file is part of SkywarnPlus.
SkywarnPlus is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version. SkywarnPlus is distributed in the hope
that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with SkywarnPlus. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import shutil
import sys
import subprocess
from pathlib import Path
from functools import lru_cache

# Lazy imports for performance
def _lazy_import_pydub():
    """Lazy import pydub to avoid loading unless needed."""
    try:
        from pydub import AudioSegment
        return AudioSegment
    except ImportError:
        raise ImportError("pydub is required for audio processing")

def _lazy_import_yaml():
    """Lazy import YAML to avoid loading unless needed."""
    try:
        from ruamel.yaml import YAML
        return YAML()
    except ImportError:
        raise ImportError("ruamel.yaml is required")

# Use ruamel.yaml instead of PyYAML to preserve comments in the config file
yaml = _lazy_import_yaml()

# Optimized configuration loading with caching
@lru_cache(maxsize=1)
def _load_config():
    """Load configuration with caching."""
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yaml")
    with open(config_path, "r") as config_file:
        return yaml.load(config_file)


def changeCT(ct_mode):
    """
    Changes all courtesy tones to the specified mode ('normal' or 'wx').
    This function ensures that the case of the keys in the config.yaml is correctly handled,
    dynamically selecting and applying tone configurations based on the mode.

    :param ct_mode: The operational mode to switch to ('normal' or 'wx').
    """
    ct_mode_lower = ct_mode.lower()  # Convert the mode to lowercase for comparison
    if ct_mode_lower not in ["normal", "wx"]:
        print("Invalid CT mode. Please provide either 'wx' or 'normal'.")
        sys.exit(1)

    mode_key = (
        "Normal" if ct_mode_lower == "normal" else "WX"
    )  # Convert to the case used in config.yaml

    tone_dir = config["CourtesyTones"].get(
        "ToneDir", "/usr/local/bin/SkywarnPlus/SOUNDS/TONES"
    )
    tones_config = config["CourtesyTones"]["Tones"]
    changes_made = False

    for ct_key, settings in tones_config.items():
        # Normalize the ct_key to lowercase to ensure consistent access
        target_tone = settings.get(
            mode_key
        )  # Access settings using the corrected mode key
        if not target_tone:
            print("No tone configured for {} mode in {}".format(ct_mode_lower, ct_key))
            continue

        src_file = os.path.join(tone_dir, target_tone)
        dest_file = os.path.join(tone_dir, "{}.ulaw".format(ct_key))

        # Check if the source file exists and perform the file copy operation
        if os.path.exists(src_file):
            shutil.copyfile(src_file, dest_file)
            print(
                "Updated {} to {} mode with tone {}".format(
                    ct_key, ct_mode, target_tone
                )
            )
            changes_made = True
        else:
            print("Source tone file does not exist: {}".format(src_file))

    if changes_made:
        print("All courtesy tones updated to {} mode.".format(ct_mode_lower))
    else:
        print("No changes made to courtesy tones.")

    return changes_made


def changeID(id):
    id_dir = config["IDChange"].get("IDDir", os.path.join(str(SCRIPT_DIR), "ID"))
    normal_id = config["IDChange"]["IDs"]["NormalID"]
    wx_id = config["IDChange"]["IDs"]["WXID"]
    rpt_id = config["IDChange"]["IDs"]["RptID"]

    if id == "normal":
        src_file = os.path.join(id_dir, normal_id)
        dest_file = os.path.join(id_dir, rpt_id)
        shutil.copyfile(src_file, dest_file)
        return True  # Indicate that ID was changed to normal
    elif id == "wx":
        src_file = os.path.join(id_dir, wx_id)
        dest_file = os.path.join(id_dir, rpt_id)
        shutil.copyfile(src_file, dest_file)
        return False  # Indicate that ID was changed to wx
    else:
        print("Invalid ID value. Please provide either 'wx' or 'normal'.")
        sys.exit(1)


def silent_tailmessage():
    """
    Generates a 100ms silent audio file and replaces the existing tailmessage file,
    ensuring the audio is compatible with Asterisk (8000Hz, mono).
    """
    tailmessage_path = config["Tailmessage"].get(
        "TailmessagePath", "/tmp/SkywarnPlus/wx-tail.wav"
    )
    silence = AudioSegment.silent(duration=100)
    converted_silence = silence.set_frame_rate(8000).set_channels(1)
    converted_silence.export(tailmessage_path, format="wav")
    print("Replaced tailmessage with 100ms of silence.")


# Define valid keys and corresponding audio files
VALID_KEYS = {
    "enable": {
        "key": "Enable",
        "section": "SKYWARNPLUS",
        "true_file": "SWP_137.wav",
        "false_file": "SWP_138.wav",
    },
    "sayalert": {
        "key": "SayAlert",
        "section": "Alerting",
        "true_file": "SWP_139.wav",
        "false_file": "SWP_140.wav",
    },
    "sayallclear": {
        "key": "SayAllClear",
        "section": "Alerting",
        "true_file": "SWP_141.wav",
        "false_file": "SWP_142.wav",
    },
    "tailmessage": {
        "key": "Enable",
        "section": "Tailmessage",
        "true_file": "SWP_143.wav",
        "false_file": "SWP_144.wav",
    },
    "courtesytone": {
        "key": "Enable",
        "section": "CourtesyTones",
        "true_file": "SWP_145.wav",
        "false_file": "SWP_146.wav",
    },
    "idchange": {
        "key": "Enable",
        "section": "IDChange",
        "true_file": "SWP_135.wav",
        "false_file": "SWP_136.wav",
    },
    "alertscript": {
        "key": "Enable",
        "section": "AlertScript",
        "true_file": "SWP_133.wav",
        "false_file": "SWP_134.wav",
    },
    "changect": {
        "key": "",
        "section": "",
        "true_file": "SWP_131.wav",
        "false_file": "SWP_132.wav",
        "available_values": ["wx", "normal"],
    },
    "changeid": {
        "key": "",
        "section": "",
        "true_file": "SWP_129.wav",
        "false_file": "SWP_130.wav",
        "available_values": ["wx", "normal"],
    },
}

# Get the directory of the script
SCRIPT_DIR = Path(__file__).parent.absolute()

# Get the configuration file
CONFIG_FILE = SCRIPT_DIR / "config.yaml"

# Check if the correct number of arguments are passed
if len(sys.argv) != 3:
    print("Incorrect number of arguments. Please provide the key and the new value.")
    print("Usage: python3 {} <key> <value>".format(sys.argv[0]))
    sys.exit(1)

# The input key and value
key, value = sys.argv[1:3]

# Convert to lower case
key = key.lower()
value = value.lower()

# Make sure the provided key is valid
if key not in VALID_KEYS:
    print("The provided key does not match any configurable item.")
    sys.exit(1)

# Validate the provided value
if key in ["changect", "changeid"]:
    if value not in VALID_KEYS[key]["available_values"]:
        print(
            "Invalid value for {}. Please provide either {} or {}".format(
                key,
                VALID_KEYS[key]["available_values"][0],
                VALID_KEYS[key]["available_values"][1],
            )
        )
        sys.exit(1)
else:
    if value not in ["true", "false", "toggle"]:
        print("Invalid value. Please provide either 'true' or 'false' or 'toggle'.")
        sys.exit(1)

# Load the config file with caching
config = _load_config()

tailmessage_previously_enabled = config["Tailmessage"]["Enable"]

if key == "changect":
    value = changeCT(value)
elif key == "changeid":
    value = changeID(value)
else:
    # Convert the input value to boolean if not 'toggle'
    if value != "toggle":
        value = value.lower() == "true"

    # Check if toggle is required
    if value == "toggle":
        current_value = config[VALID_KEYS[key]["section"]][VALID_KEYS[key]["key"]]
        value = not current_value

    # Special handling for disabling SKYWARNPLUS or Tailmessage
    if (
        key in ["enable", "tailmessage"]
        and value is False
        and tailmessage_previously_enabled
    ):
        silent_tailmessage()

    # Update the key in the config
    config[VALID_KEYS[key]["section"]][VALID_KEYS[key]["key"]] = value

    # Save the updated config back to the file
    with open(str(CONFIG_FILE), "w") as f:
        yaml.dump(config, f)

# Get the correct audio file based on the new value
audio_file = VALID_KEYS[key]["true_file"] if value else VALID_KEYS[key]["false_file"]

# Play the corresponding audio message on all nodes
nodes = config["Asterisk"]["Nodes"]
for node in nodes:
    try:
        subprocess.run(
            [
                "/usr/sbin/asterisk",
                "-rx",
                "rpt localplay {} {}/SOUNDS/ALERTS/{}".format(
                    node, SCRIPT_DIR, audio_file.rsplit(".", 1)[0]
                ),
            ],
            timeout=30,
            check=False
        )
    except subprocess.TimeoutExpired:
        print(f"Subprocess timeout for node {node}")
    except Exception as e:
        print(f"Subprocess error for node {node}: {e}")
