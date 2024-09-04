import os
import time
import psutil
import subprocess
old=''
def monitor_processes():    
    # List of unauthorized applications that should trigger the self-destruct
    unauthorized_processes = ['firefox', 'pcmanfm']  # 'chromium',  'lxterminal',Include web browsers, terminal, and file explorer
    
    while True:
        old = subprocess.check_output(['ps', '-A'], text=True).splitlines()
        time.sleep(5)  # Adjust the frequency of checks as needed
        
        # Get the list of all running processes
        #process_list = subprocess.getoutput('ps -A')#'ps -A'
        process_list = subprocess.check_output(['ps', '-A'], text=True).splitlines()
        # Convert the lists to sets for comparison
        old_set = set(old)
        new_set = set(process_list)

        # Find the differences
        added_processes = new_set - old_set  # Processes in new_set but not in old_set
        removed_processes = old_set - new_set  # Processes in old_set but not in new_set

        # Print the differences
        print("Added processes:")
        for process in added_processes:
            print(process)

        print("\nRemoved processes:")
        for process in removed_processes:
            print(process)
        #print(process_list)
        
        # Check if any unauthorized process is running
        # Check if any unauthorized process is running
        for unauthorized_process in unauthorized_processes:
            print(unauthorized_process)
            if any(unauthorized_process in process for process in process_list):
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
