import usb.core
import usb.util
import time

# Find the MSR90 device
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
expected_length = False
while True:
    # Read data from the device
    time.sleep(2)
    print("Reading data")
    data_chunks = []
    try:
        while True:
            data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            if data:
                data_chunks.append(data)
                # Check if the data is complete (e.g., based on expected length or specific end byte)
                if  expected_length:  # Replace with actual condition
                    break
            else:
                break

        # Process the complete data
        full_data = b''.join(data_chunks)
        print('Complete data read:', full_data)

    except usb.core.USBError as e:
        expected_length=True
        if e.args == ('Operation timed out',):
            print("Timed out")
        else:
            print("USB Error:", e)

    except Exception as ex:
        print("An error occurred:", ex)
