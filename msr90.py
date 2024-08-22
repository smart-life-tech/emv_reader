import usb.core
import usb.util

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

# Read data from the device
try:
    while True:
        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        # Process the data as needed
        print('Data read:', data)

except usb.core.USBError as e:
    if e.args == ('Operation timed out',):
        print("Timed out")
