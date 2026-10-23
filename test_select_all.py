"""
Systematic test of Select All button detection and tapping.
Logs all attempts and calibrates for Google Pixel 7.
"""
from snapscore import SnapScore, select_device
import struct
import time
import json

LOG_FILE = "select_all_test_log.json"
logs = []

def log_test(test_name, details):
    """Log test result"""
    entry = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "test": test_name,
        "details": details
    }
    logs.append(entry)
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"DETAILS: {details}")
    print(f"{'='*60}")

def sample_pixel_colors(bot, test_name):
    """Sample pixels around the button area"""
    shot = bot.screenshot()
    width = struct.unpack_from("<I", shot, 0)[0]
    
    # Test multiple points around expected button area
    test_points = {
        "button_center": (603, 283),
        "button_left": (550, 283),
        "button_right": (650, 283),
        "button_top": (603, 270),
        "button_bottom": (603, 300),
    }
    
    colors = {}
    for name, point in test_points.items():
        offset = 16 + (point[1] * width + point[0]) * 4
        b, g, r = shot[offset], shot[offset+1], shot[offset+2]
        colors[name] = f"RGB({r}, {g}, {b})"
    
    log_test(f"Pixel sampling - {test_name}", colors)
    return colors

device = select_device()
bot = SnapScore(device)

print("\n\n" + "="*60)
print("STARTING SELECT ALL BUTTON CALIBRATION TEST")
print("Google Pixel 7 - Dev Mode ON")
print("="*60)

# TEST 1: Sample colors when button says "Select All"
print("\n>>> Navigate to Send To screen with Select All visible")
input("Press ENTER when ready (screen should show 'Select All' button)...")

sample_pixel_colors(bot, "Select All visible")

# TEST 2: Find button with image recognition
print("\nTesting image recognition...")
coords = bot.find_select_all_button()
log_test("Image recognition result", {"found_coordinates": coords})

# TEST 3: Tap and observe
print(f"\nAttempting to tap at {coords}...")
bot.tap(coords)
time.sleep(2)

shot = bot.screenshot()
print("Taking screenshot after tap...")

# TEST 4: Check if button changed to "Deselect All"
# Sample the button area again
sample_pixel_colors(bot, "After first tap")

log_test("After tap observation", {
    "expected": "Button should change to 'Deselect All'",
    "action": "Check screenshot"
})

# Save logs
with open(LOG_FILE, 'w') as f:
    json.dump(logs, f, indent=2)

print(f"\n\nLogs saved to {LOG_FILE}")
print("\nTest Complete!")

