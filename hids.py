import hid

# Open the device
h = hid.device()
h.open(0x1136, 0x3004)

# Set non-blocking mode
h.set_nonblocking(True)

try:
    while True:
        data = h.read(64)  # Read 64 bytes (change if necessary)
        if data:
            print("Data received:", data)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    h.close()
