#!/usr/bin/python3

"""
UpdateSWP.py by Mason Nelson
===============================================================================
Script to update SkywarnPlus to the latest version. This script will download
the latest version of SkywarnPlus from GitHub, and then merge the existing
config.yaml with the new config.yaml. This script will also create a backup of the
existing SkywarnPlus directory before updating.

Please note that this script might not work correctly if you have made
significant changes to the SkywarnPlus code or directory structure.
If you have made significant changes, it is recommended that you manually update SkywarnPlus.

This file is part of SkywarnPlus.
SkywarnPlus is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version. SkywarnPlus is distributed in the hope
that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with SkywarnPlus. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import os.path
import zipfile
import shutil
import requests
import datetime
from functools import lru_cache
import argparse

# Lazy imports for performance
def _lazy_import_yaml():
    """Lazy import YAML to avoid loading unless needed."""
    try:
        from ruamel.yaml import YAML
        return YAML()
    except ImportError:
        raise ImportError("ruamel.yaml is required")

# Set up command line arguments
parser = argparse.ArgumentParser(description="Update SkywarnPlus")
parser.add_argument(
    "-f",
    "--force",
    help="Force update without confirmation prompt",
    action="store_true",
)
args = parser.parse_args()


# Logging function
def log(message):
    print("[UPDATE]:", message)


# Function to load a yaml file with caching
@lru_cache(maxsize=2)
def load_yaml_file(filename):
    yaml = _lazy_import_yaml()
    with open(filename, "r") as f:
        return yaml.load(f)


# Function to save a yaml file
def save_yaml_file(filename, data):
    yaml = _lazy_import_yaml()
    yaml.preserve_quotes = True
    with open(filename, "w") as f:
        yaml.dump(data, f)


# Function to merge two yaml files
def merge_yaml_files(old_file, new_file):
    # Load the old and new yaml files
    old_yaml_data = load_yaml_file(old_file)
    new_yaml_data = load_yaml_file(new_file)

    # Merge the new yaml file with values from the old file
    for key in new_yaml_data:
        if key in old_yaml_data:
            if isinstance(new_yaml_data[key], dict) and isinstance(
                old_yaml_data[key], dict
            ):
                new_yaml_data[key].update(old_yaml_data[key])
            else:
                new_yaml_data[key] = old_yaml_data[key]

    # Save the merged yaml data back to the new file
    save_yaml_file(new_file, new_yaml_data)


def remove_duplicate_comments(filename):
    # Keep track of the last comment block
    last_comment_block = []
    new_lines = []

    # Read the file line by line
    with open(filename, "r") as f:
        lines = f.readlines()

    current_comment_block = []
    for line in lines:
        stripped_line = line.strip()

        # If line is a comment or blank, it's part of the current block
        if stripped_line.startswith("#") or not stripped_line:
            current_comment_block.append(line)
        else:
            if current_comment_block:
                if current_comment_block != last_comment_block:
                    new_lines.extend(current_comment_block)
                last_comment_block = list(current_comment_block)
                current_comment_block = []
            new_lines.append(line)

    # Check after finishing file
    if current_comment_block and current_comment_block != last_comment_block:
        new_lines.extend(current_comment_block)

    # Write the new lines back to the file
    with open(filename, "w") as f:
        f.writelines(new_lines)
        

# Display the initial warning
def display_update_warning():
    warning_message = """
    ============================================================
    WARNING: Please read the following information carefully before updating.

    This utility is designed to update SkywarnPlus to the latest version by fetching it 
    directly from GitHub. Before updating:
    
    - A backup of the existing SkywarnPlus directory will be created to ensure safety.
    
    - The updater will attempt to merge your existing config.yaml with the new version's 
      config.yaml. ALWAYS double-check your config.yaml after updating. This script is not 
      perfect and may not merge your configuration correctly.
    
    - If you've made significant changes to the SkywarnPlus code, directory structure, or 
      configuration, this updater might not work correctly. In such cases, manual updating 
      is recommended.
    
    Remember, this script's primary goal is to help with the updating process. However, 
    given the complexities of merging and updating, always verify the results yourself to 
      ensure your system continues to operate as expected.

    Proceed with caution.
    ============================================================
    """
    print(warning_message)


# Check for root privileges
if os.geteuid() != 0:
    exit("ERROR: This script must be run as root.")

# Make sure the script is in the right directory
if not os.path.isfile("main.py"):
    print(
        "ERROR: Cannot find main.py. Make sure this script is in the SkywarnPlus directory."
    )
    exit()

# Display the warning message
if not args.force:
    display_update_warning()
    
    confirmation = input("\nDo you want to continue with the update? (yes/no) ")
    if confirmation.lower() != "yes":
        log("Update cancelled by user.")
        exit()

# Zip the current directory
root_dir = os.getcwd()
log("Current directory is {}".format(root_dir))

# Full path to the archive
zip_name = root_dir + "_backup_" + datetime.datetime.now().strftime("%Y%m%d_%H%M")
log("Creating backup at {}.zip...".format(zip_name))

# Create the zip archive
shutil.make_archive(zip_name, "zip", root_dir)

# Download the new zip from GitHub
url = (
    "https://github.com/Mason10198/SkywarnPlus/releases/latest/download/SkywarnPlus.zip"
)
log("Downloading SkywarnPlus from {}...".format(url))
# Use session for connection pooling
session = requests.Session()
session.headers.update({
    'User-Agent': 'SkywarnPlus-Update/1.0.0',
    'Accept': 'application/zip',
    'Accept-Encoding': 'gzip, deflate'
})

response = session.get(url, timeout=60)
response.raise_for_status()

with open("/tmp/SkywarnPlus.zip", "wb") as out_file:
    out_file.write(response.content)

# Delete /tmp/SkywarnPlus if it already exists
if os.path.isdir("/tmp/SkywarnPlus"):
    log("Removing old /tmp/SkywarnPlus directory...")
    shutil.rmtree("/tmp/SkywarnPlus")

# Unzip the downloaded file
log("Extracting SkywarnPlus.zip...")
with zipfile.ZipFile("/tmp/SkywarnPlus.zip", "r") as zip_ref:
    zip_ref.extractall("/tmp")

# Merge the old config with the new config
log("Merging old config with new config...")
merge_yaml_files("config.yaml", "/tmp/SkywarnPlus/config.yaml")

# Remove duplicate comments from config.yaml
remove_duplicate_comments("/tmp/SkywarnPlus/config.yaml")

# Replace old directory with updated files
log("Merging updated files into {}...".format(root_dir))
for root, dirs, files in os.walk("/tmp/SkywarnPlus"):
    for file in files:
        old_file_path = os.path.join(root, file)
        relative_path = os.path.relpath(old_file_path, "/tmp/SkywarnPlus")
        new_file_path = os.path.join(root_dir, relative_path)

        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
        shutil.copy2(old_file_path, new_file_path)

# Set all .py files as executable
log("Setting .py files as executable...")
for dirpath, dirs, files in os.walk(root_dir):
    for filename in files:
        if filename.endswith(".py"):
            os.chmod(os.path.join(dirpath, filename), 0o755)  # chmod +x

# Delete temporary files and folders
log("Deleting temporary files and folders...")
shutil.rmtree("/tmp/SkywarnPlus")
os.remove("/tmp/SkywarnPlus.zip")

# Delete old TmpDir if it still exists
if os.path.isdir("/tmp/SkywarnPlus"):
    log("Removing old /tmp/SkywarnPlus directory...")
    shutil.rmtree("/tmp/SkywarnPlus")

log("Update complete!")
