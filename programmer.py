from smartcard.System import readers
from smartcard.util import toHexString
import time

def send_apdus(connection, apdu):
    response, sw1, sw2 = connection.transmit(apdu)
    print(f"APDU: {toHexString(apdu)}")
    print(f"Response (Hex): {toHexString(response)}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")
    return response, sw1, sw2

def write_data_to_card(connection, card_id):
    try:
        # Initialize card (using an APDU command)
        init_apdu = [0xFF, 0xA4, 0x00, 0x00, 0x01, 0x06]  
        send_apdus(connection, init_apdu)
        time.sleep(1)
        
        # Convert card_id to bytes (split into two 8-byte chunks if needed)
        id_bytes = [int(card_id[i:i+2]) for i in range(0, len(card_id), 2)]
        
        # Assuming the card can handle 8 bytes at a time, we will split the ID into two parts
        for i in range(0, len(id_bytes), 8):
            chunk = id_bytes[i:i+8]
            write_command = [0xFF, 0xA4, 0x00, 0x00, len(chunk)] + chunk
            
            # Write the chunk to the card
            response, sw1, sw2 = send_apdus(connection, write_command)
            
            # Check if the write was successful
            if sw1 == 0x90 and sw2 == 0x00:
                print(f"Card ID chunk {toHexString(chunk)} written successfully.")
            else:
                print(f"Failed to write Card ID chunk {toHexString(chunk)}. Status Word: {sw1:02X} {sw2:02X}")
    except Exception as e:
        print(f"An error occurred during the write operation: {e}")

def main():
    # Prompt the user for an initial 16-digit ID number
    card_id = input("Enter the initial 16-digit ID number: ")

    if len(card_id) != 16 or not card_id.isdigit():
        print("Invalid ID. Please enter exactly 16 digits.")
        return

    try:
        # List available readers
        reader_list = readers()
        if not reader_list:
            raise Exception("No readers available.")

        # Use the first available reader
        reader = reader_list[0]
        print(f"Using reader: {reader}")

        while True:
            # Wait for a new card to be inserted
            print("Please insert a card...")
            connection = reader.createConnection()
            connection.connect()

            # Increment the card ID for each new card
            card_id = str(int(card_id) + 1).zfill(16)

            # Write data to the card using the incremented card ID
            write_data_to_card(connection, card_id)
            print(card_id)
            
            # Prompt for the next card
            input("Remove the card and press Enter to continue, or Ctrl+C to exit.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
