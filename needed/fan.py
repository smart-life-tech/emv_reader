import serial
import time
import RPi.GPIO as GPIO
import os,sys
# Redirect standard output to null
sys.stdout = open(os.devnull, 'w')
# GPIO Setup for fan
FAN_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

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
        if temp_celsius >= 75:
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
        temp_celsius = read_temperature()  # Reading temperature
        print("temp read", temp_celsius)
        if temp_celsius:
            control_fan(temp_celsius)  # Controlling the fan

        time.sleep(5)  # Delay for 5 seconds before the next iteration

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    GPIO.cleanup()
    print("Cleanup complete")
