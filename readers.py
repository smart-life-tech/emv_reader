import usb.core
import usb.util

# Find the device
dev = usb.core.find(idVendor=0x0acd, idProduct=0x3810)  # Replace with your Vendor ID and Product ID

if dev is None:
    raise ValueError("Device not found")
# Detach kernel driver if necessary
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)
# Set the active configuration. With no arguments, the first configuration will be the active one
dev.set_configuration()

# Get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

ep_out = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

ep_in = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

assert ep_out is not None
assert ep_in is not None

# Define the command to get firmware version
command = b'\x02\x52\x22\x03\x71'  # 0x71 is the LRC value for the command 0x52 0x22

# Send the command
ep_out.write(command)

# Read the response
response = ep_in.read(size=64)  # Adjust the size according to your expected response length
print("Response:", response)

# Interpret the response
# The response format is <0x02> <Len_Low><Len_High> <Response Body> <LRC> <CheckSUM> <0x03>
response_data = response[3:-3]  # Stripping off the STX, length, LRC, CheckSUM, and ETX
print("Firmware Version:", response_data)
# Reattach the kernel driver if needed (usually only if you need to let the kernel handle it again)
usb.util.dispose_resources(dev)