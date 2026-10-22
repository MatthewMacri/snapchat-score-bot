"""Send blank snaps to a Snapchat Shortcut over ADB, from a real Android phone.

Usage:
    python snapscore.py            # 400 rounds
    python snapscore.py 100        # 100 rounds
Stop any time with Ctrl+C. Every sent round is logged to snapscore_log.csv.
"""
from ppadb.client import Client as AdbClient
import os
import struct
import subprocess
import time
import sys

# Pixel 7 (1080x2400), Snapchat layout as of Oct 2026
SHUTTER_CORD = (539, 1902)        # camera screen
SEND_TO_CORD = (877, 2237)        # preview screen, blue "Send To" button
SHORTCUT_CORD = (206, 350)        # Send To screen, shortcut chip
SHORTCUT_CHECK_CORD = (165, 350)  # inside the chip; blue only when it is selected
SELECT_ALL_CORD = (923, 746)      # "Select All" next to the "Send To" heading in the shortcut view
FIRST_FRIEND_CORD = (966, 874)    # first friend's tick circle; used when the shortcut has one person and no Select All
SEND_BAR_CHECK_CORD = (300, 2256) # bottom send bar; only shown once someone is ticked
PRIVATE_STORY_CHECK_CORD = (966, 614)  # Private Story tick circle; must stay unticked
SEND_GRP_CORD = (1003, 2256)      # send arrow

# Without the shortcut selected, SELECT_ALL_CORD lands on the "My Story" rows,
# so exp_snaps refuses to tap it unless the chip is blue.
SELECTED_BLUE = (1, 54, 106)
SEND_BAR_BLUE = (15, 173, 255)
WHITE = (255, 255, 255)

# Used to work out which screen Snapchat is on, so a round can start from anywhere.
SHUTTER_RING_CHECK_CORDS = [(426, 1902), (653, 1902), (539, 1790), (539, 2017)]  # white ring = camera
PREVIEW_SEND_TO_CHECK_CORD = (720, 2237)  # blue "Send To" button on the preview screen
PREVIEW_STORIES_CHECK_CORD = (300, 2237)  # gray "Stories" button beside it (blue on the Send To screen)
SNAPCHAT_PACKAGE = "com.snapchat.android"
ADB_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Android\platform-tools\adb.exe")
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapscore_log.csv")


class SnapScore:
    def __init__(self, device):
        self.device = device

    def tap(self, point):
        self.device.shell(f'input touchscreen tap {point[0]} {point[1]}')
        time.sleep(1)

    def screenshot(self):
        return subprocess.run([ADB_PATH, "-s", self.device.serial, "exec-out", "screencap"],
                              capture_output=True).stdout

    def matches(self, point, color, shot=None):
        raw = shot or self.screenshot()
        width = struct.unpack_from("<I", raw, 0)[0]
        offset = 16 + (point[1] * width + point[0]) * 4
        return all(abs(a - b) <= 12 for a, b in zip(raw[offset:offset + 3], color))

    def shortcut_selected(self):
        return self.matches(SHORTCUT_CHECK_CORD, SELECTED_BLUE)

    def ready_to_send(self):
        # someone is ticked, and it isn't the Private Story
        shot = self.screenshot()
        return self.matches(SEND_BAR_CHECK_CORD, SEND_BAR_BLUE, shot) and \
            not self.matches(PRIVATE_STORY_CHECK_CORD, SEND_BAR_BLUE, shot)

    def current_screen(self):
        shot = self.screenshot()
        if all(self.matches(p, WHITE, shot) for p in SHUTTER_RING_CHECK_CORDS):
            return "camera"
        if self.matches(PREVIEW_SEND_TO_CHECK_CORD, SEND_BAR_BLUE, shot) and \
                not self.matches(PREVIEW_STORIES_CHECK_CORD, SEND_BAR_BLUE, shot):
            return "preview"
        return None

    def find_start(self):
        # Back out of whatever is open (chat, Send To, ...); if that doesn't
        # reach the camera or a ready snap, reopen Snapchat and try again.
        for attempt in range(8):
            screen = self.current_screen()
            if screen:
                return screen
            if attempt in (3, 6):
                self.device.shell(f'monkey -p {SNAPCHAT_PACKAGE} -c android.intent.category.LAUNCHER 1')
                time.sleep(5)
            else:
                self.device.shell('input keyevent 4')
                time.sleep(2)
        return None

    def log(self, round_no, how):
        # one row per sent round, written straight away so it survives Ctrl+C
        new = not os.path.exists(LOG_PATH)
        with open(LOG_PATH, "a") as f:
            if new:
                f.write("time,round,selected_by\n")
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{round_no},{how}\n")

    def exp_snaps(self, total=400):
        count = 0
        failures = 0
        while count != total:
            screen = self.find_start()
            if screen is None:
                print("Couldn't get Snapchat to the camera - stopping.")
                sys.exit(1)
            if screen == "camera":
                self.tap(SHUTTER_CORD)
            self.tap(SEND_TO_CORD)
            self.tap(SHORTCUT_CORD)
            if not self.shortcut_selected():
                print("Shortcut not selected - skipping this round so nothing gets posted to your story.", flush=True)
                failures += 1
            else:
                self.tap(SELECT_ALL_CORD)
                how = "select_all"
                if not self.ready_to_send():
                    # One-person shortcut: there's no Select All, so tick the friend directly
                    self.tap(FIRST_FRIEND_CORD)
                    how = "single_friend"
                if not self.ready_to_send():
                    print("Selection looks wrong - skipping this round without sending.", flush=True)
                    failures += 1
                else:
                    self.tap(SEND_GRP_CORD)
                    count += 1
                    failures = 0
                    self.log(count, how)
                    print(f"Cycle: {count} ({how})", flush=True)
            if failures >= 3:
                print("3 rounds in a row went wrong - stopping.")
                sys.exit(1)
            time.sleep(1)


def select_device():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    if not devices:
        print("No devices attached.")
        sys.exit(1)

    print("Connected devices:")
    for idx, device in enumerate(devices):
        print(f"{idx}: {device.serial}")

    # Default to first device if only one
    selected_index = 0 if len(devices) == 1 else int(input("Select device index: "))
    return devices[selected_index]


def main():
    total = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    SnapScore(select_device()).exp_snaps(total)


if __name__ == "__main__":
    main()
