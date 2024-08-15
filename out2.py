from smartcard.System import readers
from smartcard.util import toHexString

# Select the first reader
r = readers()
print("Using reader:", r)
reader = r[0]

# Connect to the card
connection = reader.createConnection()
connection.connect()

# Function to read memory card
def read_memory_card(byte_address, mem_length):
    command = [0x01, 0xA0, 0x00, 0x05, 0xFF, byte_address >> 8, byte_address & 0xFF, mem_length]
    response, sw1, sw2 = connection.transmit(command)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Data read from memory card:", toHexString(response))
    else:
        print(f"Error reading memory card: SW1={sw1:02X}, SW2={sw2:02X}")

# Function to write memory card
def write_memory_card(byte_address, data):
    mem_length = len(data)
    command = [0x01, 0xA0, 0x00, 0x05 + mem_length, 0xFF, byte_address >> 8, byte_address & 0xFF, mem_length] + data
    response, sw1, sw2 = connection.transmit(command)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Data written to memory card successfully.")
    else:
        print(f"Error writing to memory card: SW1={sw1:02X}, SW2={sw2:02X}")

# Example usage
byte_address = 0x0000  # Starting address
mem_length = 16  # Length of data to read/write

# Read data from memory card
read_memory_card(byte_address, mem_length)

# Write data to memory card
data_to_write = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10]
write_memory_card(byte_address, data_to_write)
