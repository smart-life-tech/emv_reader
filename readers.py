import usb.core
import usb.util
import time
# Vendor and Product ID
VENDOR_ID = 0x0acd
PRODUCT_ID = 0x3810

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
# Print configuration details for debugging
print(f"Configuration: {cfg}")

# Access the first interface in the configuration
try:
    intf = cfg.interfaces()[0]  # Access the first interface
except IndexError:
    raise ValueError("Interface not found")

# Print interface details for debugging
print(f"Interface gottrn: {intf}")

# Find the IN and OUT endpoints
#intf = cfg[0]  # Assuming interface 0 is the relevant one

ep_out = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)

ep_in = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

# Check if endpoints were found

if ep_in is None:
    raise ValueError("IN Endpoint not found")

# Perform operations
try:
    while True:
        # Write data to the OUT endpoint
        #data_to_send = b'Test data'  # Example data
        #ep_out.write(data_to_send)
        #print("Data sent successfully")

        # Read data from the IN endpoint
        data_received = ep_in.read(64)  # Adjust the size as needed
        print(f"Data received: {data_received}")
        time.sleep(3)

except usb.core.USBError as e:
        print(f"USB error: {e}")

finally:
    # Release resources and reattach the kernel driver if it was detached
    usb.util.dispose_resources(dev)
    if dev.is_kernel_driver_active(0):
        dev.attach_kernel_driver(0)
