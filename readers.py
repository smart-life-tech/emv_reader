import usb.core
import usb.util
import time

# Find the device
dev = usb.core.find(idVendor=0x0801, idProduct=0x0005)

if dev is None:
    raise ValueError("Device not found")

# Detach the device from the kernel driver if necessary
if dev.is_kernel_driver_active(1):
    dev.detach_kernel_driver(1)

# Set the configuration
#dev.set_configuration()

# Claim the EMV interface (interface 1)
usb.util.claim_interface(dev, 1)

# Endpoint addresses for EMV reader
endpoint_in = dev[0][(1, 0)][0]  # IN endpoint for interface 1

try:
    while True:
        time.sleep(3)  # Adjust sleep time as needed
        
        # Read data from the EMV reader
        try:
            data = dev.read(endpoint_in.bEndpointAddress, endpoint_in.wMaxPacketSize, timeout=5000)  # 5-second timeout
            print("EMV Data received:", data)
        except usb.core.USBError as e:
            if e.errno == 110:  # Timeout error
                print("Timeout: No EMV data received")
            else:
                print("Error reading from the EMV reader:", str(e))
except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Release the interface and reattach the kernel driver when done
    usb.util.release_interface(dev, 1)
    if dev.is_kernel_driver_active(1) == False:
        dev.attach_kernel_driver(1)
