import hid

# Define the Vendor ID and Product ID for your device
VID = 0x0ACD  # Replace with your device's VID
PID = 0x3410  # Replace with your device's PID

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
    response = device.read(64)  # Adjust the read size as necessary
    return response

# Main function
def main():
    # Open the device
    device = open_device()

    # Define the command body (example command)
    command_body = [0x72, 0xF1]  # Example command: ICC read

    # Prepare and send the command
    command = prepare_command(command_body)
    print("Sending command:", command)
    response = send_command(device, command)

    # Print the raw response
    print("Raw response:", response)

    # Process response
    if response:
        stx, len_low, len_high, *response_body, lrc, checksum, etx = response
        # Verify LRC and checksum
        if lrc == calculate_lrc(response_body) and checksum == calculate_checksum(response_body):
            print("Valid response:", response_body)
        else:
            print("Invalid response")
    else:
        print("No response received")

    # Close the device
    device.close()

if __name__ == "__main__":
    main()
