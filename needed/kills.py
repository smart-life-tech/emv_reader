import os
import time
import psutil
import subprocess
old=''
def get_open_windows():
    try:
        # Get a list of all open windows
        windows = subprocess.check_output(['wmctrl', '-l'], text=True).splitlines()
        filtered_windows = [window for window in windows if  'raspberrypi chingup@raspberrypi' not in window]
        return filtered_windows
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

def detect_unauthorized_windows(unauthorized_processes):
    window_list = get_open_windows()
    print(window_list)
    for process in unauthorized_processes:
        if any(process in window for window in window_list):
            if any(process == window for window in window_list):
                print(f"Specific unauthorized window detected: {process}")
                self_destruct(f"Unauthorized process detected: {process}")
                break

def monitor_processes():    
    # List of unauthorized applications that should trigger the self-destruct
    # Example usage
    unauthorized_processes = [ 'raspberrypi chingup']
    # 'chromium',  'lxterminal',Include web browsers, terminal, and file explorer
    detect_unauthorized_windows(unauthorized_processes)


def self_destruct(message):
    print("Wipe critical data",message)
    #os.system('rm -rf /path/to/critical/data')
    
    # Optionally, format the SD card
    # os.system('sudo mkfs.ext4 /dev/mmcblk0p1')
    
    print("Shutdown the system")
    #os.system('sudo shutdown -h now')
    #os.system('sudo reboot')
    time.sleep(1)  # Adjust the frequenc
    

if __name__ == "__main__":
    while True:
        monitor_processes()
        time.sleep(5)
