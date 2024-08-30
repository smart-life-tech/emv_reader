import usb.core
import usb.util

# Find the device
dev = usb.core.find(idVendor=0x0801, idProduct=0x0005)

if dev is None:
    raise ValueError("Device not found")

# Detach the device from the kernel driver if necessary
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

# Set the configuration
dev.set_configuration()

# Claim the first interface
usb.util.claim_interface(dev, 0)

# Endpoint addresses for reading data
endpoint_in = dev[0][(0, 0)][1]  # IN endpoint address
endpoint_out = dev[0][(0, 0)][0]  # OUT endpoint address

# Read data from the device
try:
    # You may need to send some data to initialize communication
    # dev.write(endpoint_out.bEndpointAddress, some_data)

    data = dev.read(endpoint_in.bEndpointAddress, endpoint_in.wMaxPacketSize)
    print("Data received:", data)
except usb.core.USBError as e:
    print("Error reading from the device:", str(e))
finally:
    # Release the interface
    usb.util.release_interface(dev, 0)
    # Reattach the kernel driver
    dev.attach_kernel_driver(0)
