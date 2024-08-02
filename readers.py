import usb.core
import usb.util
import time

# Vendor and Product ID for the AugustaS device
VENDOR_ID = 0x0acd
PRODUCT_ID = 0x3810

# Find the USB device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError('Device not found')

# Detach the kernel driver if it's attached
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

# Set the configuration
dev.set_configuration()

# Get the active configuration
cfg = dev.get_active_configuration()

# Access the first interface
intf = cfg.interfaces()[0]

# Find the IN endpoint (interrupt IN endpoint)
ep_in = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

if ep_in is None:
    raise ValueError("IN Endpoint not found")

print("Starting data read...")

try:
    while True:
        try:
            # Read data from the IN endpoint
            data = ep_in.read(ep_in.wMaxPacketSize, timeout=5000)  # Adjust timeout and size if needed
            if data:
                # Print the raw data (may need further processing depending on device)
                print("Data received:", data)
        except usb.core.USBError as e:
            if e.errno == 110:  # Timeout error
                print("Timeout occurred, retrying...")
            else:
                print("USB error:", e)
        time.sleep(1)  # Delay between reads

finally:
    # Clean up
    usb.util.dispose_resources(dev)
    if dev.is_kernel_driver_active(0):
        dev.attach_kernel_driver(0)
