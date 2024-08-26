import os
import sys
import struct

# Replace with the correct event device
device_path = '/dev/input/event8'
device = open(device_path, 'rb')

def get_event_data(data):
    """Decode and return the event data."""
    event_type, code, value = struct.unpack('IHHI', data)
    return event_type, code, value

print("Waiting for card swipe...")

while True:
    try:
        # Read event data (16 bytes at a time)
        data = device.read(16)
        if len(data) == 16:
            event_type, code, value = get_event_data(data)
            # Check if it's a key press event (event_type 1)
            if event_type == 1:
                # Convert key code to ASCII character
                if 32 <= value <= 126:
                    sys.stdout.write(chr(value))
                    sys.stdout.flush()
                elif value == 13:  # Enter key
                    sys.stdout.write('\n')
                    sys.stdout.flush()
    except Exception as e:
        print(f"Error: {e}")
