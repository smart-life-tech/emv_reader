import os
import struct
from datetime import datetime
import pychrome
import time
# The path to your keyboard event file
DEVICE_PATH = "/dev/input/event1"

# Event format: struct with 16-byte size
EVENT_FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)
count=0
# Map key codes to characters (normal and shifted)
KEY_MAP = {
    2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0',
    12: '-', 13: '=',  # Added '=' to the map
    16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't', 21: 'y', 22: 'u', 23: 'i', 24: 'o', 25: 'p',
    30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g', 35: 'h', 36: 'j', 37: 'k', 38: 'l',
    44: 'z', 45: 'x', 46: 'c', 47: 'v', 48: 'b', 49: 'n', 50: 'm',
    39: ';', 40: '=', 51: ',', 52: '.', 53: '/', 28: '\n', 57: ' ',
    # With shift
    'SHIFTED': {
        2: '!', 3: '@', 4: '#', 5: '$', 6: '%', 7: '^', 8: '&', 9: '*', 10: '(', 11: ')',
        12: '_', 13: '+',  # Shifted characters for '-' and '='
        16: 'Q', 17: 'W', 18: 'E', 19: 'R', 20: 'T', 21: 'Y', 22: 'U', 23: 'I', 24: 'O', 25: 'P',
        30: 'A', 31: 'S', 32: 'D', 33: 'F', 34: 'G', 35: 'H', 36: 'J', 37: 'K', 38: 'L',
        44: 'Z', 45: 'X', 46: 'C', 47: 'V', 48: 'B', 49: 'N', 50: 'M',
        39: ':', 40: '+', 51: '<', 52: '>', 53: '?', 57: ' ',
    }
}

SHIFT_KEY_CODES = {42, 54}  # Left shift and right shift
SHIFT_HELD = False
def escape_js_string(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', '\\n')



def chrome(card_data,type):
    print("Starting Chrome interaction")
    try:
        # Connect to the Chromium browser
        browser = pychrome.Browser(url="http://127.0.0.1:9222")
        tabs = browser.list_tab()

        if not tabs:
            print("No tabs found")
            exit(1)

        tab = tabs[0]
        tab.start()
        # Define the path to the secret file
        secret_file_path = os.path.expanduser("~/.hidden_dir/secret_file.txt")

        # Read the file contents
        with open(secret_file_path, 'r') as file:
            secret_data = file.read()

        # Split the secret data into pos_id and brn
        secret_lines = secret_data.strip().splitlines()
        pos_id = secret_lines[0].split(': ')[1]
        brn = secret_lines[1].split(': ')[1]
        print(brn)
        print(pos_id)

        # JavaScript code to trigger the card check with simulated card data
        js_code = f"""
        window.emvProcessed("{card_data}", "{type}", "{pos_id}", "{brn}");
        """
        js_code = f"""
        window.emvProcessed("{escape_js_string(card_data)}", "{escape_js_string(type)}", "{escape_js_string(pos_id)}", "{escape_js_string(brn)}");
        """
        # Execute the JavaScript code
        result = tab.Runtime.evaluate(expression=js_code)
        print("JavaScript executed:", result)
        
        # Optional: Close the tab connection
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        
def process_key_event(code, value):
    global SHIFT_HELD

    if value == 1:  # Key press
        if code in SHIFT_KEY_CODES:
            SHIFT_HELD = True
        else:
            if SHIFT_HELD and code in KEY_MAP['SHIFTED']:
                return KEY_MAP['SHIFTED'][code]
            elif code in KEY_MAP:
                return KEY_MAP[code]
    elif value == 0:  # Key release
        if code in SHIFT_KEY_CODES:
            SHIFT_HELD = False
    return None

def read_input_events(device_path):
    with open(device_path, 'rb') as device:
        print(f"Listening for keyboard events on {device_path}...")
        captured_data = ""

        while True:
            # Read an event
            event = device.read(EVENT_SIZE)
            if event:
                (tv_sec, tv_usec, type, code, value) = struct.unpack(EVENT_FORMAT, event)

                if type == 1:  # Key press/release event
                    key = process_key_event(code, value)
                    if key:
                        captured_data += key
                        print(key, end='', flush=True)

                    # Stop capturing when '?' is detected
                    if captured_data.endswith('?'):
                        global count
                        count=count+1
                        print(count)
                        if count==4:
                            print("\nCaptured Data: ", captured_data)
                            time.sleep(1)
                            chrome(captured_data,"swipe")
                            captured_data = ""  # Reset the data for the next swipe
                            count=0

if __name__ == "__main__":
    # Make sure the script is run with enough privileges (root) to access the device
    if os.geteuid() != 0:
        print("This script must be run as root to access /dev/input/")
        exit(1)

    # Start reading events
    read_input_events(DEVICE_PATH)
