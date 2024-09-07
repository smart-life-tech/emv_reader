import os
import struct
from datetime import datetime

# The path to your keyboard event file (check with 'cat /proc/bus/input/devices' to find yours)
DEVICE_PATH = "/dev/input/event1"


# Event format: struct with 16-byte size
EVENT_FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

def read_input_events(device_path):
    with open(device_path, 'rb') as device:
        print(f"Listening for keyboard events on {device_path}...")
        while True:
            # Read an event
            event = device.read(EVENT_SIZE)
            if event:
                (tv_sec, tv_usec, type, code, value) = struct.unpack(EVENT_FORMAT, event)
                # Key press/release events (type 1)
                if type == 1:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if value == 1:  # Key press
                        print(f"{timestamp} Key {code} pressed")
                    elif value == 0:  # Key release
                        print(f"{timestamp} Key {code} released")

if __name__ == "__main__":
    # Make sure the script is run with enough privileges (root) to access the device
    if os.geteuid() != 0:
        print("This script must be run as root to access /dev/input/")
        exit(1)

    # Start reading events
    read_input_events(DEVICE_PATH)
