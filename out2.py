from smartcard.System import readers
from smartcard.util import toHexString

# Select the reader
r = readers()
reader = r[1]  # ACS ACR 38U-CCID

# Connect to the card
connection = reader.createConnection()
connection.connect()

# Step 1: Verify PSC (assuming PSC is 0xFF, 0xFF, 0xFF)
verify_psc = [0xFF, 0x20, 0x00, 0x00, 0x03, 0xFF, 0xFF, 0xFF]
response, sw1, sw2 = connection.transmit(verify_psc)

if sw1 == 0x90 and sw2 == 0x00:
    print("PSC verification successful")

    # Step 2: Write data (Example: Writing 0x31, 0x32, 0x33 to address 0x04)
    write_command = [0xFF, 0xD0, 0x00, 0x04, 0x03, 0x31, 0x32, 0x33]
    response, sw1, sw2 = connection.transmit(write_command)

    if sw1 == 0x90 and sw2 == 0x00:
        print("Data write successful")
    else:
        print(f"Write failed: {hex(sw1)} {hex(sw2)}")
else:
    print(f"PSC verification failed: {hex(sw1)} {hex(sw2)}")
