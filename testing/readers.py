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

# Claim the interface that is likely to be for EMV (try Interface 1)
usb.util.claim_interface(dev, 1)

# Endpoint for reading EMV data (Interrupt IN)
endpoint_in = dev[0][(1, 0)][0]  # Interface 1 IN endpoint (0x81)

try:
    # Example control transfer that might be needed to initialize EMV
    # This is a placeholder, and the actual command needs to be determined from documentation
    init_command = [0x00, 0x00, 0x00, 0x00]  # This is just an example; adjust accordingly
    dev.ctrl_transfer(0x21, 0x09, 0x0200, 1, [0x00])  # Example of control transfer
    
    while True:
        time.sleep(3)  # Adjust sleep time as needed
        
        # Try reading data, see if the device responds differently after a potential mode switch
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
    if not dev.is_kernel_driver_active(1):
        dev.attach_kernel_driver(1)
