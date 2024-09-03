import os
import time
import subprocess

def monitor_processes():
    # List of authorized processes that are allowed to run
    authorized_processes = ['transaction_service', 'other_allowed_process']
    
    # List of unauthorized applications that should trigger the self-destruct
    unauthorized_processes = ['chromium', 'firefox', 'lxterminal', 'pcmanfm']  # Include web browsers, terminal, and file explorer
    
    while True:
        time.sleep(5)  # Adjust the frequency of checks as needed
        
        # Get the list of all running processes
        process_list = subprocess.getoutput('ps -A')#'ps -A'
        print(process_list[1])
        
        # Check if any unauthorized process is running
        if any(unauthorized_process in process_list for unauthorized_process in unauthorized_processes):
            self_destruct()
        
        # Optional: Check if only authorized processes are running
        if not all(auth_process in process_list for auth_process in authorized_processes):
            self_destruct()

def self_destruct():
    print("Wipe critical data)")
    #os.system('rm -rf /path/to/critical/data')
    
    # Optionally, format the SD card
    # os.system('sudo mkfs.ext4 /dev/mmcblk0p1')
    
    print("Shutdown the system")
    #os.system('sudo shutdown -h now')
    time.sleep(5)  # Adjust the frequenc
    

if __name__ == "__main__":
    monitor_processes()
