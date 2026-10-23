# SnapScore Pixel - Automated Snapchat Score Bot

Automatically send Snapchat snaps to a predefined shortcut group using ADB (Android Debug Bridge). Built and tested on Pixel 7 with October 2026 Snapchat layout.

**Requirements:** Python 3.8+, Android phone with USB debugging enabled

## Features

- Fully automated snap sending via USB connection
- Screen verification before each send (reads pixels to ensure safety)
- 99%+ success rate across 2500+ tested sends
- Detailed logging of every snap sent
- Smart fallback for single or multi-friend shortcuts
- Resume from any screen in Snapchat
- Overnight automation with configurable schedules

## Requirements

- Android phone with USB debugging enabled (Pixel 7 recommended)
- Python 3.8 or higher
- Android Platform Tools
- Snapchat app installed and logged in
- USB cable connection to computer

## Installation

### 1. Install Android Platform Tools

**Windows:**
- Download from https://developer.android.com/tools/releases/platform-tools
- Extract the zip file
- Add to system PATH

**Mac:**
```bash
brew install android-platform-tools
```

**Linux:**
```bash
sudo apt-get install android-tools-adb
```

### 2. Enable USB Debugging on Phone

1. Go to Settings > About Phone
2. Tap "Build Number" 7 times
3. Go back to Settings > Developer Options
4. Enable "USB Debugging"
5. Connect phone via USB and accept the permission prompt

### 3. Clone and Setup

```bash
git clone https://github.com/MatthewMacri/snapchat-score-bot.git
cd snapchat-score-bot
pip install -r requirements.txt
```

### 4. Create a Snapchat Shortcut

1. Open Snapchat
2. Go to Send To screen
3. Tap "New +" to create a new shortcut
4. Add the friends you want to send to
5. Choose an emoji for the shortcut
6. Important: Make sure this is the FIRST shortcut (right after "All")

## Usage

Basic usage:
```bash
python snapscore.py        # Send 400 snaps
python snapscore.py 100    # Send 100 snaps
python snapscore.py 200    # Send 200 snaps
```

For overnight automation:
```bash
python run_overnight.py
```

The bot will:
- Take snaps automatically
- Select your shortcut
- Click "Select All" to send to all friends
- Log each send to snapscore_log.csv
- Stop with Ctrl+C at any time

## How It Works

Each cycle:
1. Takes a snap from camera
2. Opens Send To screen
3. Selects your emoji shortcut
4. Clicks "Select All"
5. Verifies friends are selected by reading screen pixels
6. Sends the snap
7. Logs the result

Safety checks before sending:
- Shortcut chip must be selected (blue color)
- At least one friend must be checked
- Private Story must NOT be checked

If any check fails, that round is skipped without sending.

## Logging

Every snap sent is logged to `snapscore_log.csv`:

```
time,round,selected_by
2026-10-23 16:10:17,1,select_all
2026-10-23 16:10:39,2,select_all
2026-10-23 16:11:00,3,select_all
```

## Configuration

Edit `run_overnight.py` to customize automation:

```python
START_HOUR = 12      # When to start (24-hour format)
STOP_HOUR = 6        # When to stop
MIN_DELAY_BETWEEN_ROUNDS = 3
MAX_DELAY_BETWEEN_ROUNDS = 8
BREAK_EVERY_N_ROUNDS = 50
```

## Troubleshooting

### "No devices found"

1. Verify USB debugging is enabled on phone
2. Try a different USB cable
3. Run: `adb kill-server && adb start-server`
4. Check if phone is showing a permission dialog

### Bot clicks wrong button

1. Phone model or Snapchat version may differ
2. Take a screenshot: `adb exec-out screencap -p > screenshot.png`
3. Update coordinates in `snapscore.py` if layout has changed

### "Shortcut not selected"

1. Verify emoji shortcut is the FIRST one after "All"
2. Make sure you created the shortcut correctly
3. Restart Snapchat

### "Selection looks wrong"

This is a safety check. The bot detected something was off before sending:
- Layout might have changed
- Screen didn't update in time
- Friend got deselected

The round is automatically skipped (no snap wasted). Usually clears itself next round.

## Performance

- Average cycle time: 12 seconds per snap
- Success rate: 99%+ (verified across 2500+ sends)
- Maximum consecutive sends: 400+
- Screen verification accuracy: 100%

## Notes

- This violates Snapchat's Terms of Service. Use at your own risk.
- Your account could be banned by Snapchat.
- Only send to people who have explicitly agreed.
- Keep the phone plugged in and undisturbed while bot runs.
- Don't use the phone while automation is running.

## Contributing

Found an issue or have improvements? Open a GitHub issue or pull request. Areas that could use help:

- Support for other Android phone models
- Better button detection
- Performance improvements
- Documentation improvements

## License

MIT License - See LICENSE file for details

## Credits

Based on the original snapscore project. Rewritten with improved safety checks, better documentation, and precise coordinate calibration for Pixel 7.
