import serial

# Open the serial port (adjust '/dev/ttyUSB0' and baudrate as needed)
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            print("Data received:", data)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
