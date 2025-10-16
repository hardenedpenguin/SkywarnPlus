![SkywarnPlus Logo](https://raw.githubusercontent.com/Mason10198/SkywarnPlus/main/Logo_SWP.svg)

![Release Version](https://img.shields.io/github/v/release/Mason10198/SkywarnPlus?label=Version&color=f15d24)
![Release Date](https://img.shields.io/github/release-date/Mason10198/SkywarnPlus?label=Released&color=f15d24)
![Hits](https://img.shields.io/endpoint?url=https%3A%2F%2Fhits.dwyl.com%2FMason10198%2FSkywarnPlus.json&label=Hits&color=f15d24)
![Total Downloads](https://img.shields.io/github/downloads/Mason10198/SkywarnPlus/total?label=Downloads&color=f15d24)
![GitHub Repo Size](https://img.shields.io/github/repo-size/Mason10198/SkywarnPlus?label=Size&color=f15d24)

**SkywarnPlus** is an advanced software solution tailored for Asterisk/app_rpt nodes. It is designed to provide important information about local government-issued alerts in the United States, thereby broadening the scope and functionality of your node. By intelligently integrating local alert data, SkywarnPlus brings a new layer of relevance and utility to your existing system. **SkywarnPlus** works with all major distributions, including AllstarLink, HAMVOIP, myGMRS, GMRS Live, and more.

- [Installation](#installation)
  - [Automated Installation](#automated-installation)
  - [Configuration](#configuration)
- [Modern Architecture](#modern-architecture)
  - [New Modular Structure](#new-modular-structure)
  - [Migration Guide](#migration-guide)
- [TimeType Configuration](#timetype-configuration)
- [Tail Messages](#tail-messages)
- [Courtesy Tones](#courtesy-tones)
  - [Configuration Overview](#configuration-overview)
    - [`config.yaml` Configuration](#configyaml-configuration)
    - [`rpt.conf` Configuration](#rptconf-configuration)
    - [Dynamic Tone Switching](#dynamic-tone-switching)
    - [Consistent Filenames](#consistent-filenames)
- [CW / Voice IDs](#cw--voice-ids)
  - [Configuration](#configuration-1)
- [Pushover Integration](#pushover-integration)
- [SkyControl](#skycontrol)
  - [Usage](#usage)
  - [Spoken Feedback](#spoken-feedback)
  - [Mapping to DTMF Commands](#mapping-to-dtmf-commands)
- [AlertScript](#alertscript)
  - [Understanding AlertScript](#understanding-alertscript)
  - [Matching](#matching)
  - [ClearCommands: Responding to Alert Clearance](#clearcommands-responding-to-alert-clearance)
    - [Why Caution with Wildcards?](#why-caution-with-wildcards)
    - [Best Practice:](#best-practice)
  - [Transition-Based Commands](#transition-based-commands)
    - [ActiveCommands](#activecommands)
      - [Configuration Example for ActiveCommands:](#configuration-example-for-activecommands)
    - [InactiveCommands](#inactivecommands)
      - [Configuration Example for InactiveCommands:](#configuration-example-for-inactivecommands)
    - [Implementing Transition-Based Commands](#implementing-transition-based-commands)
  - [The Power of YOU](#the-power-of-you)
- [SkyDescribe](#skydescribe)
  - [Usage](#usage-1)
  - [Integration with AlertScript](#integration-with-alertscript)
  - [Mapping to DTMF commands](#mapping-to-dtmf-commands-1)
- [Customizing the Audio Files](#customizing-the-audio-files)
  - [County Identifiers](#county-identifiers)
    - [Automated Setup using `CountyIDGen.py`](#automated-setup-using-countyidgenpy)
    - [Manual Setup](#manual-setup)
- [Supermon Integration](#supermon-integration)
  - [AutoSkywarn vs. AUTOSKY](#autoskywarn-vs-autosky)
  - [Supermon 6.1 - 7.4](#supermon-61---74)
  - [Supermon 2](#supermon-2)
    - [ast\_var\_update.sh](#ast_var_updatesh)
    - [SkywarnPlus Integration with Supermon 2 Upgraded](#skywarnplus-integration-with-supermon-2-upgraded)
- [Manual Installation](#manual-installation)
- [Testing](#testing)
- [Debugging](#debugging)
- [Maintenance and Bug Reporting](#maintenance-and-bug-reporting)
- [Contributing](#contributing)
- [Frequently Asked Questions](#frequently-asked-questions)
    - [I just installed SkywarnPlus on my HamVoIP node, why is it giving me errors?](#i-just-installed-skywarnplus-on-my-hamvoip-node-why-is-it-giving-me-errors)
    - [Why do I see depreciation warnings when installing SkywarnPlus on my HamVoIP node?](#why-do-i-see-depreciation-warnings-when-installing-skywarnplus-on-my-hamvoip-node)
    - [Can I change the crontab interval to something other than 60 seconds?](#can-i-change-the-crontab-interval-to-something-other-than-60-seconds)
    - [What does "with multiples" mean?](#what-does-with-multiples-mean)
    - [Why is SkywarnPlus saying the same thing every 60 seconds?](#why-is-skywarnplus-saying-the-same-thing-every-60-seconds)
    - [I just installed SkywarnPlus, why don't I hear anything?](#i-just-installed-skywarnplus-why-dont-i-hear-anything)
    - [There is an active alert in my area, but SkywarnPlus isn't doing anything. What gives?](#there-is-an-active-alert-in-my-area-but-skywarnplus-isnt-doing-anything-what-gives)
    - [Why aren't my test alerts working?](#why-arent-my-test-alerts-working)
    - [Can SkywarnPlus automatically read the full alert description?](#can-skywarnplus-automatically-read-the-full-alert-description)
- [License](#license)

## Key Features

- **Real-Time Alerts:** The software watches the new NWS v1.2 API for real-time alerts for user-defined areas.

- **Automatic Announcements:** Alerts, including when all warnings have been cleared, are announced automatically on the node.

- **Human Speech:** Announcements are delivered in a natural, human speech for easier understanding.

- **Unlimited Area & Node Numbers:** Users can define as many areas and local node numbers as desired.

- **Tailmessage Creation:** The software generates tailmessages for the node to continuously inform listeners about active alerts after the initial broadcast.

- **Dynamic Changes to Node:** Courtesy tones and node CW / voice ID automatically change according to user-defined alerts, optimizing communication during severe weather.

- **County Identification:** Dynamically and automatically inform listeners which county or counties an alert is affecting

- **Efficiency & Speed:** SkywarnPlus is optimized for speed and efficiency to provide real-time information without delay.

- **Preserves Hardware:** SkywarnPlus limits I/O to the physical disk, preventing SD card burnout in Raspberry Pi devices.

- **Remote Control:** Functions can be mapped to DTMF commands for remote over-the-air control.

- **Detailed Alert Descriptions:** In addition to standard alert announcements, SkywarnPlus includes SkyDescribe, a feature for announcing detailed NWS provided descriptions of alert details.

- **Highly Customizable:** SkywarnPlus is extremely customizable, offering advanced filtering parameters to block certain alerts or types of alerts from different functions. Users can easily modify the sound effects and audio files used in SkywarnPlus. Users can even map DTMF macros or shell commands to specified weather alerts, infinitely expanding the software's capabilities according to user needs.

- **Pushover Integration:** With Pushover integration, SkywarnPlus can send weather alert notifications directly to your phone or other devices.

- **Fault Tolerance:** In the event that SkywarnPlus is unable to access the internet for alert updates (during a severe storm), it will continue to function using alert data it has stored from the last successful data update, using the estimated expiration time provided by the NWS to determine when to automatically "clear" alerts. There is no need to worry about your node "locking up" with stale alerts.

Whether you wish to auto-link to a Skywarn net during severe weather, program your node to control an external device like a siren during a tornado warning, or simply want to stay updated on changing weather conditions, SkywarnPlus offers a comprehensive, efficient, and customizable solution for your weather alert needs.

## Comprehensive Information

SkywarnPlus supports all 128 alert types included in the [NWS v1.2 API](https://www.weather.gov/documentation/services-web-api).

|                                    |                                        |                                         |
| ---------------------------------- | -------------------------------------- | --------------------------------------- |
| 911 Telephone Outage Emergency     | Administrative Message                 | Air Quality Alert                       |
| Air Stagnation Advisory            | Arroyo And Small Stream Flood Advisory | Ashfall Advisory                        |
| Ashfall Warning                    | Avalanche Advisory                     | Avalanche Warning                       |
| Avalanche Watch                    | Beach Hazards Statement                | Blizzard Warning                        |
| Blizzard Watch                     | Blowing Dust Advisory                  | Blowing Dust Warning                    |
| Brisk Wind Advisory                | Child Abduction Emergency              | Civil Danger Warning                    |
| Civil Emergency Message            | Coastal Flood Advisory                 | Coastal Flood Statement                 |
| Coastal Flood Warning              | Coastal Flood Watch                    | Dense Fog Advisory                      |
| Dense Smoke Advisory               | Dust Advisory                          | Dust Storm Warning                      |
| Earthquake Warning                 | Evacuation - Immediate                 | Excessive Heat Warning                  |
| Excessive Heat Watch               | Extreme Cold Warning                   | Extreme Cold Watch                      |
| Extreme Fire Danger                | Extreme Wind Warning                   | Fire Warning                            |
| Fire Weather Watch                 | Flash Flood Statement                  | Flash Flood Warning                     |
| Flash Flood Watch                  | Flood Advisory                         | Flood Statement                         |
| Flood Warning                      | Flood Watch                            | Freeze Warning                          |
| Freeze Watch                       | Freezing Fog Advisory                  | Freezing Rain Advisory                  |
| Freezing Spray Advisory            | Frost Advisory                         | Gale Warning                            |
| Gale Watch                         | Hard Freeze Warning                    | Hard Freeze Watch                       |
| Hazardous Materials Warning        | Hazardous Seas Warning                 | Hazardous Seas Watch                    |
| Hazardous Weather Outlook          | Heat Advisory                          | Heavy Freezing Spray Warning            |
| Heavy Freezing Spray Watch         | High Surf Advisory                     | High Surf Warning                       |
| High Wind Warning                  | High Wind Watch                        | Hurricane Force Wind Warning            |
| Hurricane Force Wind Watch         | Hurricane Local Statement              | Hurricane Warning                       |
| Hurricane Watch                    | Hydrologic Advisory                    | Hydrologic Outlook                      |
| Ice Storm Warning                  | Lake Effect Snow Advisory              | Lake Effect Snow Warning                |
| Lake Effect Snow Watch             | Lake Wind Advisory                     | Lakeshore Flood Advisory                |
| Lakeshore Flood Statement          | Lakeshore Flood Warning                | Lakeshore Flood Watch                   |
| Law Enforcement Warning            | Local Area Emergency                   | Low Water Advisory                      |
| Marine Weather Statement           | Nuclear Power Plant Warning            | Radiological Hazard Warning             |
| Red Flag Warning                   | Rip Current Statement                  | Severe Thunderstorm Warning             |
| Severe Thunderstorm Watch          | Severe Weather Statement               | Shelter In Place Warning                |
| Short Term Forecast                | Small Craft Advisory                   | Small Craft Advisory For Hazardous Seas |
| Small Craft Advisory For Rough Bar | Small Craft Advisory For Winds         | Small Stream Flood Advisory             |
| Snow Squall Warning                | Special Marine Warning                 | Special Weather Statement               |
| Storm Surge Warning                | Storm Surge Watch                      | Storm Warning                           |
| Storm Watch                        | Test                                   | Tornado Warning                         |
| Tornado Watch                      | Tropical Depression Local Statement    | Tropical Storm Local Statement          |
| Tropical Storm Warning             | Tropical Storm Watch                   | Tsunami Advisory                        |
| Tsunami Warning                    | Tsunami Watch                          | Typhoon Local Statement                 |
| Typhoon Warning                    | Typhoon Watch                          | Urban And Small Stream Flood Advisory   |
| Volcano Warning                    | Wind Advisory                          | Wind Chill Advisory                     |
| Wind Chill Warning                 | Wind Chill Watch                       | Winter Storm Warning                    |
| Winter Storm Watch                 | Winter Weather Advisory                |

# Installation

## Automated Installation
1. Access the terminal of your node and execute the following command as `root`:
   ```bash
   bash -c "$(curl -fsSL https://raw.githubusercontent.com/Mason10198/SkywarnPlus/main/swp-install)"
   ```
2. The installer will set up a systemd timer to automatically run SkywarnPlus every minute.
3. Continue with [Configuration](#configuration).

> [!NOTE]
> SkywarnPlus requires systemd for automatic execution. If systemd is not available, you can still run SkywarnPlus manually.

> [!NOTE]
> To install manually, see [Manual Installation](#manual-installation).

## Configuration

SkywarnPlus was designed with customization in mind, making it possible to fit nearly any usage scenario you can throw at it. However, this can make the configuration seem a bit daunting. Be patient, and when in doubt, read the documentation.

Edit the [config.yaml](config.yaml) file according to your needs. This is where you will enter your NWS codes, enable/disable specific functions, etc.

```bash
nano config.yaml
```

 You can find your county codes in the [CountyCodes.md](CountyCodes.md) file included in this repository. Navigate to the file and look for your state and then your specific county to find the associated County Code you'll use in SkywarnPlus to poll for alerts.

## Modern Architecture

SkywarnPlus has been completely modernized with a clean, modular architecture following Python best practices. The new structure provides better maintainability, testability, and extensibility while maintaining full backward compatibility.

### New Modular Structure

The application has been restructured into focused modules:

**Core Application:**
- **`src/skywarnplus.py`** - Main application class
- **`src/api_client.py`** - NWS API interactions
- **`src/audio_processor.py`** - Audio processing and caching
- **`src/alert_processor.py`** - Alert processing and management
- **`src/state_manager.py`** - State persistence
- **`src/alert_announcer.py`** - Alert announcements and audio generation
- **`src/notification_service.py`** - Pushover and other notifications
- **`src/asterisk_integration.py`** - Asterisk/repeater integration
- **`src/config.py`** - Configuration management

**Utilities:**
- **`src/tts_processor.py`** - Text-to-speech processing
- **`src/text_processor.py`** - Text processing utilities
- **`src/county_id_generator.py`** - County audio file generation
- **`src/config_controller.py`** - Configuration control operations

**Support:**
- **`src/data_types.py`** - Type definitions and dataclasses
- **`src/constants.py`** - Constants and enums
- **`src/exceptions.py`** - Custom exception classes

**Modernized Scripts:**
- **`main.py`** - Main SkywarnPlus entry point
- **`skydescribe.py`** - Modernized TTS utility
- **`countyidgen.py`** - Modernized county ID generator
- **`skycontrol.py`** - Modernized configuration controller

### Migration Guide

The new structure is fully backward compatible:

- **Existing `config.yaml`** works unchanged
- **All functionality preserved** from the original version
- **New entry point**: Use `python3 main.py` instead of `python3 SkywarnPlus.py`
- **Same output formats** and file locations

For detailed migration information, see [MODERNIZATION_GUIDE.md](MODERNIZATION_GUIDE.md).

**Quick Start with New Structure:**
```bash
# Install dependencies (if not already installed)
pip3 install -r requirements.txt

# Run SkywarnPlus
python3 main.py

# Use modernized utilities
python3 skydescribe.py "Tornado Warning"    # Generate TTS for alert
python3 countyidgen.py --force              # Generate county audio files
python3 skycontrol.py set sayalert true     # Control configuration
```

> [!WARNING]
> YOU WILL MISS ALERTS IF YOU USE A **ZONE** CODE. DO NOT USE **ZONE** CODES UNLESS YOU KNOW WHAT YOU ARE DOING.

According to the official [NWS API documentation](https://www.weather.gov/documentation/services-web-api):

> "For large scale or longer lasting events, such as snow storms, fire threat, or heat events, alerts are issued
> by NWS public forecast zones or fire weather zones. These zones differ in size and can cross county
> boundaries."

> "...county based alerts are not mapped to zones but zone based alerts are mapped to counties. The effect this has is for requests such as:
>
> https://api.weather.gov/alerts/active?zone=MDZ013
>
> or
>
> https://api.weather.gov/alerts?zone=MDZ013
>
> Will not contain county based products. However requests such as:
>
> https://api.weather.gov/alerts?zone=MDC033
>
> or
>
> https://api.weather.gov/alerts/active?zone=MDC033
>
> Will contain all county based alerts and all zone based alerts that are associated to the county or counties requested. If there are multiple zones associated with that county, the response from API will include all alerts for those zones."

[This information was obtained from this document.](https://www.weather.gov/media/documentation/docs/NWS_Geolocation.pdf)

This means that if you use a County code, you will receive all alerts for both your County **AND** your Zone - but if you use a Zone code, you will **ONLY** receive alerts that cover the entire Zone, and none of the alerts specific to your County.

> [!IMPORTANT]
> When SkywarnPlus runs for the first time after installation (and for the first time at each boot), **YOU WILL NOT HEAR ANY MESSAGES** until alerts are detected. This is by design. SkywarnPlus announces when alerts change from `none` to `some`, and it announces when alerts change from `some` to `none`. It will announce nothing if the status of alerts does not change (`none` to `none`).

> [!TIP]
If you want to test SkywarnPlus' operation after installation, please see the **Testing** section of this README.

# TimeType Configuration
This setting in SkywarnPlus determines the timing for issuing weather alerts. Users have the option to select between "onset" and "effective" time types, which influence the alerting strategy as follows:

- **ONSET**
  - With the ONSET setting, alerts are issued based on the anticipated start time of the weather event. This ensures that alerts are timely and relevant, focusing on imminent events. For instance, consider an Air Quality Alert issued due to a distant wildfire's smoke predicted to affect the area in three days time. While the alert might be issued early by the NWS, SkywarnPlus will only process the alert at the actual onset of the deteriorating air quality, avoiding premature notifications about conditions that are not yet affecting the area. Additionally, if Tailmessages are enabled, then using the ONSET setting prevents unnecessary repeated notifications of an event over an extended period of time.

- **EFFECTIVE**
  - In contrast, the EFFECTIVE setting triggers SkywarnPlus to process alerts immediately upon their issuance from the NWS, regardless of the time until the subject matter is considered to be onset. This can result in alerts being announced well in advance of the actual event. Using the same Air Quality Alert scenario, the alert would be processed and announced as soon as it is issued, regardless of the smoke's actual arrival time, potentially leading to early warnings about conditions that are days away from materializing. Additionally, if Tailmessages are enabled, then the Air Quality Alert notifications would be continuously repeated for 3 days prior to the event actually occuring.

The default ONSET setting is recommended for ensuring that alerts are pertinent and actionable. It helps in maintaining the alert system's credibility by avoiding unnecessary alarms about conditions that are forecasted but not yet imminent, thereby aiding in better preparedness and response when the event actually occurs.

When in doubt, you can verity the exact data being provided by the NWS API, and whether an alert is currently EFFECTIVE or ONSET, by visiting the API endpoing in the following format:
```
https://api.weather.gov/alerts/active?zone=YOUR_COUNTY_CODE_HERE
```

> [!NOTE]
> Most weather websites and applications, including the NWS's own website, use the EFFECTIVE time when displaying "active" alerts. This often leads SkywarnPlus users to believe that their SkywarnPlus-enabled system is not functioning correctly when an alert is visible on the NWS website, but SkywarnPlus has not processed it yet. This discrepancy is due to the different alert processing times based on the chosen TimeType setting in SkywarnPlus. While other services might show alerts as soon as they become effective, SkywarnPlus, when set to ONSET, waits until the conditions are imminent. It's important for users to understand this distinction to accurately assess the functionality of their SkywarnPlus system.

# Tail Messages

SkywarnPlus can automatically create, manage, and remove a tail message whenever certain weather alerts are active to keep listeners informed throught the duration of active alerts. The configuration for this will be based on your `rpt.conf` file setup. Here's an example:

```ini
tailmessagetime = 600000
tailsquashedtime = 30000
tailmessagelist = /tmp/SkywarnPlus/wx-tail
```

# Courtesy Tones

SkywarnPlus offers the capability to dynamically change node courtesy tones based on the current weather alert status. This feature enhances the responsiveness and informational value of the repeater system by providing auditory signals corresponding to specific weather conditions. Configuration is managed via the `config.yaml` and `rpt.conf` files, allowing for precise control over tone behavior.

## Configuration Overview

The setup process involves specifying your preferences in the `config.yaml` file and ensuring the `rpt.conf` file correctly references the managed courtesy tone files.

### `config.yaml` Configuration

Within `config.yaml`, you can enable the feature, specify the directory for tone files, and define the tones for "normal" and "wx" (weather alert) modes. Here's an example configuration:

```yaml
CourtesyTones:
  # Configuration for automatic CT changing. Requires initial setup in RPT.CONF.
  # Enable/disable automatic courtesy tones.
  Enable: true

  # Directory where tone files will be read from & stored to. Modify this path to match your setup.
  # Default location is within the SkywarnPlus installation directory.
  ToneDir: /usr/local/bin/SkywarnPlus/SOUNDS/TONES

  # Define custom courtesy tones for use in different modes. This allows for dynamic response to weather alerts.
  Tones:
    # Define each courtesy tone, and which files to use for that tone in Normal and WX mode.
    ct1:
      Normal: Boop.ulaw
      WX: Stardust.ulaw

    ct2:
      Normal: Beep.ulaw
      WX: Stardust.ulaw
      
    ct3:
      Normal: NBC.ulaw
      WX: SatPass.ulaw

    ct4:
      Normal: BlastOff.ulaw
      WX: Target.ulaw
    
    ct5:
      Normal: BumbleBee.ulaw
      WX: XPError.ulaw
    
    ct6:
      Normal: Comet.ulaw
      WX: Waterdrop.ulaw
```

### `rpt.conf` Configuration

Ensure `rpt.conf` is set up to reference the courtesy tone files that SkywarnPlus manages. The configuration should match the defined tones in `config.yaml`. Example:

```ini
[NODENUMBER]
unlinkedct = ct1
remotect = ct1
linkunkeyct = ct2
[telemetry]
ct1 = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/ct1
ct2 = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/ct2
ct3 = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/ct3
ct4 = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/ct4
ct5 = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/ct5
ct6 = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/ct6
remotetx = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/ct1
remotemon = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/ct1
```

### Dynamic Tone Switching

When enabled, SkywarnPlus will automatically switch between "normal" and "wx" mode tones based on the active weather alerts defined in the `CTAlerts` section of `config.yaml`. This change enhances situational awareness through auditory cues.

### Consistent Filenames

Ensure that filenames and case sensitivity are consistent across `config.yaml` and `rpt.conf` to ensure seamless operation.

After initially setting up automatic courtesy tones, the audio files will not refresh until the next time the alert status changes. To refresh immediately, run `/usr/local/bin/SkywarnPlus/SkyControl.py changect normal` to force the CTs to "normal" mode.

# CW / Voice IDs

SkywarnPlus has a feature that allows it to automatically change the node ID based on the status of certain weather alerts. This requires the creation of custom audio files for the `NORMAL` and `WX` ID modes.

The configuration for this is in the `config.yaml` file, with additional setup needed in the `rpt.conf` file. Let's take a look at how it's done.

## Configuration

Here's an example of how the `config.yaml` file should be configured:

```yaml
IDChange:
  # Configuration for Automatic ID Changing. Requires initial setup in RPT.CONF and manual creation of audio files.

  # Enable/disable automatic ID changing.
  Enable: false

  # Specify an alternative directory where ID files are located.
  # Default is SkywarnPlus/SOUNDS/ID.
  IDDir: /usr/local/bin/SkywarnPlus/SOUNDS/ID

  # Define the sound files for IDs.
  IDs:
    # Audio file to feed Asterisk as ID in "normal" mode
    NormalID: NORMALID.ulaw

    # Audio file to feed Asterisk as ID in "wx" mode
    WXID: WXID.ulaw

    # Audio file rpt.conf is looking for as ID
    RptID: RPTID.ulaw
```

In this setup, if none of the alerts specified in the IDAlerts list are active, SkywarnPlus replaces the file `RPTID.ulaw` with a duplicate of `NORMALID.ulaw`.

However, if any of the alerts in the IDAlerts list are currently active, SkywarnPlus will replace `RPTID.ulaw` with a duplicate of `WXID.ulaw`.

To enable these changes, the following setup is required in your `rpt.conf` file:

```ini
[NODENUMBER]
idrecording = /usr/local/bin/SkywarnPlus/SOUNDS/ID/RPTID
```

In this case, Asterisk will always use `RPTID.ulaw` as the node ID. SkywarnPlus effectively changes the contents of the `RPTID.ulaw` file depending on the weather alert status while Asterisk "isn't looking".

Note that filenames are case-sensitive, so be sure they match exactly between `rpt.conf` and `config.yaml`.

After initially setting up automatic IDs, the audio files will not refresh until the next time the alert status changes. To refresh immediately, run `/usr/local/bin/SkywarnPlys/SkyControl.py changeid normal` to force the ID to "normal" mode.

# Pushover Integration

SkywarnPlus can use the free Pushover API to send WX alert notifications and debug messages directly to your smartphone or other devices.

1. Visit https://pushover.net/ to sign up for a free account.
2. Find your UserKey on your main dashboard
3. Scroll down and create an Application/API key for your node
4. Add UserKey & API Key to `config.yaml`

# SkyControl

SkywarnPlus comes with a powerful control script (`SkyControl.py`) that can be used to enable or disable certain SkywarnPlus functions via shell, without manually editing `config.yaml`. This script is particularly useful when you want to map DTMF control codes to these functions. An added advantage is that the script provides spoken feedback upon execution, making it even more suitable for DTMF control.

## Usage

To use the `SkyControl.py` script, you need to call it with two parameters:

1. The name of the setting you want to change (case insensitive).

   - Enable (Completely enable/disable SkywarnPlus)
   - SayAlert
   - SayAllClear
   - TailMessage
   - CourtesyTone
   - IDChange
   - AlertScript

2. The new value for the setting (either 'true' or 'false' or 'toggle').

For example, to completely disable SkywarnPlus, you would use:

```bash
/usr/local/bin/SkywarnPlus/SkyControl.py enable false
```

And to reenable it, you would use:

```bash
/usr/local/bin/SkywarnPlus/SkyControl.py enable true
```

And to toggle it, you would use:

```bash
/usr/local/bin/SkywarnPlus/SkyControl.py enable toggle
```

> [!TIP]
> Running the `Enable` command after installing SkywarnPlus is not necessary. The enable flag is already set to `true` in the `config.yaml` file by default, and all you need to do for SkywarnPlus to operate is execute it (or allow it to be executed automatically).

You can also use `SkyControl.py` to manually force the state of Courtesy Tones or IDs:

```bash
/usr/local/bin/SkywarnPlus/SkyControl.py changect normal
/usr/local/bin/SkywarnPlus/SkyControl.py changect wx
/usr/local/bin/SkywarnPlus/SkyControl.py changeid normal
/usr/local/bin/SkywarnPlus/SkyControl.py changect wx
```

## Spoken Feedback

Upon the successful execution of a control command, the `SkyControl.py` script will provide spoken feedback that corresponds to the change made. For instance, if you execute a command to enable the SayAlert function, the script will play an audio message stating that SayAlert has been enabled. This feature enhances user experience and confirms that the desired changes have been effected.

## SystemD Timer Management

SkywarnPlus uses systemd timers for automatic execution instead of cron jobs. This provides better logging, more precise scheduling, and improved reliability.

### Timer Status and Control

You can manage the SkywarnPlus systemd timer using the `timer` command:

```bash
# Check timer status
python3 skycontrol.py timer status

# Start the timer
python3 skycontrol.py timer start

# Stop the timer
python3 skycontrol.py timer stop

# Restart the timer
python3 skycontrol.py timer restart

# Enable timer to start on boot
python3 skycontrol.py timer enable

# Disable timer from starting on boot
python3 skycontrol.py timer disable

# View recent logs
python3 skycontrol.py timer logs

# List all systemd timers
python3 skycontrol.py timer list
```

### Viewing Logs

SkywarnPlus logs are integrated with the systemd journal, providing centralized logging:

```bash
# View SkywarnPlus service logs
journalctl -u skywarnplus.service

# Follow logs in real-time
journalctl -u skywarnplus.service -f

# View logs from last hour
journalctl -u skywarnplus.service --since "1 hour ago"

# View timer status
systemctl status skywarnplus.timer

# List all active timers
systemctl list-timers
```

### Timer Configuration

The systemd timer runs SkywarnPlus every minute by default. The timer configuration is located at:
- Service: `/etc/systemd/system/skywarnplus.service`
- Timer: `/etc/systemd/system/skywarnplus.timer`

### Advantages of SystemD Timers

- **Better Logging**: All output goes to the systemd journal
- **More Precise Scheduling**: Sub-second accuracy vs cron's minute precision
- **Dependency Management**: Can wait for network and other services
- **Persistent Execution**: Catches up if system was down
- **Centralized Management**: Use `systemctl` for all timer operations
- **Resource Limits**: Built-in security and resource constraints

## Mapping to DTMF Commands

> [!IMPORTANT]
> In regards to ASL3, the Asterisk process no longer runs as the `root` user. Therefore, in order to call most SkyControl functions via DTMF, you will need to enable passwordless sudo access for the `asterisk` user and add `sudo` to the DTMF commands in `rpt.conf`.

You can map the `SkyControl.py` script to DTMF commands in the `rpt.conf` file of your node. Here is an example of how to do this:

```ini
; SkyControl DTMF Commands
831 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py enable toggle ; Toggles SkywarnPlus
832 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py sayalert toggle ; Toggles SayAlert
833 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py sayallclear toggle ; Toggles SayAllClear
834 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py tailmessage toggle ; Toggles TailMessage
835 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py courtesytone toggle ; Toggles CourtesyTone
836 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py alertscript toggle ; Toggles AlertScript
837 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py idchange toggle ; Toggles IDChange
838 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py changect normal ; Forces CT to "normal" mode
839 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py changeid normal ; Forces ID to "normal" mode
840 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py timer status ; Check systemd timer status
841 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py timer restart ; Restart systemd timer
842 = cmd,/usr/local/bin/SkywarnPlus/SkyControl.py timer logs ; View recent logs
```

With this setup, you can control SkywarnPlus' functionality using DTMF commands.

# AlertScript

SkywarnPlus's `AlertScript` feature is an immensely flexible tool that provides the ability to program your node to respond to specific alerts in unique ways. By enabling you to map alerts to DTMF commands or bash scripts, `AlertScript` offers you the versatility to design your own extensions to SkywarnPlus, modifying its functionalities to perfectly fit your needs.

With `AlertScript`, you can outline actions to be executed when specific alerts are activated. For instance, you might want to broadcast a unique sound, deliver a particular message, or initiate any other action your hardware can perform and that can be activated by a DTMF command or bash script.

## Understanding AlertScript

To utilize `AlertScript`, you define the mapping of alerts to either DTMF commands or bash scripts in the `config.yaml` file under the `AlertScript` section.

Here are examples of how to map alerts to DTMF commands or bash scripts:

```yaml
AlertScript:
  # Completely enable/disable AlertScript
  Enable: false
  Mappings:
    # Define the mapping of alerts to either DTMF commands or bash scripts here.
    # Examples:
    #
    # This entry will execute the bash command 'asterisk -rx "rpt fun 1999 *123*456*789"'
    # when the alerts "Tornado Warning" AND "Tornado Watch" are detected. It will execute the
    # bash command 'asterisk -rx "rpt fun 1999 *987*654*321"' when there are no longer ANY alerts matching
    # "Tornado Warning" OR "Tornado Watch".
    #
    - Type: DTMF
      Nodes:
        - 1999
      Commands:
        - "*123*456*789"
      ClearCommands:
        - "*987*654*321"
      Triggers:
        - Tornado Warning
        - Tornado Watch
      Match: ALL
    #
    # This entry will execute the bash command '/home/repeater/testscript.sh'
    # and the bash command '/home/repeater/saytime.sh' when an alert whose
    # title ends with "Statement" is detected.
    #
    - Type: BASH
      Commands:
        - "/home/repeater/testscript.sh"
        - "/home/repeater/saytime.sh"
      Triggers:
        - "*Statement"
    #
    # This entry will execute the bash command 'asterisk -rx "rpt fun 1998 *123*456*789"'
    # and the bash command 'asterisk -rx "rpt fun 1999 *123*456*789"' when an alert
    # titled "Tornado Warning" OR "Tornado Watch" is detected.
    #
    - Type: DTMF
      Nodes:
        - 1998
        - 1999
      Commands:
        - "*123*456*789"
      Triggers:
        - Tornado Warning
        - Tornado Watch
    #
    # This entry will execute the bash command 'asterisk -rx "rpt fun 1999 *123*456*789"'
    # and the bash command 'asterisk -rx "rpt fun 1999 *987*654*321"'
    # when an alert titled "Tornado Warning" OR "Tornado Watch" is detected.
    #
    - Type: DTMF
      Nodes:
        - 1999
      Commands:
        - "*123*456*789"
        - "*987*654*321"
      Triggers:
        - Tornado Warning
        - Tornado Watch
      Match: ANY
    #
    # This is an example entry that will automatically execute SkyDescribe and
    # announce the full details of a Tornado Warning when it is detected.
    #
    - Type: BASH
      Commands:
        - '/usr/local/bin/SkywarnPlus/SkyDescribe.py "Tornado Warning"'
      Triggers:
        - Tornado Warning
```

## Matching

The `Match:` parameter tells `AlertScript` how to handle the triggers. If `Match: ANY`, then only 1 of the triggers needs to be matched for the command(s) to execute. If `Match: ALL`, then all of the triggers must be matched for the command(s) to execute. If `Match:` is not defined, then `ANY` is used by default.

## ClearCommands: Responding to Alert Clearance

With the introduction of `ClearCommands`, `AlertScript` now allows you to define actions that should be executed once a specific alert has been cleared. This can be particularly useful for scenarios where you want to notify users that a previously active alert is no longer in effect or to reset certain systems to their default state after an alert ends.

In the `config.yaml` file, under each mapping in the `AlertScript` section, you can specify the `ClearCommands` that should be executed when the corresponding alert(s) are cleared.

For example:

```yaml
- Type: DTMF
  Nodes:
    - 1999
  Commands:
    - "*123*456*789"
  ClearCommands:
    - "*987*654*321"
  Triggers:
    - Tornado Warning
    - Tornado Watch
  Match: ALL
```

In the above configuration, when the alerts "Tornado Warning" AND "Tornado Watch" are detected, the DTMF macro `*123*456*789` will be executed. However, when there are no longer ANY alerts matching "Tornado Warning" OR "Tornado Watch", the DTMF macro `*987*654*321` will be executed.

> [!WARNING]
> While `ClearCommands` enhances `AlertScript`'s functionality, it's important to exercise caution when using them with wildcard-based mappings (`*`). This is because such mappings may not behave as expected with `ClearCommands`, especially in complex alert scenarios where multiple alerts might be active simultaneously.

### Why Caution with Wildcards?

Wildcards offer broad matching capabilities, activating `Commands` for a wide range of alerts. However, when it comes to alert clearance (`ClearCommands`), the broad nature of wildcards can lead to unintended behaviors:

- **Non-Specific Clearance**: Wildcards do not specify a single alert clearance that should trigger `ClearCommands`, potentially causing them to execute in unintended scenarios.
- **Overlap and Confusion**: In situations with multiple active alerts covered by a single wildcard trigger, identifying the precise moment for `ClearCommands` execution can become ambiguous and may not function as intended.

### Best Practice:

It's recommended to use specific mappings for `ClearCommands` to ensure precise and predictable behavior upon alert clearance. If using wildcards, be prepared for `ClearCommands` to potentially execute in broader circumstances than anticipated, and consider the overall context of your alert management strategy.

## Transition-Based Commands

`AlertScript` includes the capability to execute specific BASH or DTMF commands based on transitions in overall state of alert activity.

### ActiveCommands

`ActiveCommands` are designed to be executed when the system transitions from a state of having zero active weather alerts to a state where one or more alerts become active. This feature is particularly useful for signaling the onset of weather-related activities or conditions that warrant immediate attention or action.

#### Configuration Example for ActiveCommands:

```yaml
ActiveCommands:
  - Type: BASH
    Commands:
      - 'echo "THE NUMBER OF ACTIVE ALERTS JUST CHANGED FROM ZERO TO NON-ZERO"'
```

In this example, a message is echoed whenever the system detects the first active weather alert after a period of no alerts. This could be adapted to activate lights, sounds, or other notification systems to alert of changing conditions.

### InactiveCommands

Conversely, `InactiveCommands` are triggered when the number of active weather alerts changes from one or more to zero. This transition indicates a return to a state of no immediate weather threats, and commands under this category can be used to deactivate alerts, reset systems, or notify personnel of the all-clear status.

#### Configuration Example for InactiveCommands:

```yaml
InactiveCommands:
  - Type: BASH
    Commands:
      - 'echo "THE NUMBER OF ACTIVE ALERTS JUST CHANGED FROM NON-ZERO TO ZERO"'
```

This example would output a message signaling that all active weather alerts have been cleared. Similar to `ActiveCommands`, `InactiveCommands` can be customized to perform a wide range of actions, such as turning off alerting systems or sending an all-clear message through your communication channels.

### Implementing Transition-Based Commands

To utilize these new command types, simply add `ActiveCommands` and/or `InactiveCommands` to your `AlertScript` configuration in the `config.yaml` file, following the same format as other AlertScript mappings. This allows for both BASH and DTMF commands to be executed in response to changes in the alert status landscape, providing a dynamic and responsive alert management system.

## The Power of YOU

`AlertScript` derives its power from its versatility and extensibility. By providing the capacity to directly interface with your node's functionality through DTMF commands or bash scripts, you can effectively program the node to do virtually anything in response to a specific weather alert.

Fancy activating a siren when a tornado warning is received? You can do that. Want to send an email notification when there's a severe thunderstorm warning? You can do that too. The only limit is the capability of your node and connected systems.

In essence, `AlertScript` unleashes a world of customization possibilities, empowering you to add new capabilities to SkywarnPlus, create your own extensions, and modify your setup to align with your specific requirements and preferences. By giving you the authority to dictate how your system should react to various weather alerts, `AlertScript` makes SkywarnPlus a truly powerful tool for managing weather alerts on your node.

# SkyDescribe

`SkyDescribe` is a powerful and flexible tool that works in tandem with SkywarnPlus. It enables the system to provide a spoken detailed description of weather alerts, adding depth and clarity to the basic information broadcasted by default.

The `SkyDescribe.py` script works by fetching a specific alert from the stored data (maintained by SkywarnPlus) based on the title or index provided. The script then converts the description to audio using a free text-to-speech service and broadcasts it using Asterisk on the defined nodes.

## Usage

To use `SkyDescribe.py`, you simply execute the script with the title or index of the alert you want to be described. The index of the alert is the place it holds in the alert announcement or tailmessage (depending on blocking sonfiguration).

For example, if SkywarnPlus announces `"Tornado Warning, Tornado Watch, Severe Thunderstorm Warning"`, you could execute the following:

```bash
SkyDescribe.py 1 # Describe the 1st alert (Tornado Warning)
SkyDescribe.py 2 # Describe the 2nd alert (Tornado Watch)
SkyDescribe.py 3 # Describe the 3rd alert (Severe Thunderstorm Warning)
```

or, you can use the title of the alert instead of the index:

```bash
SkyDescribe.py "Tornado Warning"
SkyDescribe.py "Tornado Watch"
SkyDescribe.py "Severe Thunderstorm Warning"
```

## Integration with AlertScript

`SkyDescribe.py` can be seamlessly integrated with `AlertScript`, enabling automatic detailed description announcements for specific alerts. This can be accomplished by mapping the alerts to a bash command that executes `SkyDescribe.py` with the alert title as a parameter.

Here's an example of how to achieve this in the `config.yaml` file:

```yaml
AlertScript:
  Enable: true
  Mappings:
    # This is an example entry that will automatically execute SkyDescribe and
    # announce the full details of a Tornado Warning when it is detected.
    - Type: BASH
      Commands:
        - "echo Tornado Warning detected!"
        - '/usr/local/bin/SkywarnPlus/SkyDescribe.py "Tornado Warning"'
      Triggers:
        - Tornado Warning
```

## Mapping to DTMF commands

For added flexibility, `SkyDescribe.py` can also be linked to DTMF commands, allowing alert descriptions to be requested over-the-air.

```ini
; SkyDescribe DTMF Commands
841 = cmd,/usr/local/bin/SkywarnPlus/SkyDescribe.py 1 ; SkyDescribe the 1st alert
842 = cmd,/usr/local/bin/SkywarnPlus/SkyDescribe.py 2 ; SkyDescribe the 2nd alert
843 = cmd,/usr/local/bin/SkywarnPlus/SkyDescribe.py 3 ; SkyDescribe the 3rd alert
844 = cmd,/usr/local/bin/SkywarnPlus/SkyDescribe.py 4 ; SkyDescribe the 4th alert
845 = cmd,/usr/local/bin/SkywarnPlus/SkyDescribe.py 5 ; SkyDescribe the 5th alert
846 = cmd,/usr/local/bin/SkywarnPlus/SkyDescribe.py 6 ; SkyDescribe the 6th alert
847 = cmd,/usr/local/bin/SkywarnPlus/SkyDescribe.py 7 ; SkyDescribe the 7th alert
848 = cmd,/usr/local/bin/SkywarnPlus/SkyDescribe.py 8 ; SkyDescribe the 8th alert
849 = cmd,/usr/local/bin/SkywarnPlus/SkyDescribe.py 9 ; SkyDescribe the 9th alert
```

> [!IMPORTANT]
> If you have SkywarnPlus set up to monitor multiple counties, it will, by design, only store **ONE** instance of each alert type in order to prevent announcing duplicate messages. Because of this, if SkywarnPlus checks 3 different counties and finds a `"Tornado Warning"` in each one, only the first description will be saved. Thus, executing `SkyControl.py "Tornado Warning"` will broadcast the description of the `"Tornado Warning"` for the first county **ONLY**.
> 
> In _most_ cases, any multiple counties that SkywarnPlus is set up to monitor will be adjacent to one another, and any duplicate alerts would actually be the **_same_** alert with the **_same_** description, so this wouldn't matter.

# Customizing the Audio Files

SkywarnPlus comes with a library of audio files that can be replaced with any 8kHz mono PCM16 WAV files you want. These are found in the `SOUNDS/` directory by default, along with `DICTIONARY.txt` which explains audio file assignments. Several customizations can be easily made in `config.yaml`, but the sound files are always available for you to modify directly as well.

If you'd like to use IDChange, you must create your own audio files. Follow **[this guide](https://wiki.allstarlink.org/images/d/dd/RecordingSoundFiles.pdf)** on how to record/convert audio files for use with Asterisk/app_rpt.

> [!TIP]
> For users wishing to maintain vocal continuity in their SkywarnPlus installation, the original creator of SkywarnPlus (N5LSN) and the woman behind the voice of it's included library of audio recordings (N5LSN XYL) will, for a small fee, record custom audio files for your SkywarnPlus installation. Contact information is readily available via QRZ.

## County Identifiers

SkywarnPlus features the capability to play county-specific audio files to reference the affected area of alerts. It enhances the user's awareness of the geographic area affected by an event, making the system more informative and valuable to users monitoring systems that provide coverage for multiple counties. By assigning unique audio tags to each county, users can immediately recognize which county is affected by an event as soon as it is detected by SkywarnPlus.

### Automated Setup using `CountyIDGen.py`

To simplify the process of setting up county-specific audio tags, SkywarnPlus provides a utility script called CountyIDGen.py. This script is designed to:

- Generate WAV audio files for each county code defined in the config.yaml using the Voice RSS Text-to-Speech API.
- Save these generated files in the proper directory.
- Modify the config.yaml automatically to reference these files.

To use the script for automated setup, simply make sure you have already set up all of your county codes (`Alerting` section) and VoiceRSS details (`SkyDescribe` section) in `config.yaml`, and then execute the script:
```bash
./CountyIDGen.py
```
### Manual Setup

Manual setup involves creating or otherwise aquire these audio files yourself. The audio files must be located in the root of the `SkywarnPlus/SOUNDS/` directory.

The `config.yaml` explains how to use the free VoiceRSS API to generate these files using a computer synthesized voice.

Here is an example of how to manually configure the `config.yaml` to utilize this feature:

```yaml
Alerting:
  # Specify the county codes for which you want to pull weather data.
  # Find your county codes at https://alerts.weather.gov/.
  # Make sure to use county codes ONLY, NOT zone codes, otherwise you might miss out on alerts.
  #
  # SkywarnPlus allows adding county-specific audio indicators to each alert in the message.
  # To enable this feature, specify an audio file containing a recording of the county name in the
  # ROOT of the SOUNDS/ directory as shown in the below example. You must create these files yourself.
  # You can use the same VoiceRSS API used for SkyDescribe (see below) to generate these files with a synthetic voice:
  # http://api.voicerss.org/?key=[YOUR_API_KEY_HERE]=en-us&f=8khz_16bit_mono&v=John&src=[YOUR COUNTY NAME HERE]
  # http://api.voicerss.org/?key=1234567890QWERTY&hl=en-us&f=8khz_16bit_mono&v=John&src=Saline County
  CountyCodes:
    - DCC001: "County1.wav"
    - MDC031: "County2.wav"
    - MDC033: "County3.wav"
    - VAC013: "County4.wav"
    - VAC059: "County5.wav"
    - VAC510: "County6.wav"
    - VAC107: "County7.wav"
    - VAC047: "County8.wav"
    - MDC510: "County9.wav"
    - VAC683: "County10.wav"
```

# Supermon Integration
The compatibility between various versions of Supermon and SkywarnPlus, as well as their interactions with the now outdated AutoSkywarn / AUTOSKY, requires clarification due to historical development constraints and system updates. Below is a detailed explanation of the intended functionalities and limitations.

All of the integration functionality implemented by SkywarnPlus described below are workarounds. They need to be replaced by proper integration from Supermon/Supermon2 developers. Please encourage developers to check the `/tmp/SkywarnPlus/data.json` for alerts to display so that these 'hacks' can be removed.

> [!IMPORTANT]
> ## Important Note About ASL3
> Starting with AllStarLink 3 (ASL3), Asterisk has been upgraded to version 20 and no longer runs as the `root` user. Consequently, SkywarnPlus also runs without root privileges on ASL3 systems. As a result, SkywarnPlus needs a helper script with the necessary permissions (`ASL3_Supermon_Workaround.py`) to create or modify the `/tmp/AUTOSKY/warnings.txt` file.

## AutoSkywarn vs. AUTOSKY
The original AutoSkywarn (KF5VH) was forked and modified to create the very similar AUTOSKY (HamVoIP). For the purposes of this document, they are considered the same.

## Supermon 6.1 - 7.4
In Supermon versions 6.1 - 7.4, the following code segment was added to `link.php` to ingest plaintext alert titles from a file created by AUTOSKY:

```php
// ADDED WA3DSP Autosky warning messages
// if they exist
if (file_exists("/tmp/AUTOSKY/warnings.txt")) {
    if (filesize("/tmp/AUTOSKY/warnings.txt")) {
        $warnings = file_get_contents("/tmp/AUTOSKY/warnings.txt");
        print "<span style=\"color: red;\"><br><b>$warnings</b></span>";
    }
}
// END WA3DSP
```

This code segment in Supermon versions 6.1 - 7.4 simply adds the entire contents of the `/tmp/AUTOSKY/warnings.txt` text file to the webpage, colors them red, and makes them bold. The contents of `/tmp/AUTOSKY/warnings.txt` would look like this:

```
Tornado Warning
Severe Thunderstorm Warning
Tornado Watch
```

A workaround called `SupermonCompat` was added to SkywarnPlus so that the alert titles would still be displayed in Supermon. This feature simply adds alert titles to `/tmp/AUTOSKY/warnings.txt` so that Supermon versions 6.1 - 7.4 can display them.

## Supermon 2

> [!IMPORTANT]
> You will still need to add your location info to `/usr/local/sbin/node_info.ini` for Supermon2 to display the correct weather information.

A completely separate version of Supermon, called Supermon 2, was also written with the intention of ingesting alert titles from AUTOSKY. Supermon 2 operates differently from its predecessors. It reads the Asterisk channel variables for each node and places those variables into the Node Information section. These variables are always empty when Asterisk first starts up. To address this, Supermon 2 includes a script called `ast_var_update.sh`.

### ast_var_update.sh
The `ast_var_update.sh` script needs to be run periodically to update variables in Allstar, which are used to transfer data to Supermon 2 from local or remote servers. This script updates various pieces of information, including the CPU temperature, uptime, load average, weather, alerts, log file size, and registration status for the nodes displayed in Supermon 2.

Please note that the `ast_var_update.sh` script included with Supermon 2 will process the `/tmp/AUTOSKY/warnings.txt` file in a way that mostly works with, but is not fully compatible with, SkywarnPlus. It will attempt to wrap the alert titles in `<a>` tags to create a hyperlink to that alert on the NWS website, but it does so by using the `AutoSky.ini` file, which does not exist unless AUTOSKY is installed. As a result, SkywarnPlus alerts in Supermon 2 have historically hyperlinked to nowhere, simply opening a new Supermon 2 tab. Since SkywarnPlus hinges on the ability to process alerts for several different locations at the same time, there is no good way to hyperlink to the NWS page from an alert title, thus this functionality could not be improved.

Here is the relevant portion of the `ast_var_update.sh` script included with Supermon 2:

```bash
#!/bin/bash

# ****************************************************
# ast_var_update.sh   UPDATE 3                       *
#                                                    *
# This script needs to be run periodically to update *
# variables in Allstar which are used to transfer    *
# data to Supermon2 from local or remote servers     *
# If a server is defined in Allstar this script      *
# would need to be present and run on each server    *
# in order to update the servers CPU temperature,    *
# Uptime, load average, weather, alerts, log file    *
# size and registration status information for the   *
# node information window of each server displayed   *
# in Supermon2. If this script is not running on a   *
# particular server it will just display the data    *
# as empty space but will otherwise work as normal.  *
#                                                    *
# NO SETUP in this script - User setup in file -     *
#     /usr/local/sbin/supermon/node_info.ini         *
#                                                    *
# Recommend that this script be run at least every   *
# 5 minutes with a cron job. Here is an example -    *
#                                                    *
# ****************************************************

#  */5 * * * * /usr/local/sbin/supermon/ast_var_update.sh

# ****************************************************
#                                                    *
#  (C) WA3DSP 12/15/2020                             *
#  Original concept                                  *
#                                                    *
#  Updated 12/19/2020                                *
#   Name changed to ast_var_update.sh                *
#   Added Weather, Alerts, and Log file size         *
#                                                    *   
#  Update 1/2/2021                                   *
#   Added Registrations to node info                 *
#                                                    *
#  Update 1/9/2021                                   *
#     Name changed to ast_var_update.sh              *
#     Added node_info.ini file                       *
#                                                    *
#  Update 1/16/2021                                  *
#     Added check for Hamvoip updates                *
#                                                    *
#  Update 3 - 2/6/2021                               *
#     Corrected log size wording                     *
#     added clickable URL to WX Alert                *
#     Fixed CPU temperature for later kernels        *
# ****************************************************

# Setup in /usr/local/sbin/supermon/node_info.ini
# No user setable parameters in this script
# DO NOT CHANGE LINES below 

source "$script_dir/node_info.ini"
Alert_ini="/usr/local/bin/AUTOSKY/AutoSky.ini"
##############################################
if [ -e /tmp/AUTOSKY/warnings.txt ]; then
    ALERTURL=$(grep "^OFILE=" $Alert_ini | sed 's/OFILE=//' | sed "s/\&y=0/\&y=1/" | sed 's/"//g')
    ALERTURL="<a target='WX ALERT' href=$ALERTURL>"
    ALERT=$(cat /tmp/AUTOSKY/warnings.txt)
    if [ "$ALERT" == "" ]; then
        ALERT="$ALERTURL <span style='color: red;'><b>No Alerts</b></span></a>"
    else
        ALERT="<span style='color: red;'><b>$ALERT</b></span></a>"
        ALERT="$ALERTURL $(echo $ALERT | tr -d "\n\r]" | sed 's/\[//' | sed 's/  \[/,/g')"
    fi
    ALERT="\"$ALERT\""
else
    ALERT="\" \""
fi
```

### SkywarnPlus Integration with Supermon 2 Upgraded
Beginning with SkywarnPlus release [v0.8.0](https://github.com/Mason10198/SkywarnPlus/releases/tag/v0.8.0) (7/21/24), a function was added to emulate the functionality of `ast_var_update.sh` in an enhanced way. This allows proper display of alert information from SkywarnPlus in Supermon 2, without broken hyperlinks.

# Manual Installation
SkywarnPlus is recommended to be installed at the `/usr/local/bin/SkywarnPlus` location on both Debian and Arch systems.

Follow the steps below to install:

1. **Dependencies**

   Install the required dependencies using the following commands:

   1. **Debian 11 and Older (ASL 1 & ASL 2)**

   ```bash
   # EXECUTE ONE LINE AT A TIME
   apt install unzip python3 python3-pip ffmpeg
   pip3 install ruamel.yaml requests python-dateutil pydub
   ```

   2. **Debian 12 and Newer (ASL 3+)**
   
   Beginning around Debian 12 "Bookworm", installing Python packages via `pip` will have Debian throw a fit about package managers and externally managed virtual environments. Use these commands instead on newer distros.

    ```bash
    # EXECUTE ONE LINE AT A TIME
    apt install unzip python3 python3-pip ffmpeg
    apt install python3-ruamel.yaml python3-requests python3-dateutil python3-pydub
    ```

   3. **Arch (HAMVOIP)**

   It is a good idea to first update your HAMVOIP system using **Option 1** in the HAMVOIP menu before installing the dependencies.

   ```bash
   # EXECUTE ONE LINE AT A TIME
   pacman -S ffmpeg
   wget https://bootstrap.pypa.io/pip/3.5/get-pip.py
   python get-pip.py
   pip install requests python-dateutil pydub
   pip install ruamel.yaml==0.15.100
   ```

2. **Download SkywarnPlus**

   Download the latest release of SkywarnPlus from GitHub

   ```bash
   cd /usr/local/bin
   wget https://github.com/Mason10198/SkywarnPlus/releases/latest/download/SkywarnPlus.zip
   unzip SkywarnPlus.zip
   rm SkywarnPlus.zip
   ```

3. **Configure Permissions**

   The scripts must be made executable. Use the chmod command to change the file permissions:

   ```bash
   cd SkywarnPlus
   chmod +x *.py
   ```
   
> [!IMPORTANT]
> **ONLY if you are using AllStarLink (ASL) version 3 or newer**, then you must additionally execute the following commands to allow the `asterisk` user access to SkywarnPlus files.
> ```bash
> chown -R asterisk:asterisk /usr/local/bin/SkywarnPlus/
> chmod -R u+rw /usr/local/bin/SkywarnPlus/
> ```

4. **Crontab Entry**

      1. **ASL1, ASL2, and HamVoIP**

          Add a crontab entry to call SkywarnPlus on an interval **as the `root` user**.

          ```bash
          echo '* * * * * root /usr/local/bin/SkywarnPlus/SkywarnPlus.py' > /etc/cron.d/SkywarnPlus
          ```
    
    1. **ASL3**

        Add a crontab entry to call SkywarnPlus on an interval **as the `asterisk` user**

        ```bash
        echo '* * * * * asterisk /usr/local/bin/SkywarnPlus/SkywarnPlus.py' > /etc/cron.d/SkywarnPlus
        ```

   This command will execute SkywarnPlus (poll NWS API for data) every 60 seconds. For slower systems, or systems with several counties and/or advanced configurations, the interval may need to be increased.

# Testing

SkywarnPlus provides the ability to inject predefined alerts, bypassing the call to the NWS API. This feature is extremely useful for testing SkywarnPlus.

To enable injection, modify the following settings in the `[DEV]` section of your `config.yaml` file:

```yaml
  # Enable test alert injection instead of calling the NWS API by setting 'INJECT' to 'True'.
  INJECT: false

  # List the test alerts to inject. Alert titles are case sensitive.
  # Optionally specify the CountyCodes and/or EndTime for each alert.
  # CountyCodes used here must be defined at the top of this configuration file.
  # Example:
  # INJECTALERTS:
  #   - Title: "Tornado Warning"
  #     CountyCodes: ["ARC119", "ARC120"]
  #   - Title: "Tornado Watch"
  #     CountyCodes: ["ARC125"]
  #     EndTime: "2023-08-01T12:00:00Z"
  #   - Title: "Severe Thunderstorm Warning"
  INJECTALERTS:
  - Title: "Tornado Warning"
  - Title: "Tornado Watch"
  - Title: "Severe Thunderstorm Warning"
```

# Debugging

Debugging is an essential part of diagnosing issues with SkywarnPlus. To facilitate this, SkywarnPlus provides a built-in debugging feature. Here's how to use it:

1. **Enable Debugging**: The debugging feature can be enabled in the `config.yaml` file. Open this file and set the `debug` option under the `[SkywarnPlus]` section to `true`.

```yaml
Logging:
  # Configuration for logging options.
  # Enable verbose logging by setting 'Debug' to 'True'.
  Debug: false
```

This will allow the program to output detailed information about its operations, which is helpful for identifying any issues or errors.

2. **Open an Asterisk Console**: While debugging SkywarnPlus, it's helpful to have an Asterisk console open in a separate terminal window. This allows you to observe any issues related to Asterisk, such as problems playing audio files.

You can open an Asterisk console with the following command:

```bash
asterisk -rvvv
```

This command will launch an Asterisk console with a verbose output level of 3 (`vvv`), which provides a detailed look at what Asterisk is doing. This can be particularly useful if you're trying to debug issues with audio playback.

3. **Analyze Debugging Output**: With debugging enabled in SkywarnPlus and the Asterisk console open, you can now run SkywarnPlus and observe the detailed output in both terminals. This information can be used to identify and troubleshoot any issues or unexpected behaviors.

Remember, the more detailed your debug output is, the easier it will be to spot any issues. However, please be aware that enabling debug mode can result in large amounts of output, so it should be used judiciously.

If you encounter any issues that you're unable to resolve, please don't hesitate to submit a detailed bug report on the [SkywarnPlus GitHub Repository](https://github.com/mason10198/SkywarnPlus).

# Maintenance and Bug Reporting

SkywarnPlus is actively maintained by a single individual who dedicates their spare time to improve and manage this project. Despite best efforts, the application may have some bugs or areas for improvement.

If you encounter any issues with SkywarnPlus, please check back to the [SkywarnPlus GitHub Repository](https://github.com/mason10198/SkywarnPlus) to see if there have been any updates or fixes since the last time you downloaded it. New commits are made regularly to enhance the system's performance and rectify any known issues.

Bug reporting is greatly appreciated as it helps to improve SkywarnPlus. If you spot a bug, please raise an issue in the GitHub repository detailing the problem. Include as much information as possible, such as error messages, screenshots, and steps to reproduce the issue. This will assist in quickly understanding and resolving the issue.

Thank you for your understanding and assistance in making SkywarnPlus a more robust and reliable system for all.

# Contributing

SkywarnPlus is open-source and welcomes contributions. If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

If the spare time I put into the development of SkywarnPlus has helped you, please consider supporting!

<p align="center"><a href="https://www.paypal.com/donate/?business=93AJFB9BAVSJL&no_recurring=0&item_name=Thank+you+so+much+for+your+support%21+I+put+a+lot+of+my+spare+time+into+this%2C+and+I+sincerely+appreciate+YOU%21&currency_code=USD"><img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" width=300px alt="Donate with PayPal"/></a></p>

# Frequently Asked Questions

### I just installed SkywarnPlus on my HamVoIP node, why is it giving me errors?
HamVoIP uses a very outdated version of Python which can cause some issues that ASL users do not experience. Carefully follow the installation inctructions line-by-line (do not copy/paste all commands at once) and try again.

### Why do I see depreciation warnings when installing SkywarnPlus on my HamVoIP node?
HamVoIP uses a very outdated version of Python, and Python will display warnings asking you to update it. Unfortunately, Python cannot be upgraded on HamVoIP and these warnings must be ignored.

### Can I change the crontab interval to something other than 60 seconds?
Yes! You can run SkywarnPlus as frequently or infrequently as you wish. Be aware, whatever you set the interval to (X), there will be a delay of "up to" X minutes between the time an alert is issued by the NWS, and the time that SWP announces it.

### What does "with multiples" mean?
The "multiples" flag informs the listener that there is more than one unique instance of the given alert type in the county/counties you defined in the configuration. For example, a config file with 2x counties defined, and a unique Tornado Warning in each county.

### Why is SkywarnPlus saying the same thing every 60 seconds?
You probably have the `CLEANSLATE` developer option enabled in the `config.yaml` file by accident.

### I just installed SkywarnPlus, why don't I hear anything?
Assuming you installed it correctly, SkywarnPlus will not do anything until it detects alerts provided by the NWS.

### There is an active alert in my area, but SkywarnPlus isn't doing anything. What gives?
It is very likely that the alert is not technically active yet in your area, and SkywarnPlus is holding off on announcing that alert until it is imminent. Please see the [TimeType Configuration](#timetype-configuration) section for more information. When in doubt, you can verity the exact data being provided by the NWS API, and whether an alert is currently EFFECTIVE or ONSET, by visiting the API endpoing in the following format:
```
https://api.weather.gov/alerts/active?zone=YOUR_COUNTY_CODE_HERE
```

### Why aren't my test alerts working?
Make sure you're injecting alerts with the correct format, shown in the [Testing](#testing) section.

### Can SkywarnPlus automatically read the full alert description?
Yes! You can use [AlertScript](#alertscript) to automcatially trigger [SkyDescribe](#skydescribe) whenever specific alerts are detected.

# License

SkywarnPlus is open-sourced software licensed under the [GPL-3.0 license](LICENSE).

Created by Mason Nelson (N5LSN/WRKF394)

Audio Library voiced by Rachel Nelson (N5LSN/WRKF394 XYL)

Skywarn® and the Skywarn® logo are registered trademarks of the National
Oceanic and Atmospheric Administration, used with permission.
