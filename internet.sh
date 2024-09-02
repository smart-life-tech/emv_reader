#!/bin/bash
# C. Configure the Script to Run on Boot
# Edit rc.local:
# bash
# A. Install network-manager
# Use network-manager to handle network connections interactively.

# bash
# Copy code
# sudo apt-get update
# sudo apt-get install network-manager
# Copy code
# sudo nano /etc/rc.local
# Add the script before the exit 0 line:
# bash
# Copy code
# /home/pi/check_internet.sh &
# Save and exit: Press CTRL + X, then Y, and ENTER to save and exit.
# D. Ensure NetworkManager Handles Connections
# Make sure that network-manager is managing the network interfaces:

# bash
# Copy code
# sudo systemctl enable NetworkManager
# sudo systemctl start NetworkManager
# Summary:
# This approach allows the system to dynamically prompt for the SSID and password at boot if there is no internet connection, without hard-coding the credentials. Users can interactively connect to a Wi-Fi network, and the Raspberry Pi will proceed to kiosk mode if the connection is successful.

You said:
startx -- -nocursor

# Check for internet connection
if ! ping -c 1 google.com &> /dev/null
then
    # If no internet, bring up network manager to connect to Wi-Fi
    sudo nmcli dev wifi list

    echo "No internet connection detected. Please connect to a Wi-Fi network."
    echo "Enter the SSID of the Wi-Fi network you want to connect to:"
    read ssid

    echo "Enter the password for $ssid:"
    read -s password

    # Attempt to connect to the entered Wi-Fi network
    sudo nmcli dev wifi connect "$ssid" password "$password"

    # Check connection again
    if ! ping -c 1 google.com &> /dev/null
    then
        echo "Failed to connect to the internet. Please check your credentials and try again."
        exit 1
    else
        echo "Connected to $ssid successfully!"
    fi
fi

# Start the X server and launch Chromium in kiosk mode
startx -- -nocursor &

# Give X server time to start before launching Chromium
sleep 5

# Launch Chromium in kiosk mode
chromium-browser --kiosk --noerrdialogs --disable-infobars --incognito http://your-pos-app-url &

# Launch the Python script
python3 /path/to/your_script.py &
