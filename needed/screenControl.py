import os
import time
from evdev import InputDevice, categorize, ecodes

# Path to the input device (you may need to adjust this)
device_path = '/dev/input/event0'

# Function to turn off the screen
def turn_off_screen():
    os.system('xrandr --output HDMI-1 --off')

# Function to turn on the screen
def turn_on_screen():
    time.sleep(5)
    print("turing on screen")
    os.system('xrandr --output HDMI-1 --mode 1920x1080')
    time.sleep(4)
    os.system('xrandr --output HDMI-1 --mode 1920x1080')

def testOnOff():
    print("turning off screen")
    os.system('xrandr --output HDMI-1 --off')
    time.sleep(5)
    print("turing on screen")
    os.system('xrandr --output HDMI-1 --mode 1920x1080')
    time.sleep(4)
    os.system('xrandr --output HDMI-1 --mode 1920x1080')
# Monitor for inactivity
def monitor_inactivity():
    last_activity_time = time.time()
    device = InputDevice(device_path)
    print("device types: ",device)
    for event in device.read_loop():
        print( "event types: ",event.type)
        if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
            last_activity_time = time.time()
            print("preesed")
            #turn_on_screen()

        if time.time() - last_activity_time > 30:  # 5 minutes
            #turn_off_screen()
            print("turning off screen")

if __name__ == "__main__":
    monitor_inactivity()
    #testOnOff()
