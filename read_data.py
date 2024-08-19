from smartcard.System import readers
from smartcard.util import toHexString

def transmit_apdu(connection, apdu):
    response, sw1, sw2 = connection.transmit(apdu)
    print(f"APDU: {toHexString(apdu)}")
    print(f"Response: {toHexString(response)}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")
    return response, sw1, sw2

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

    # Select VISA AID
    select_aid_apdu = [0x00, 0xA4, 0x04, 0x00, 0x07] + [0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10] + [0x00]
    response, sw1, sw2 = transmit_apdu(connection, select_aid_apdu)
    
    if sw1 == 0x90 and sw2 == 0x00:
        # Example: Read Record 1, SFI 1
        read_record_apdu = [0x00, 0xB2, 0x01, 0x0C, 0x00]
        response, sw1, sw2 = transmit_apdu(connection, read_record_apdu)

        # Example: Read Record 2, SFI 1
        read_record_apdu = [0x00, 0xB2, 0x02, 0x0C, 0x00]
        response, sw1, sw2 = transmit_apdu(connection, read_record_apdu)
    else:
        print("Failed to select VISA application.")

except Exception as e:
    print(f"An error occurred: {e}")
