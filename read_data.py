from smartcard.System import readers
from smartcard.util import toHexString

def send_apdu(connection, apdu):
    response, sw1, sw2 = connection.transmit(apdu)
    print(f"APDU: {toHexString(apdu)}")
    print(f"Response (Hex): {toHexString(response)}")
    print(f"Response (ASCII): {''.join([chr(byte) for byte in response if 32 <= byte <= 126])}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")
    return response, sw1, sw2

try:
    # List available readers
    reader_list = readers()
    if not reader_list:
        raise Exception("No readers available.")

    # Use the first available reader
    reader =  reader = "ACS ACR38U-CCID 00 00"#reader_list[0]  # Adjust index if needed reader_list[1]
    print(f"Using reader: {reader}")

    # Connect to the reader
    connection = reader.createConnection()
    connection.connect()
        

    def send_apdu(connection, apdu):
        response, sw1, sw2 = connection.transmit(apdu)
        return response, sw1, sw2

    # Example APDU command to read binary data
    read_binary_apdu = [0xFF, 0xB0, 0x00, 0x00, 0x19]  # Read 16 bytes from offset 0x00
    response, sw1, sw2 = send_apdu(connection, read_binary_apdu)
    print(f"Read Binary Response: {toHexString(response)}")
    print(f"Response (ASCII): {''.join([chr(byte) for byte in response if 32 <= byte <= 126])}")
    print(f"Read Binary Response: {(response)}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")

except Exception as e:
    print(f"An error occurred: {e}")
