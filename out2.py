from smartcard.System import readers
from smartcard.util import toHexString

# Initialize reader
r = readers()
print("readers: ",r)
connection = r[1].createConnection()  # Using the ACS ACR 38U-CCID reader
connection.connect()

# Command to read data (replace with correct address and length)
READ_COMMAND = [0xFF, 0xB0, 0x00, 0x00, 0x10]  # Replace 0x10 with your length

data, sw1, sw2 = connection.transmit(READ_COMMAND)

if sw1 == 0x90 and sw2 == 0x00:
    print(f"Data read: {toHexString(data)}")
else:
    print(f"Error: SW1={sw1:02X}, SW2={sw2:02X}")
