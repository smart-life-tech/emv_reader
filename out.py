import usb.core
import usb.util

# Replace with your device's vendor and product ID
VENDOR_ID = 0x072f
PRODUCT_ID = 0x90cc
# Find the device
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

assert ep_out is not None, "Endpoint OUT not found"
assert ep_in is not None, "Endpoint IN not found"

# Perform operations
try:
    # Write data to the OUT endpoint
    data_to_send = bytes([0x01, 0xA4, 0x00, 0x04, 0x11, 0x22, 0x33, 0x44])  # Example command
    ep_out.write(data_to_send)
    print(f"Data sent: {data_to_send}")
    # Read data from the IN endpoint
    data_received = ep_in.read(64, timeout=5000)  # Adjust the size as needed
    print(f"Data received: {data_received}")

finally:
    # Release resources and reattach the kernel driver if it was detached
    usb.util.dispose_resources(dev)
