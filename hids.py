import hid
import time

# Define the Vendor ID and Product ID for your device
VID = 0x0acd  # Replace with your device's VID
PID = 0x3810  # Replace with your device's PID

# Open the HID device
def open_device():
    h = hid.device()
    h.open(VID, PID)
    h.set_nonblocking(1)
    return h

# Calculate LRC (Longitudinal Redundancy Check)
def calculate_lrc(data):
    lrc = 0
    for byte in data:
        lrc ^= byte
    return lrc

# Calculate Checksum
def calculate_checksum(data):
    checksum = sum(data) % 256
    return checksum

# Prepare command with NGA protocol
def prepare_command(command_body):
    stx = 0x02
    etx = 0x03
    len_low = len(command_body) & 0xFF
    len_high = (len(command_body) >> 8) & 0xFF
    lrc = calculate_lrc(command_body)
    checksum = calculate_checksum(command_body)

    command = bytearray([stx, len_low, len_high] + command_body + [lrc, checksum, etx])
    return command

# Send command and read response
def send_command(device, command):
    device.write(command)
    time.sleep(1)  # Wait for the device to process the command
    response = device.read(64)  # Adjust the read size as necessary
    return response

# Main function
def main():
    # Open the device
    device = open_device()

    # Define the command body (example command: Get DUKPT Key KSN)
    command_body = [
        0x78,  # Command Prefix (Configuration commands)
        0x46,  # Function ID
        0x3E,  # Specific Function ID
        0x04, 0x00,  # Length of Data (2 bytes)
        0x02,  # KeyNameIndex
        0x01, 0x00,  # Length of Key Slot (2 bytes)
        0x00   # Key Slot
    ]

    # Prepare and send the command
    command = prepare_command(command_body)
    print("Sending command:", command)
    response = send_command(device, command)

    # Print the raw response
    print("Raw response:", response)

    # Process response
    if response:
        if len(response) >= 6:  # Ensure there are enough bytes for STX, LRC, CheckSUM, and ETX
            stx, len_low, len_high, *response_body, lrc, checksum, etx = response

            # Verify STX and ETX
            if stx != 0x02 or etx != 0x03:
                print("Invalid response: Missing STX or ETX")
                return

            # Verify LRC and checksum
            if lrc == calculate_lrc(response_body) and checksum == calculate_checksum(response_body):
                # Extract and print response status and data
                response_status = response_body[0]
                response_data = response_body[1:]
                print("Valid response:")
                print("Response Status:", response_status)
                print("Response Data:", response_data)
            else:
                print("Invalid response: LRC or Checksum mismatch")
        else:
            print("Invalid response: Insufficient data length")
    else:
        print("No response received or response is empty")

    # Close the device
    device.close()

if __name__ == "__main__":
    main()
