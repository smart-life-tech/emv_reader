import sys
from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.Exceptions import CardConnectionException

def connect_to_card():
    r = readers()
    if len(r) == 0:
        raise Exception("No smart card readers found")

    reader = r[0]
    connection = reader.createConnection()
    connection.connect()
    return connection

def write_data(connection, data, start_address=0):
    for i, byte in enumerate(data):
        write_command = [0xA0, 0x00, start_address + i, byte]
        connection.transmit(write_command)

def read_data(connection, length, start_address=0):
    read_command = [0xB0, 0x00, start_address, length]
    data, sw1, sw2 = connection.transmit(read_command)
    return data

def main():
    unique_string = "YOUR_UNIQUE_STRING"
    start_address = 0  # Address to start writing the string

    connection = connect_to_card()

    try:
        # Convert string to bytes
        data = toBytes(unique_string)

        # Write data to card
        write_data(connection, data, start_address)
        print(f"Data written to card: {unique_string}")

        # Read data from card
        read_length = len(data)
        read_data_bytes = read_data(connection, read_length, start_address)
        read_string = ''.join(chr(b) for b in read_data_bytes)
        print(f"Data read from card: {read_string}")

    except CardConnectionException as e:
        print(f"Connection error: {e}")
        sys.exit()

if __name__ == "__main__":
    main()
