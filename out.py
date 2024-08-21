import usb.core
import usb.util

# Replace with your device's vendor and product ID
VENDOR_ID = 0x072f
PRODUCT_ID = 0x90cc
# Find the devi
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError('Device not found')

# Detach kernel driver if necessary
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

# Set the configuration
dev.set_configuration()

# Get the active configuration
cfg = dev.get_active_configuration()

# Get the first interface
intf = cfg[(0, 0)]

# Find the OUT and IN endpoints
ep_out = usb.util.find_descriptor(
    intf,
    # Match the first OUT endpoint
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)

ep_in = usb.util.find_descriptor(
    intf,
    # Match the first IN endpoint
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)
print(f"Endpoint OUT: {ep_out}")
print(f"Endpoint IN: {ep_in}")
assert ep_out is not None, "Endpoint OUT not found"
assert ep_in is not None, "Endpoint IN not found"

# Perform operations
try:
    # Write data to the card
    write_command = bytes([0xFF, 0xA4, 0x00, 0x00, 0x01, 0x06, 0x03, 0x04])  # Example write command
    print(f"Data sending..: {write_command}")
    ep_out.write(write_command)
    print(f"Data sent: {write_command}")
    data_received = ep_in.read(ep_in.wMaxPacketSize, timeout=10000)  # Increase timeout to 10 seconds
    print(f"Data received: {data_received}")
    # Read data from the card
    print(f"Data reading..: {write_command}")
    read_command = bytes([0x01, 0xB0, 0x00, 0x04])  # Example read command
    ep_out.write(read_command)
    data_received = ep_in.read(ep_in.wMaxPacketSize, timeout=10000)  # Increase timeout to 10 seconds
    print(f"Data received: {data_received}")

finally:
    # Release resources and reattach the kernel driver if it was detached
    usb.util.dispose_resources(dev)
