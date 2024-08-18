from smartcard.System import readers

r = readers()
connection = r[1].createConnection()
connection.connect()

# Write example data to the card
write_apdu = [0x00, 0xD0, 0x00, 0x00, 0x05]  # Write command
data = [0x12, 0x34, 0x56, 0x78, 0x90]  # Example data to write
connection.transmit(write_apdu + data)

# Read back the data
read_apdu = [0x00, 0xB0, 0x00, 0x00, 0x05]  # Read command for the same length
response, sw1, sw2 = connection.transmit(read_apdu)
print(f"Read Data: {response}")
