# Complete Setup Guide - SnapScore Pixel

This is a step-by-step guide to get SnapScore working on your phone.

## ✅ Prerequisites Checklist

- [ ] Android phone (Pixel 7 recommended)
- [ ] USB cable
- [ ] Computer with Python 3.8+
- [ ] Snapchat app installed on phone
- [ ] Snapchat account logged in

---

## Step 1: Enable USB Debugging on Your Phone

### What is USB Debugging?
USB Debugging allows your computer to communicate with your Android phone via ADB.

### How to Enable

1. **Go to Settings**
2. **Scroll down and tap "About Phone"** (or "Phone Info")
3. **Find "Build Number"**
4. **Tap "Build Number" 7 times** until you see a message like "You are now a developer"
5. **Go back to Settings**
6. **Scroll down and tap "Developer Options"** (now visible)
7. **Find "USB Debugging" and toggle it ON**
8. **A permission dialog will appear - tap "Allow"**

✅ USB Debugging is now enabled!

---

## Step 2: Install Android Platform Tools

### Windows

1. Download from: https://developer.android.com/tools/releases/platform-tools
2. Extract the ZIP file (example: `C:\Users\YourName\Downloads\platform-tools`)
3. **Add to PATH:**
   - Search for "Environment Variables" in Windows search
   - Click "Edit the system environment variables"
   - Click "Environment Variables..." button
   - Under "System variables", find and click "Path"
   - Click "New" and add: `C:\Users\YourName\Downloads\platform-tools`
   - Click "OK" on all dialogs
   - **Restart your computer**

4. **Verify installation:**
   ```bash
   adb version
   ```

### Mac

```bash
# Install via Homebrew
brew install android-platform-tools

# Verify
adb version
```

### Linux

```bash
# Ubuntu/Debian
sudo apt-get install android-tools-adb

# Verify
adb version
```

---

## Step 3: Connect Your Phone

1. **Connect your phone to computer with USB cable**
2. **On your phone, you'll see a permission dialog:**
   - Tap "Allow" to allow USB debugging from this computer
   - Check "Always allow from this computer"
3. **On your computer, verify connection:**
   ```bash
   adb devices
   ```
   You should see your device listed like:
   ```
   List of attached devices
   100.111.3.63:5555    device
   ```

✅ Phone is connected!

---

## Step 4: Clone and Setup SnapScore

### Clone the Repository

```bash
# Navigate to where you want to save the project
cd ~/Documents  # or your preferred location

# Clone the repo
git clone https://github.com/MatthewMacri/snapchat-score-bot.git
cd snapchat-score-bot
```

### Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

✅ SnapScore is installed!

---

## Step 5: Create a Snapchat Shortcut

This is the group of friends you'll send snaps to.

1. **Open Snapchat**
2. **Tap "Send To"** (paper airplane icon)
3. **Look for the tabs at the top:** "All", emoji shortcuts, "New Friends", "New +"
4. **Tap the "New +" button** to create a new shortcut
5. **Add your friends:**
   - Search and tap each friend
   - Check the box next to their name
6. **Tap "Create"**
7. **Choose an emoji** for this shortcut (you'll see emoji options)
8. **Tap "Done"**

### Important!
⚠️ The shortcut you create **MUST be the FIRST shortcut** (right after "All" tab)

Verify:
- Close Snapchat
- Reopen it
- Go to Send To
- Your emoji shortcut should be the first chip after "All"

✅ Shortcut is ready!

---

## Step 6: Test the Connection

Before running the full bot, test that everything works:

```bash
# Make sure your virtual environment is activated
# (you should see "(venv)" at the start of your command line)

# Test with just 1 snap
python snapscore.py 1
```

Watch your phone. The bot should:
1. Take a snap
2. Tap "Send To"
3. Select your emoji shortcut
4. Click "Select All"
5. Send to all friends in the shortcut

If this works → ✅ **You're ready to run the full bot!**

If it fails → See [Troubleshooting](#troubleshooting) section

---

## Step 7: Run the Bot

### Quick Run (400 snaps)

```bash
python snapscore.py
```

The bot will:
- Send 400 snaps automatically
- Log each one to `snapscore_log.csv`
- Take about 80 minutes (12 seconds per snap)
- Stop if 3 snaps fail in a row

### Custom Count

```bash
python snapscore.py 100    # 100 snaps
python snapscore.py 200    # 200 snaps
```

### Overnight Mode

```bash
python run_overnight.py
```

The bot will:
- Start sending immediately
- Take random breaks (2-5 min every 50 snaps)
- Stop at 6 AM (configurable)
- Resume the next day

### Stop the Bot

Press **Ctrl+C** at any time to stop

---

## 📊 Check Your Results

After running, check `snapscore_log.csv`:

```csv
time,round,selected_by
2026-10-23 16:10:17,1,select_all
2026-10-23 16:10:39,2,select_all
2026-10-23 16:11:00,3,select_all
```

Count the rows = number of snaps sent ✅

---

## 🆘 Troubleshooting

### Problem: "No devices found"

**Error message:** `List of attached devices` shows nothing

**Solutions:**
1. Unplug phone and replug it
2. Verify USB Debugging is enabled (Settings → Developer Options)
3. Try a different USB cable
4. Restart your phone
5. On computer, run:
   ```bash
   adb kill-server
   adb start-server
   adb devices
   ```

### Problem: "Device not found" after connecting

1. Check your phone's screen - there might be a permission dialog
2. Tap "Allow" and check "Always allow"
3. Run `adb devices` again

### Problem: Bot clicks the wrong thing

1. Take a screenshot:
   ```bash
   adb exec-out screencap -p > screenshot.png
   ```
2. Open the screenshot and compare with your screen
3. If layout is different:
   - Your phone model or Snapchat version differs
   - You need to recalibrate coordinates (advanced)
   - Open an issue on GitHub with screenshot

### Problem: Bot says "Shortcut not selected"

**This means:**
- Bot couldn't find your emoji shortcut in the expected position
- The shortcut isn't blue/selected

**Fix:**
1. Make sure the emoji shortcut is the FIRST one after "All"
2. You didn't create a new shortcut properly
3. Try creating a new shortcut and moving it to the first position

### Problem: "Selection looks wrong" message

**This means:**
- Bot detected something odd before sending
- Examples:
  - Someone got deselected
  - Layout changed
  - Screen didn't update

**What happens:**
- Bot skips that round (doesn't send)
- No snap wasted ✅

**Why:**
- This is a safety feature!
- Better to skip one snap than send to the wrong place

**Fix:**
- Usually clears itself next round
- If persistent, restart bot

### Problem: Very slow cycle time (>20 seconds)

**Possible causes:**
- Phone storage is full
- Too many apps running
- Snapchat is laggy
- Network issues

**Solutions:**
- Close other apps
- Clear phone storage (delete old videos, etc.)
- Restart phone
- Restart Snapchat

### Problem: Bot keeps restarting Snapchat

**This happens when:**
- Navigation failed
- Unexpected dialog appeared
- Screen layout changed unexpectedly

**Why:**
- Bot is being safe
- Better to restart app than get lost in wrong screen

**Fix:**
- Wait and let it retry (bot is designed for this)
- If persistent, check if Snapchat layout changed
- Take screenshot and check against expected screens

---

## ⚙️ Configuration

### Change Bot Settings

Edit `run_overnight.py` to customize:

```python
# When to start/stop
START_HOUR = 12      # Noon (24-hour format)
STOP_HOUR = 6        # 6 AM next day

# Delays between snaps
MIN_DELAY_BETWEEN_ROUNDS = 3   # seconds
MAX_DELAY_BETWEEN_ROUNDS = 8   # seconds

# When to take breaks
BREAK_EVERY_N_ROUNDS = 50       # Take break after 50 snaps
BREAK_MIN_SECONDS = 120         # 2 min
BREAK_MAX_SECONDS = 300         # 5 min
```

---

## 📈 Monitor Progress

### Real-time Monitoring

While bot is running, you can:

1. **Watch your phone** - see it working
2. **Check Snapchat score** - it updates every few minutes
3. **Monitor `snapscore_log.csv`** - see new entries being added

### After Running

```bash
# Count total snaps sent
wc -l snapscore_log.csv

# Check timestamp of last snap
tail -1 snapscore_log.csv

# Calculate points per snap
# (Final Score - Initial Score) / Total Snaps
```

---

## 🎯 Best Practices

1. **Don't use phone while bot runs** - Let it work undisturbed
2. **Keep Snapchat in foreground** - Don't switch apps
3. **Keep phone unlocked** - Bot needs screen access
4. **Stable surface** - Don't move phone around
5. **Good lighting** - Bot reads screen pixels (lighting matters!)
6. **Close notifications** - Unexpected popups could interfere

---

## 🔒 Important Reminders

⚠️ **This violates Snapchat's Terms of Service**
- Use at your own risk
- Your account could be banned
- Snapchat may detect automation

✅ **Only use responsibly:**
- Get friends' consent first
- Don't spam people
- Understand account risk

---

## 🎉 You're Ready!

You should now be able to run SnapScore! Start with:

```bash
python snapscore.py 10   # Test with 10 snaps first
```

Then when confident:

```bash
python snapscore.py 400  # Full 400 snap run
```

---

## 📞 Need Help?

1. **Check this guide** - Most issues are covered above
2. **Check README.md** - Has troubleshooting section
3. **Open a GitHub Issue** - Include:
   - Phone model
   - Snapchat version
   - Error message
   - Screenshot if possible

---

**Good luck! May your Snapchat score reach the clouds! 🚀**
