# SystemD Timer Migration

## Overview

SkywarnPlus has been fully migrated from cron-based scheduling to systemd timers. This provides better logging, more precise scheduling, improved reliability, and modern Linux integration.

## What Changed

### 1. SystemD Unit Files
- **`systemd/skywarnplus.service`** - Main service unit for running SkywarnPlus
- **`systemd/skywarnplus.timer`** - Timer unit for automatic execution every minute
- **`asl3-supermon-workaround.service`** - Service for ASL3 Supermon compatibility
- **`asl3-supermon-workaround.timer`** - Timer for ASL3 Supermon workaround

### 2. Installation Script
- **`swp-install`** - Completely updated to use systemd
  - Removes old cron entries automatically
  - Installs and configures systemd timers
  - Handles ASL3 Supermon workaround with systemd
  - Configurable timer intervals during installation

### 3. SkyControl Enhancements
- **New `timer` command** for systemd timer management
- Available actions:
  - `status` - Check timer status
  - `start` - Start the timer
  - `stop` - Stop the timer
  - `restart` - Restart the timer
  - `enable` - Enable timer on boot
  - `disable` - Disable timer from boot
  - `logs` - View recent logs
  - `list` - List all systemd timers

### 4. Documentation
- **README.md** - Added comprehensive systemd timer documentation
- Included management commands and examples
- Added DTMF command examples for timer control
- Documented advantages over cron

## Installation

### New Installations
Simply run the automated installer:
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Mason10198/SkywarnPlus/main/swp-install)"
```

The installer will automatically:
1. Detect systemd availability
2. Install systemd timer files
3. Configure timer interval
4. Enable and start the timer

### Upgrading Existing Installations
The upgrade process will automatically:
1. Remove old cron entries
2. Install new systemd timers
3. Preserve your configuration
4. Start the new timers

## Usage

### Basic Timer Management
```bash
# Check timer status
python3 skycontrol.py timer status

# View logs
python3 skycontrol.py timer logs
journalctl -u skywarnplus.service -f

# Restart timer
python3 skycontrol.py timer restart

# Stop timer temporarily
python3 skycontrol.py timer stop

# Start timer again
python3 skycontrol.py timer start
```

### SystemD Commands
```bash
# Check timer status
systemctl status skywarnplus.timer

# View all timers
systemctl list-timers

# View service logs
journalctl -u skywarnplus.service

# Follow logs in real-time
journalctl -u skywarnplus.service -f

# View logs from last hour
journalctl -u skywarnplus.service --since "1 hour ago"
```

### Manual Service Execution
To manually run SkywarnPlus immediately:
```bash
# Run the service once
systemctl start skywarnplus.service

# Or run directly
python3 /usr/local/bin/SkywarnPlus/main.py
```

## Configuration Files

### Service File Location
`/etc/systemd/system/skywarnplus.service`

### Timer File Location
`/etc/systemd/system/skywarnplus.timer`

### Modifying Timer Interval
To change the timer interval:

1. Edit the timer file:
```bash
nano /etc/systemd/system/skywarnplus.timer
```

2. Change the `OnCalendar` line:
```ini
# Every minute (default)
OnCalendar=*:*:00

# Every 5 minutes
OnCalendar=*:0/5

# Every 10 minutes
OnCalendar=*:0/10

# Every 2 minutes
OnCalendar=*:0/2
```

3. Reload and restart:
```bash
systemctl daemon-reload
systemctl restart skywarnplus.timer
```

## Advantages Over Cron

### 1. Better Logging
- All output goes to systemd journal
- Centralized logging with `journalctl`
- Structured log format
- Easy filtering and searching

### 2. More Precise Scheduling
- Sub-second accuracy vs cron's minute precision
- RandomizedDelaySec to prevent API load spikes
- AccuracySec for fine-tuned timing

### 3. Dependency Management
- Can wait for network availability
- Service dependencies
- Proper startup ordering

### 4. Persistent Execution
- Catches up missed runs if system was down
- `Persistent=true` ensures no missed checks

### 5. Resource Management
- Built-in timeout handling
- Security restrictions (ProtectSystem, PrivateTmp)
- Resource limits

### 6. Centralized Management
- Use `systemctl` for all operations
- Consistent interface across services
- Better integration with system monitoring

## Troubleshooting

### Timer Not Running
```bash
# Check if timer is enabled
systemctl is-enabled skywarnplus.timer

# Check timer status
systemctl status skywarnplus.timer

# Enable if not enabled
systemctl enable skywarnplus.timer
systemctl start skywarnplus.timer
```

### Service Failing
```bash
# Check service status
systemctl status skywarnplus.service

# View recent errors
journalctl -u skywarnplus.service -n 50

# View logs with priority
journalctl -u skywarnplus.service -p err
```

### Checking Next Run Time
```bash
# List all timers with next run time
systemctl list-timers

# Specific timer info
systemctl list-timers skywarnplus.timer
```

### Manual Test Run
```bash
# Run service manually to test
systemctl start skywarnplus.service

# Check if it completed successfully
systemctl status skywarnplus.service
```

## Migration Notes

### Automatic Migration
The installation script automatically handles migration:
- Detects old cron entries
- Removes `/etc/cron.d/SkywarnPlus`
- Removes ASL3 Supermon cron files
- Installs systemd timers
- Preserves configuration

### SystemD Requirement
SkywarnPlus now requires systemd for automatic execution. If systemd is not available:
- Manual execution is still possible
- Run `python3 main.py` manually as needed
- Consider upgrading to a modern Linux distribution

## ASL3 Supermon Integration

For ASL3 systems, a separate systemd timer handles the Supermon workaround:
```bash
# Check ASL3 Supermon timer
systemctl status asl3-supermon-workaround.timer

# View logs
journalctl -u asl3-supermon-workaround.service
```

## Support

For issues or questions:
1. Check logs: `journalctl -u skywarnplus.service`
2. Verify timer status: `systemctl status skywarnplus.timer`
3. Check configuration: `nano /usr/local/bin/SkywarnPlus/config.yaml`
4. Open an issue on GitHub

## Additional Resources

- [systemd.service documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [systemd.timer documentation](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)
- [journalctl documentation](https://www.freedesktop.org/software/systemd/man/journalctl.html)

