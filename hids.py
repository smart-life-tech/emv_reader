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

# Prepare command with ITP protocol
def prepare_itp_command(func_id, data=[]):
    stx = 0x02
    etx = 0x03
    command_body = [func_id] + data
    length = len(command_body) + 3  # including STX, ETX, and LRC
    lrc = calculate_lrc([stx] + command_body + [etx])

    command = bytearray([stx] + command_body + [etx, lrc])
    return command

# Prepare command with NGA protocol
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

# Parse ITP response
def parse_itp_response(response):
    if response:
        ack_nak = response[0]
        if ack_nak == 0x06:  # ACK
            # Process response
            print("ACK received")
            # Further parsing needed based on command and response format
        elif ack_nak == 0x15:  # NAK
            print("NAK received")
        else:
            print("Invalid response")
    else:
        print("No response received")

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
            # Extract and print response body
            response_data = bytearray(response_body).decode('ascii')
            print("Valid response:")
            print("Response Data:", response_data)
        else:
            print("Invalid response: LRC or Checksum mismatch")
    else:
        print("Invalid response: Insufficient data length")

# Main function
def main():
    # Open the device
    device = open_device()

    # Define and prepare ITP command for getting firmware version
    itp_command = prepare_itp_command(0x01)  # Example function ID for firmware version
    print("Sending ITP command:", itp_command)
    itp_response = send_command(device, itp_command)
    print("ITP Raw response:", itp_response)
    parse_itp_response(itp_response)

    # Define and prepare NGA command for getting firmware version
    nga_command_body = [0x78, 0x46, 0x01]  # Example NGA command
    nga_command = prepare_nga_command(nga_command_body)
    print("Sending NGA command:", nga_command)
    nga_response = send_command(device, nga_command)
    print("NGA Raw response:", nga_response)
    parse_nga_response(nga_response)

    # Close the device
    device.close()

if __name__ == "__main__":
    main()
