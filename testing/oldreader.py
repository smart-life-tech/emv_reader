from smartcard.System import readers
from smartcard.util import toHexString

try:
    # List available readers
    reader_list = readers()
    if not reader_list:
        raise Exception("No readers available.")

    # Use the first available reader
    reader = reader_list[0]
    print(f"Using reader: {reader}")

    # Connect to the reader
    connection = reader.createConnection()
    connection.connect()

    # Send a command to the card (example: get card UID)
    apdu = [0xFF, 0xCA, 0x00, 0x00, 0x00]
    response, sw1, sw2 = connection.transmit(apdu)

    print(f"Response: {toHexString(response)}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")

except Exception as e:
    print(f"An error occurred: {e}")
