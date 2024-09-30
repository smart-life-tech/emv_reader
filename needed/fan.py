import serial
import time
import RPi.GPIO as GPIO
import os
import re
# UART Setup (modify as per your battery module documentation)
uart_port = '/dev/serial1'  # This should match the UART port for your battery
baud_rate = 9600

# Serial object, initialized to None
ser = None

# Try to open the serial port
try:
    ser = serial.Serial(uart_port, baud_rate, timeout=1)
    print(f"Successfully opened serial port {uart_port}")
except serial.SerialException as e:
    print(f"Could not open serial port {uart_port}: {e}")
except FileNotFoundError as e:
    print(f"Serial port {uart_port} not found: {e}")
except Exception as e:
    print(f"General error: {e}")
# GPIO Setup for fan
FAN_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

class UPS2:
    def __init__(self,port):
        self.ser  = serial.Serial(port,9600)        
        
    def get_data(self,nums):
        while True:
            self.count = self.ser.inWaiting()
            
            if self.count !=0:
                self.recv = self.ser.read(nums)
                return self.recv
    
    def decode_uart(self):
        self.uart_string = self.get_data(100)
#    print(uart_string)
        self.data = self.uart_string.decode('ascii','ignore')
#    print(data)
        self.pattern = r'\$ (.*?) \$'
        self.result = re.findall(self.pattern,self.data,re.S)
    
        self.tmp = self.result[0]
    
        self.pattern = r'SmartUPS (.*?),'
        self.version = re.findall(self.pattern,self.tmp)
    
        self.pattern = r',Vin (.*?),'
        self.vin = re.findall(self.pattern,self.tmp)
        
        self.pattern = r'BATCAP (.*?),'
        self.batcap = re.findall(self.pattern,self.tmp)
        
        self.pattern = r',Vout (.*)'
        self.vout = re.findall(self.pattern,self.tmp)

        return self.version[0],self.vin[0],self.batcap[0],self.vout[0]
    
# Function to read battery data over UART
def read_battery_data():
    i=1
    print("This is UPS v2 class file")
    test = UPS2("/dev/ttyS0")
    version,vin,batcap,vout = test.decode_uart()
    print("--------------------------------")
    print("       UPS Version:"+version)
    print("--------------------------------")
    version,vin,batcap,vout = test.decode_uart()
    print("-%s-" %i)
       
    if vin == "NG":
        print("USB input adapter : NOT connected!")
    else:
        print("USB input adapter : connected!")
    print("Battery Capacity: "+batcap+"%")
    print("UPS Output Voltage: "+vout+" mV")
    print("\n")
       
   
    if ser is None:
        print("Serial port is not available, skipping battery read.")
        return None

    try:
        if ser.in_waiting > 0:
            
            line = ser.readline().decode('utf-8').strip()
            print("read data",line)
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
        if temp_celsius >= 52:
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
        # battery_data = read_battery_data()  # Reading battery data
        # if battery_data:
        #     print(f"Battery: {battery_data}")

        temp_celsius = read_temperature()  # Reading temperature
        print("temp read", temp_celsius)
        if temp_celsius:
            control_fan(temp_celsius)  # Controlling the fan

        time.sleep(5)  # Delay for 5 seconds before the next iteration

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    GPIO.cleanup()
    if ser is not None:
        ser.close()
    print("Cleanup complete")
