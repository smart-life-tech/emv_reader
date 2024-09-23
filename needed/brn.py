#echo -e "pos_id: 1\nbrn: add5008577937ea6a3227b496eda41f92fb8630db42639efb89197cefb4e77a5617b766ddc1ab5da" > ~/.hidden_dir/secret_file.txt
#sudo PYTHONPATH=$PYTHONPATH:/home/chingup/.local/lib/python3.9/site-packages python3 brn.py
import threading
import time
from smartcard.System import readers
from smartcard.util import toHexString
import pychrome
import os
# Initialize a string variable to store the card data
gotten = ''
shift_pressed = False
done = False
def process_card():
    global done
    #start_keyboard_listener()
    while True:
        try:
            if 1:
                time.sleep(2)
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
                if not done:
                    # Example APDU command to read binary data
                    read_binary_apdu = [0xFF, 0xA4, 0x00, 0x00, 0x01, 0x06]  # Read 16 bytes from offset 0x00
                    response, sw1, sw2 = send_apdus(connection, read_binary_apdu)
                    time.sleep(1)
                    
                    # Another example APDU command to read binary data
                    read_binary_apdu = [0xFF, 0xB0, 0x00, 0x00, 0x16]  # Read 16 bytes from offset 0x00
                    response, sw1, sw2 = send_apdu(connection, read_binary_apdu)
                    done = True
                    print("Smartcard processing completed. You can now swipe the card.")

        except Exception as e:
            print(f"An error occurred: {e}")
            done = False

def send_apdu(connection, apdu):
    global done
    response, sw1, sw2 = connection.transmit(apdu)
    print(f"APDU: {toHexString(apdu)}")
    print(f"Response (Hex): {toHexString(response)}")
    print(f"Response (ASCII): {''.join([chr(byte) for byte in response if 32 <= byte <= 126])}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")
    # Filter to get only the digits from the first 16 bytes
    response_digits = ''.join([chr(byte) for byte in response[:16] if chr(byte).isdigit()])
    print(f"Response (Digits): {response_digits}")
    
    # Trigger the Chrome function with the card data
    if len(response_digits)>4:
        chrome(response_digits,"chingup")
        done = True  # Mark as done after processing
    
    return response, sw1, sw2

def send_apdus(connection, apdu):
    response, sw1, sw2 = connection.transmit(apdu)
    print(f"APDU: {toHexString(apdu)}")
    print(f"Response (Hex): {toHexString(response)}")
    print(f"Response (ASCII): {''.join([chr(byte) for byte in response if 32 <= byte <= 126])}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")
    
    return response, sw1, sw2

def chrome(card_data,type):
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
        # Define the path to the secret file
        secret_file_path = os.path.expanduser("~/.hidden_dir/secret_file.txt")

        # Read the file contents
        with open(secret_file_path, 'r') as file:
            secret_data = file.read()

        # Split the secret data into pos_id and brn
        secret_lines = secret_data.strip().splitlines()
        pos_id = secret_lines[0].split(': ')[1]
        brn = secret_lines[1].split(': ')[1]
        print(brn)
        print(pos_id)

        # JavaScript code to trigger the card check with simulated card data
        js_code = f"""
        window.cardProcessed("{card_data}", "{type}", "{pos_id}", "{brn}");
        """
        # Execute the JavaScript code
        
        result = tab.Runtime.evaluate(expression=js_code)
        print("JavaScript executed:", result)
        
        # Optional: Close the tab connection
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")



# Create and start threads for smartcard processing and keyboard listening
smartcard_thread = threading.Thread(target=process_card)
#keyboard_thread = threading.Thread(target=start_keyboard_listener)

smartcard_thread.start()
#keyboard_thread.start()

smartcard_thread.join()
#keyboard_thread.join()
