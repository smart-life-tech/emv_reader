import os
import struct
from datetime import datetime

# The path to your keyboard event file
DEVICE_PATH = "/dev/input/event1"

# Event format: struct with 16-byte size
EVENT_FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

# Map key codes to characters (normal and shifted)
KEY_MAP = {
    # Without shift
    2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0',
    16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't', 21: 'y', 22: 'u', 23: 'i', 24: 'o', 25: 'p',
    30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g', 35: 'h', 36: 'j', 37: 'k', 38: 'l',
    44: 'z', 45: 'x', 46: 'c', 47: 'v', 48: 'b', 49: 'n', 50: 'm',
    39: ';', 40: '=', 51: ',', 52: '.', 53: '/', 28: '\n', 57: ' ',
    # With shift
    'SHIFTED': {
        2: '!', 3: '@', 4: '#', 5: '$', 6: '%', 7: '^', 8: '&', 9: '*', 10: '(', 11: ')',
        16: 'Q', 17: 'W', 18: 'E', 19: 'R', 20: 'T', 21: 'Y', 22: 'U', 23: 'I', 24: 'O', 25: 'P',
        30: 'A', 31: 'S', 32: 'D', 33: 'F', 34: 'G', 35: 'H', 36: 'J', 37: 'K', 38: 'L',
        44: 'Z', 45: 'X', 46: 'C', 47: 'V', 48: 'B', 49: 'N', 50: 'M',
        39: ':', 40: '+', 51: '<', 52: '>', 53: '?', 57: ' ', 12: 'B', 13: '^', 43: '?'
    }
}

SHIFT_KEY_CODES = {42, 54}  # Left shift and right shift

def read_input_events(device_path):
    with open(device_path, 'rb') as device:
        print(f"Listening for keyboard events on {device_path}...")
        captured_data = ""
        shift_pressed = False

        while True:
            # Read an event
            event = device.read(EVENT_SIZE)
            if event:
                (tv_sec, tv_usec, type, code, value) = struct.unpack(EVENT_FORMAT, event)

                # Handle Shift key press/release
                if type == 1 and code in SHIFT_KEY_CODES:
                    if value == 1:  # Shift pressed
                        shift_pressed = True
                    elif value == 0:  # Shift released
                        shift_pressed = False

                # Key press events (type 1)
                elif type == 1 and value == 1:  # Key press
                    if shift_pressed and code in KEY_MAP['SHIFTED']:
                        key = KEY_MAP['SHIFTED'][code]
                    elif code in KEY_MAP:
                        key = KEY_MAP[code]
                    else:
                        key = ''

                    if key:
                        captured_data += key
                        print(key, end='', flush=True)

                    # Stop capturing when '?' is detected
                    if captured_data.endswith('?'):
                        print("\nCaptured Data: ", captured_data)
                        captured_data = ""  # Reset the data for the next swipe

if __name__ == "__main__":
    # Make sure the script is run with enough privileges (root) to access the device
    if os.geteuid() != 0:
        print("This script must be run as root to access /dev/input/")
        exit(1)

    # Start reading events
    read_input_events(DEVICE_PATH)
