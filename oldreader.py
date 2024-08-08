import sys
import time
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException

def connect_to_card():
    try:
        r = readers()
        print(f"Available readers: {r}")

        if len(r) == 0:
            raise Exception("No smart card readers found")

        reader = r[0]
        connection = reader.createConnection()
        connection.connect()

        atr = connection.getATR()
        print(f"Card ATR: {toHexString(atr)}")

        return connection

    except CardConnectionException as e:
        print(f"Connection error: {e}")
        sys.exit()

def send_apdu(connection, apdu):
    try:
        response, sw1, sw2 = connection.transmit(apdu)
        print(f"Response: {toHexString(response)}, SW1: {sw1}, SW2: {sw2}")
        return response, sw1, sw2
    except Exception as e:
        print(f"APDU transmission error: {e}")
        sys.exit()

if __name__ == "__main__":
    connection = connect_to_card()

    # Replace with your custom APDU command
    custom_apdu = [0x00, 0xA4, 0x04, 0x00, 0x00]
    response, sw1, sw2 = send_apdu(connection, custom_apdu)
    
    # Additional custom APDU commands can be added here
