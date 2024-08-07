from smartcard.System import readers
from smartcard.util import toHexString

# Get the list of available readers
r = readers()
print("Available readers:", r)

if len(r) == 0:
    print("No readers available")
    exit()

# Use the first reader
reader = r[0]
connection = reader.createConnection()
connection.connect()

# Send a command to the card
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x0A]  # Example command (change as needed)
data, sw1, sw2 = connection.transmit(SELECT)
print("Response:", toHexString(data))
print("Status words:", "%02X %02X" % (sw1, sw2))
