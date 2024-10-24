import serial
import time
import re
from time import sleep
import requests
import os,sys
# Redirect standard output to null
#sys.stdout = open(os.devnull, 'w')
payload = {
        
    }
class UPS2:
    def __init__(self,port):
        self.ser  = serial.Serial(port,9600)   
        self.ser.timeout=10     
        
    def get_data(self,nums):
        while True:
            self.count = self.ser.inWaiting()
            if self.count !=0:
                self.recv = self.ser.read(nums)
                print(self.recv)
                sleep(1)
                return self.recv
                
        
    
    def decode_uart(self):
        self.uart_string = self.get_data(100)
        print("received :",self.uart_string)
        self.data = self.uart_string.decode('ascii','ignore')
        print(self.data)
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
    print("This is UPS v3 class file")
    test = UPS2("/dev/ttyS0")
    print("reading done")
    version,vin,batcap,vout = test.decode_uart()
    print("--------------------------------")
    print("       UPS Version:"+version)
    print("--------------------------------")
    version,vin,batcap,vout = test.decode_uart()
    print("-%s-" %i)
       
       
    if vin == "NG":
        print("USB input adapter : NOT connected!")
        payload = {
        'Battery': batcap,
        'Status': 'dis-connected'
    }
    else:
        print("USB input adapter : connected!")
        payload = {
        'Battery': batcap,
        'Status': 'connected' 
    }
    print("Battery Capacity: "+batcap+"%")
    print("UPS Output Voltage: "+vout+" mV")
    print("\n")
       
     # Post data to Flask endpoint
    url = 'http://localhost:5000/battery'  # Update with your Flask server URL
    
    try:
        response = requests.post(url, json=payload)
        print(f"Data posted to {url}, response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to post data: {e}")
    

try:
    while True:
        battery_data = read_battery_data()  # Reading battery data
        if battery_data:
            print(f"Battery: {battery_data}")
        time.sleep(5)  # Delay for 5 seconds before the next iteration

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    print("Cleanup complete")
