import time
import sys
import struct
import select
#sudo apt-get install evtest
#sudo evtest

# Replace with the correct event device
device_path = '/dev/input/event8'
device = open(device_path, 'rb')

def get_event_data(data):
    """Decode and return the event data."""
    # Unpack the input event structure (24 bytes)
    time_sec, time_usec, event_type, code, value = struct.unpack('llHHI', data)
    return event_type, code, value

print("Waiting for card swipe...")
gotten = ''

while True:
    # Use select to check if data is available for reading
    r, w, e = select.select([device], [], [], 0.1)  # 0.1-second timeout
    
    if device in r:
        try:
            # Read event data (24 bytes at a time)
            data = device.read(24)
            if len(data) == 24:
                event_type, code, value = get_event_data(data)
                # Check if it's a key press event (event_type 1)
                if event_type == 1:
                    # Convert key code to ASCII character
                    if 32 <= value <= 126:
                        sys.stdout.write(chr(value))
                        gotten += chr(value)
                        sys.stdout.flush()
                    elif value == 13:  # Enter key
                        sys.stdout.write('\n')
                        sys.stdout.flush()
                        print("Enter key pressed")
        except Exception as e:
            print(f"Error: {e}")
    else:
        # No card swipe detected, print the collected data so far
        print("No card swipe detected. Collected data:", gotten)
    
    time.sleep(3)
