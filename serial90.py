import serial

# Replace with the correct serial port on your Raspberry Pi
ser = serial.Serial(
    port='ttyAMA0',  # or '/dev/ttyACM0' depending on your device
    baudrate=9600,        # Adjust if your reader uses a different baud rate
    timeout=1             # Timeout for reads
)

print("Waiting for card swipe...")

try:
    while True:
        if ser.in_waiting > 0:
            card_data = ser.read(ser.in_waiting).decode('ascii').strip()
            if card_data:
                print(f'Card Data: {card_data}')
except KeyboardInterrupt:
    print("\nProgram terminated by user.")
finally:
    ser.close()
