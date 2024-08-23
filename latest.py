from smartcard.System import readers
from smartcard.util import toHexString
import pychrome
import time
done =True
#7824109948240159
def send_apdu(connection, apdu):
    response, sw1, sw2 = connection.transmit(apdu)
    print(f"APDU: {toHexString(apdu)}")
    print(f"Response (Hex): {toHexString(response)}")
    print(f"Response (ASCII): {''.join([chr(byte) for byte in response if 32 <= byte <= 126])}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")
    # Filter to get only the digits from the first 16 bytes
    response_digits = ''.join([chr(byte) for byte in response[:16] if chr(byte).isdigit()])
    print(f"Response (Digits): {response_digits}")
    # Convert response to ASCII
    response_ascii = ''.join([chr(byte) for byte in response if 32 <= byte <= 126])
    
    # Trigger the chrome function with the card data
    chrome(response_digits)
    
    return response, sw1, sw2
def send_apdus(connection, apdu):
    response, sw1, sw2 = connection.transmit(apdu)
    print(f"APDU: {toHexString(apdu)}")
    print(f"Response (Hex): {toHexString(response)}")
    print(f"Response (ASCII): {''.join([chr(byte) for byte in response if 32 <= byte <= 126])}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")
    
    return response, sw1, sw2
def chrome(card_data):
    print("Starting Chrome interaction")
    try:
        # Connect to the Chromium browser
        browser = pychrome.Browser(url="http://127.0.0.1:9222")
        tabs = browser.list_tab()

        if not tabs:
            print("No tabs found")
            exit(1)

        tab = tabs[0]
        tab.start()

        # JavaScript code to trigger the card check with simulated card data
        js_code = f"""
        window.emvProcessed("{card_data}");
        """
        # Execute the JavaScript code
        result = tab.Runtime.evaluate(expression=js_code)
        print("JavaScript executed:", result)
        
        # Optional: Close the tab connection
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
while True:
    try:
        if done:
            time.sleep(3)
            # List available readers
            reader_list = readers()
            if not reader_list:
                raise Exception("No readers available.")

            # Ensure you select the correct reader from the list
            reader_name = "ACS ACR38U-CCID 00 00"
            reader = None
            for r in reader_list:
                if reader_name in r.name:
                    reader = r
                    break

            if not reader:
                raise Exception(f"Reader '{reader_name}' not found.")

            print(f"Using reader: {reader}")

            # Connect to the reader
            connection = reader.createConnection()
            connection.connect()
            # Example APDU command to read binary data
            read_binary_apdu = [0xFF, 0xA4, 0x00, 0x00, 0x01,0x06]  # Read 16 bytes from offset 0x00
            response, sw1, sw2 = send_apdus(connection, read_binary_apdu)
            time.sleep(1)
            # Example APDU command to read binary data
            read_binary_apdu = [0xFF, 0xB0, 0x00, 0x00, 0x14]  # Read 16 bytes from offset 0x00
            response, sw1, sw2 = send_apdu(connection, read_binary_apdu)
            done=False
        else:
            time.sleep(3)
            print("card already processed")
            done=True

    except Exception as e:
        print(f"An error occurred: {e}")
        done=True
