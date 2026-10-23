#!/usr/bin/env python3
"""
Overnight Snapchat Score Bot Runner
- Runs until specified stop time
- Anti-detection: random delays, periodic breaks
- Logs progress and can be safely stopped
"""

import subprocess
import sys
import os
import time
import random
from datetime import datetime, timedelta

# Configuration
STOP_HOUR = 10  # Stop at 10 AM local time
STOP_MINUTE = 0
MIN_DELAY_BETWEEN_ROUNDS = 3  # seconds
MAX_DELAY_BETWEEN_ROUNDS = 8
BREAK_EVERY_N_ROUNDS = random.randint(40, 60)  # Take a break every 40-60 rounds
BREAK_MIN_SECONDS = 120  # 2 min
BREAK_MAX_SECONDS = 300  # 5 min

# Import the bot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snapscore import SnapScore, select_device

def should_stop():
    """Check if we've reached stop time."""
    now = datetime.now()
    stop_time = now.replace(hour=STOP_HOUR, minute=STOP_MINUTE, second=0, microsecond=0)

    # If stop time is earlier today, it means stop tomorrow
    if stop_time <= now:
        stop_time += timedelta(days=1)

    return now >= stop_time

def log_status(msg):
    """Log with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

def main():
    log_status("="*50)
    log_status("Overnight Snapchat Score Bot Started")
    log_status(f"Will stop at {STOP_HOUR}:{STOP_MINUTE:02d} AM")
    log_status("="*50)

    device = select_device()
    bot = SnapScore(device)

    count = 0
    failures = 0
    rounds_until_break = BREAK_EVERY_N_ROUNDS

    while not should_stop():
        try:
            # Check if it's time for a break
            if rounds_until_break <= 0:
                break_time = random.randint(BREAK_MIN_SECONDS, BREAK_MAX_SECONDS)
                log_status(f"Taking a {break_time//60}m {break_time%60}s break to appear human...")
                time.sleep(break_time)
                rounds_until_break = random.randint(40, 60)
                log_status("Break over, resuming...")

            # Find starting screen
            screen = bot.find_start()
            if screen is None:
                log_status("Couldn't get to camera - retrying...")
                failures += 1
                if failures >= 5:
                    log_status("Too many failures, taking a long break...")
                    time.sleep(300)  # 5 min break
                    failures = 0
                continue

            # Take and send snap
            if screen == "camera":
                bot.tap((539, 1902))  # SHUTTER_CORD

            from snapscore import SEND_TO_CORD, SHORTCUT_CORD, SEND_GRP_CORD, FIRST_FRIEND_CORD

            bot.tap(SEND_TO_CORD)
            bot.tap(SHORTCUT_CORD)

            if not bot.shortcut_selected():
                log_status("Shortcut not selected - skipping round")
                failures += 1
                time.sleep(random.uniform(2, 4))
                continue

            # Find Select All button dynamically from screenshot
            select_all_coord = bot.find_select_all_button()
            bot.tap(select_all_coord)
            time.sleep(1.5)  # Wait for all friends to be selected

            how = "select_all"

            if not bot.ready_to_send():
                log_status("Selection wrong - skipping round")
                failures += 1
                time.sleep(random.uniform(2, 4))
                continue

            bot.tap(SEND_GRP_CORD)
            count += 1
            failures = 0
            rounds_until_break -= 1
            bot.log(count, how)
            log_status(f"Sent #{count} ({how}) - next break in {rounds_until_break} rounds")

            # Random delay between rounds
            delay = random.uniform(MIN_DELAY_BETWEEN_ROUNDS, MAX_DELAY_BETWEEN_ROUNDS)
            time.sleep(delay)

        except KeyboardInterrupt:
            log_status(f"Stopped by user. Total sent: {count}")
            break
        except Exception as e:
            log_status(f"Error: {e}")
            failures += 1
            time.sleep(5)

    log_status("="*50)
    log_status(f"Session complete! Total snaps sent: {count}")
    log_status("="*50)

if __name__ == "__main__":
    main()
