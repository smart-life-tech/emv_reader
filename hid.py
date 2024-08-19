import hid

# Open the device
h = hid.device()
h.open(0x0ACD, 0x3410)  # Replace with correct VID and PID

# Set non-blocking mode
h.set_nonblocking(1)

# Read data from device
data = h.read(64)

print("Data:", data)

# Close the device
h.close()
