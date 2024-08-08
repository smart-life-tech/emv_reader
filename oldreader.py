from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.Exceptions import CardConnectionException
import time

# Define the unique identifier
unique_identifier = "123456789ABCDEF"

def connect_to_reader():
    # Get the list of available readers
    available_readers = readers()
    if len(available_readers) == 0:
        print("No readers available")
        return None
    print("Available readers:", available_readers)
    
    # Use the first reader
    reader = available_readers[0]
    connection = reader.createConnection()

    # Attempt to connect with retries
    retries = 3
    for attempt in range(retries):
        try:
            connection.connect()
            return connection
        except CardConnectionException as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Wait a bit before retrying
    print("Failed to connect to the card.")
    return None

def write_identifier(connection, identifier):
    # Convert the identifier to bytes
    identifier_bytes = toBytes(identifier)
    
    # Define APDU command to write data to the card (example)
    write_command = [0x00, 0xD6, 0x00, 0x00, len(identifier_bytes)] + identifier_bytes
    
    # Send the command to the card
    response, sw1, sw2 = connection.transmit(write_command)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Identifier written successfully")
    else:
        print(f"Failed to write identifier: {sw1:02X} {sw2:02X}")

def read_identifier(connection):
    # Define APDU command to read data from the card (example)
    read_command = [0x00, 0xB0, 0x00, 0x00, 0x10]  # Adjust the length as necessary
    
    # Send the command to the card
    response, sw1, sw2 = connection.transmit(read_command)
    if sw1 == 0x90 and sw2 == 0x00:
        identifier = toHexString(response)
        print("Identifier read from card:", identifier)
        return identifier
    else:
        print(f"Failed to read identifier: {sw1:02X} {sw2:02X}")
        return None

def main():
    connection = connect_to_reader()
    if connection:
        write_identifier(connection, unique_identifier)
        read_identifier(connection)

if __name__ == "__main__":
    main()
