import os
import time
import psutil
import subprocess
old=''
def monitor_processes():    
    # List of unauthorized applications that should trigger the self-destruct
    unauthorized_processes = ['firefox', '0x01001dbf  0 raspberrypi chingup']  # 'chromium',  'lxterminal',Include web browsers, terminal, and file explorer
    
    while True:
        old = subprocess.check_output(['ps', '-A'], text=True).splitlines()
        time.sleep(5)  # Adjust the frequency of checks as needed
        
        # Get the list of all running processes
        #process_list = subprocess.getoutput('ps -A')#'ps -A'
        process_list = subprocess.check_output(['ps', '-A'], text=True).splitlines()
        window_list = subprocess.check_output(['wmctrl', '-l'], text=True).splitlines()
        print(window_list)
        
        # Check if any unauthorized process is running
        for unauthorized_process in unauthorized_processes:
            print(unauthorized_process)
            if any(unauthorized_process in process for process in window_list):
                self_destruct(f"Unauthorized process detected: {unauthorized_process}")
                break

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
    monitor_processes()
