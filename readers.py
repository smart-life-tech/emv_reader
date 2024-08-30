import usb.core
import usb.util

# Find the device
dev = usb.core.find(idVendor=0x0801, idProduct=0x0005)

if dev is None:
    raise ValueError("Device not found")

# Detach the device from the kernel driver
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

# Set the configuration
dev.set_configuration()

# Claim the interface
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

# Find the endpoint
ep_in = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

if ep_in is None:
    raise ValueError("IN Endpoint not found")

# Read data from the IN endpoint
data = ep_in.read(ep_in.wMaxPacketSize)
print("Data received:", data)

# Release the interface
usb.util.release_interface(dev, intf)
