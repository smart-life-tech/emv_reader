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

# Prepare NGA command
def prepare_nga_command(command_body):
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

# Parse NGA response
def parse_nga_response(response):
    if len(response) >= 6:  # Ensure there are enough bytes for STX, LRC, CheckSUM, and ETX
        stx, len_low, len_high, *response_body, lrc, checksum, etx = response

        # Verify STX and ETX
        if stx != 0x02 or etx != 0x03:
            print("Invalid response: Missing STX or ETX")
            return

        # Verify LRC and checksum
        if lrc == calculate_lrc(response_body) and checksum == calculate_checksum(response_body):
            response_status = response_body[0]
            response_data = bytearray(response_body[1:]).decode('ascii', errors='ignore')

            if response_status == 0x06:  # ACK
                print("Valid response (ACK):", response_data)
            elif response_status == 0x15:  # NAK
                error_code = response_data[:4]  # First 2 bytes for error code
                print("Error response (NAK): Error Code:", error_code)
                if len(response_data) > 4:
                    tag = response_data[4:]  # Remaining bytes for tag
                    print("Tag:", tag)
            else:
                print("Unknown response status")
        else:
            print("Invalid response: LRC or Checksum mismatch")
    else:
        print("Invalid response: Insufficient data length")

# Main function
def main():
    # Open the device
    device = open_device()

    # Define and prepare NGA command (example command for firmware version)
    # Command for firmware version (example: [0x78, 0x46, 0x01])
    nga_command_body = [0x78, 0x46, 0x01]  # Configuration command for example
    nga_command = prepare_nga_command(nga_command_body)
    print("Sending NGA command:", nga_command)
    nga_response = send_command(device, nga_command)
    print("NGA Raw response:", nga_response)
    parse_nga_response(nga_response)

    # Close the device
    device.close()

if __name__ == "__main__":
    main()
