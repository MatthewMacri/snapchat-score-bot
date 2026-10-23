# Setup Guide - SnapScore Pixel

Step-by-step instructions to get SnapScore working on your phone.

## Prerequisites

- Android phone (Pixel 7 recommended)
- USB cable
- Computer with Python 3.8+
- Snapchat app installed
- Snapchat account logged in

## Step 1: Enable USB Debugging

1. Go to Settings
2. Scroll down and tap "About Phone" (or "Phone Info")
3. Find "Build Number" 
4. Tap "Build Number" 7 times until you see a developer message
5. Go back to Settings
6. Scroll down and tap "Developer Options" (now visible)
7. Find "USB Debugging" and toggle it ON
8. A permission dialog will appear - tap "Allow"

USB Debugging is now enabled.

## Step 2: Install Android Platform Tools

### Windows

1. Download from: https://developer.android.com/tools/releases/platform-tools
2. Extract the ZIP file (example: C:\Users\YourName\Downloads\platform-tools)
3. Add to PATH:
   - Search for "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables..." button
   - Under "System variables", find "Path"
   - Click "New" and add the path to platform-tools
   - Click OK and restart your computer

4. Verify:
   ```
   adb version
   ```

### Mac

```bash
brew install android-platform-tools
adb version
```

### Linux

```bash
sudo apt-get install android-tools-adb
adb version
```

## Step 3: Connect Your Phone

1. Connect phone to computer with USB cable
2. On your phone, accept the "Allow USB debugging" permission
3. On your computer, verify connection:
   ```
   adb devices
   ```
   You should see your device listed.

## Step 4: Clone and Install

```bash
cd ~/Documents  # or your preferred location
git clone https://github.com/MatthewMacri/snapchat-score-bot.git
cd snapchat-score-bot

# Create virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Create a Snapchat Shortcut

1. Open Snapchat
2. Tap "Send To" (paper airplane icon)
3. Look for the tabs at the top: "All", emoji shortcuts, "New Friends", "New +"
4. Tap "New +" to create a new shortcut
5. Add your friends by tapping their names
6. Tap "Create"
7. Choose an emoji for this shortcut
8. Tap "Done"

Important: This shortcut MUST be the first one (right after "All" tab).

## Step 6: Test

Before running the full bot, test with 1 snap:

```bash
python snapscore.py 1
```

Watch your phone. The bot should:
1. Take a snap
2. Tap "Send To"
3. Select your shortcut
4. Click "Select All"
5. Send to all friends

If this works, you're ready for the full bot.

## Step 7: Run the Bot

```bash
python snapscore.py        # 400 snaps (default)
python snapscore.py 100    # 100 snaps
python snapscore.py 200    # 200 snaps
```

Press Ctrl+C at any time to stop.

## Check Results

After running, check `snapscore_log.csv` to see all snaps sent:

```bash
# Count total rows sent
wc -l snapscore_log.csv
```

## Common Issues

### "No devices found"
- Unplug and reconnect phone
- Verify USB Debugging is enabled
- Try a different USB cable
- Restart phone and computer

### Bot clicks wrong button
- Your phone model or Snapchat version may differ
- Take a screenshot: `adb exec-out screencap -p > screenshot.png`
- Check if layout matches expected
- Update coordinates if needed

### "Shortcut not selected"
- Make sure emoji shortcut is the FIRST one after "All"
- Try creating a new shortcut
- Restart Snapchat

## Best Practices

1. Don't use phone while bot runs
2. Keep Snapchat in foreground
3. Keep phone unlocked
4. Stable surface (don't move phone)
5. Good lighting helps (bot reads screen)
6. Close notifications if possible

## Next Steps

For overnight automation:
```bash
python run_overnight.py
```

Edit `run_overnight.py` to change start/stop times and break settings.

For more info, see README.md or CONTRIBUTING.md.
