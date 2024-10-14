import os
import time
from evdev import InputDevice, categorize, ecodes, list_devices
import threading
isScreenOn=True
shared_data = {
    'last_activity_time': time.time(),
    'status': False
}
status=False

# Path to the input device (you may need to adjust this)
device_path = '/dev/input/event2'
device = InputDevice(device_path)
# Vendor, Product, and Name attributes to match
VENDOR_ID = "0x484"     # Modify as per your device
PRODUCT_ID = "0x5750"   # Modify as per your device
DEVICE_NAME = "QDTECH̐MPI700 MPI7002"  # Modify as per your device

# Function to turn off the screen
# Function to find the correct input device dynamically
def find_input_device():
    devices = [InputDevice(dev) for dev in list_devices()]
    for device in devices:
        # Get device info using 'evdev' attributes
        if (device.info.vendor == int(VENDOR_ID, 16) and
            device.info.product == int(PRODUCT_ID, 16) and
            device.name == DEVICE_NAME):
            print(f"Device found: {device.path}")
            return device.path
    return None
def turn_off_screen():
    os.system('xrandr --output HDMI-1 --off')
    print("turning off screen")

# Function to turn on the screen
def turn_on_screen():
    #time.sleep(1)
    print("turing on screen")
    os.system('xrandr --output HDMI-1 --mode 1920x1080')
    time.sleep(1)
    #os.system('xrandr --output HDMI-1 --mode 1920x1080')

def testOnOff():
    print("turning off screen")
    os.system('xrandr --output HDMI-1 --off')
    time.sleep(5)
    print("turing on screen")
    os.system('xrandr --output HDMI-1 --mode 1920x1080')
    time.sleep(20)
    os.system('xrandr --output HDMI-1 --mode 1920x1080')

# Monitor for inactivity
def monitor_inactivity(shared_data):
    global status
    global status
    input_device_path = find_input_device()
    if not input_device_path:
        print("Input device not found")
        return
    
    device = InputDevice(input_device_path)
    print("device types: ", device_path)
    
    while True:
        last_activity_time = time.time()
        print("device types: ", device)
        for event in device.read_loop():
            if event.type == ecodes.EV_ABS and event.code in [ecodes.ABS_MT_POSITION_X, ecodes.ABS_MT_POSITION_Y]:
                last_activity_time = time.time()
                status=False
                shared_data['status'] = False
                shared_data['last_activity_time'] = time.time()
                print("pressed")
                if isScreenOn:
                    turn_on_screen()
                    isScreenOn=False
                break

            if time.time() - last_activity_time > 30 and status == False:  # 0.5 minutes
                turn_off_screen()
                print("turning off screen")
                status = True
                shared_data['status'] = True
                isScreenOn=True
                
            #print("time now: ", time.time())
            #print("last activity time: ", last_activity_time)
            #print("status: ",time.time() - last_activity_time)
            time.sleep(0.1)  # Add a short delay to prevent CPU hogging
def perform_other_tasks(shared_data):
    while True:
        if time.time() - shared_data['last_activity_time'] > 30 and not shared_data['status']:  # 0.5 minutes
            turn_off_screen()
            print("Turning off screen")
            shared_data['status'] = True

        if not shared_data['status']:
            print("The screen has been turned on")
        else:
            print("The screen is off")
        time.sleep(0.1)  # Add a short delay to prevent CPU hogging
        
if __name__ == "__main__":
    # Run monitor_inactivity in a separate thread
    monitor_thread = threading.Thread(target=monitor_inactivity, args=(shared_data,))
    monitor_thread.start()
    perform_other_tasks(shared_data)
    #testOnOff()
