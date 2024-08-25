import usb.core
import usb.util
import time

# Find the MSR90 device or similar USB magnetic stripe reader
dev = usb.core.find(idVendor=0xc216, idProduct=0x0180)

# Check if the device was found
if dev is None:
    raise ValueError("Device not found")

# Detach any kernel drivers
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

# Set the active configuration
dev.set_configuration()

# Get the endpoint for reading
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]
endpoint = intf[0]

# Initialize consecutive zero count
consecutive_zeros = 0
data_chunks = []

while True:
    # Read data from the device
    time.sleep(2)
    print("Reading data")

    try:
        while True:
            data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            if data:
                # Convert the data to ASCII, ignoring non-printable characters
                ascii_data = data.tobytes().decode('ascii', errors='ignore')

                # Print raw ASCII data for debugging
                print(f"Raw ASCII data: {ascii_data}")

                # Append the ASCII data
                data_chunks.append(ascii_data)

                # Check for non-zero data
                if any(data):  # If there is any non-zero data
                    consecutive_zeros = 0  # Reset the zero count
                else:
                    consecutive_zeros += 1
                    print(f"Zero data chunk received, count: {consecutive_zeros}")

                if consecutive_zeros >= 3:
                    print("Three consecutive zero-data chunks received. Stopping.")
                    break
            else:
                print("No data")
                break

        # Process the complete data
        full_data = ''.join(data_chunks)  # Correctly join strings
        print('Complete data read (ASCII):', full_data)

        # Parse the card data (for example, by detecting track delimiters)
        if '%' in full_data or ';' in full_data:
            # This assumes that the card reader sends data in a standard track format
            print('Parsed data:')
            print(full_data.strip())  # Output the cleaned and parsed card data

    except usb.core.USBError as e:
        if e.args == ('Operation timed out',):
            print("Timed out")
        else:
            print("USB Error:", e)

    except Exception as ex:
        print("An error occurred:", ex)
