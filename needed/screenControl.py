import os
import time
from evdev import InputDevice, categorize, ecodes
status=False
# Path to the input device (you may need to adjust this)
device_path = '/dev/input/event3'

# Function to turn off the screen
def turn_off_screen():
    #os.system('xrandr --output HDMI-1 --off')
    print("turning off screen")

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
    time.sleep(20)
    os.system('xrandr --output HDMI-1 --mode 1920x1080')

# Monitor for inactivity
def monitor_inactivity():
    last_activity_time = time.time()
    device = InputDevice(device_path)
    print("device types: ", device)
    for event in device.read_loop():
        if event.type == ecodes.EV_ABS and event.code in [ecodes.ABS_MT_POSITION_X, ecodes.ABS_MT_POSITION_Y]:
            last_activity_time = time.time()
            print("pressed")
            turn_on_screen()
            status=False
            break

        if time.time() - last_activity_time > 30 and status == False:  # 0.5 minutes
            turn_off_screen()
            print("turning off screen")
            status = True
        print("time now: ", time.time())
        print("last activity time: ", last_activity_time)
        print("status: ",time.time() - last_activity_time)
        time.sleep(1)  # Add a short delay to prevent CPU hogging

if __name__ == "__main__":
    while True:
        monitor_inactivity()
        #testOnOff()
