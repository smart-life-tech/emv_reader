from smartcard.System import readers
from smartcard.util import toHexString

def send_apdu(connection, apdu):
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

    # Step 1: Select the VISA application
    select_apdu = [0x00, 0xA4, 0x04, 0x00, 0x07, 0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10, 0x00]
    response, sw1, sw2 = send_apdu(connection, select_apdu)

    if sw1 == 0x61:
        # Step 2: Use GET RESPONSE to retrieve additional data
        get_response_apdu = [0x00, 0xC0, 0x00, 0x00, sw2]  # sw2 indicates the number of bytes to retrieve
        response, sw1, sw2 = send_apdu(connection, get_response_apdu)

    if sw1 == 0x90 and sw2 == 0x00:
        # Application successfully selected, proceed to read records
        # Example: Read Record command (usually Record 1, SFI 1)
        read_record_apdu = [0x00, 0xB2, 0x01, 0x0C, 0x00]
        response, sw1, sw2 = send_apdu(connection, read_record_apdu)

        if sw1 == 0x90 and sw2 == 0x00:
            # Parse PAN and expiry date from the response
            # PAN is usually the first 16 digits in the response data
            pan = ''.join([chr(b) for b in response[:16]])
            expiry_date = response[16:20]
            expiry_date_str = f"{expiry_date[0]:02X}/{expiry_date[1]:02X}"

            print(f"PAN: {pan}")
            print(f"Expiry Date: {expiry_date_str}")
        else:
            print("Failed to read record.")
    else:
        print("Failed to select VISA application.")

except Exception as e:
    print(f"An error occurred: {e}")
