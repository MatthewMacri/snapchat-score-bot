"""
ADB Connection Config
Switch between USB and Wireless without changing bot code
"""

# Connection mode: "auto", "usb", or "wireless"
CONNECTION_MODE = "wireless"

# If CONNECTION_MODE = "wireless", specify the Tailscale IP:port
WIRELESS_DEVICE = "100.111.3.63:5555"

# USB serial (usually auto-detected)
USB_DEVICE = "32140DLH20012Z"

def get_device_id():
    """Get the device to use based on config"""
    import subprocess
    
    if CONNECTION_MODE == "auto":
        # Let ADB find it automatically (fastest)
        return None
    elif CONNECTION_MODE == "wireless":
        return WIRELESS_DEVICE
    elif CONNECTION_MODE == "usb":
        return USB_DEVICE
    else:
        raise ValueError(f"Unknown CONNECTION_MODE: {CONNECTION_MODE}")

if __name__ == "__main__":
    print(f"Connection mode: {CONNECTION_MODE}")
    device = get_device_id()
    print(f"Device: {device if device else 'Auto-detect'}")
