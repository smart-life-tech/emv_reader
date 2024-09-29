import serial
import time
import RPi.GPIO as GPIO
import os
# UART Setup (modify as per your battery module documentation)
uart_port = '/dev/ttyUSB0'  # This should match the UART port for your battery
baud_rate = 9600
ser = serial.Serial(uart_port, baud_rate, timeout=1)

# GPIO Setup for fan
FAN_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

# Function to read battery data over UART
def read_battery_data():
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Battery data: {line}")
                return line
    except serial.SerialException as e:
        print(f"Error reading battery data: {e}")
    except Exception as e:
        print(f"General error: {e}")
    return None

# Function to read temperature data
def read_temperature():
    try:
        # Read CPU temperature
        temp = os.popen("vcgencmd measure_temp").readline()
        # Extract temperature value
        temp_celsius = float(temp.replace("temp=", "").replace("'C\n", ""))
        return temp_celsius
    except Exception as e:
        print(f"Error reading CPU temperature: {e}")
        return None

# Function to control fan based on temperature
def control_fan(temp_celsius):
    try:
        if temp_celsius >= 82:
            GPIO.output(FAN_PIN, GPIO.HIGH)  # Turn on the fan
            print("Fan turned ON")
        else:
            GPIO.output(FAN_PIN, GPIO.LOW)  # Turn off the fan
            print("Fan turned OFF")
    except Exception as e:
        print(f"Error controlling fan: {e}")

# Main loop
try:
    while True:
        battery_data = read_battery_data()  # Reading battery data
        if battery_data:
            print(f"Battery: {battery_data}")

        temp_celsius = read_temperature()  # Reading temperature
        print("temp read",temp_celsius)
        if temp_celsius:
            control_fan(temp_celsius)  # Controlling the fan

        time.sleep(5)  # Delay for 5 seconds before the next iteration

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    GPIO.cleanup()
    ser.close()
    print("Cleanup complete")
