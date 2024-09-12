#sudo nano /home/chingup/emv_reader/internet.sh
#!/bin/bash
# Wait 10 seconds to ensure network is ready
sleep 10

# Check if internet is available by pinging google.com (no https://)
ping -c 1 google.com > /home/chingup/internet_check.log 2>&1

if [ $? -eq 0 ]; then
    echo "Internet is available" >> /home/chingup/internet_check.log
    # Open the online page
    chromium-browser --remote-debugging-port=9222 --kiosk --noerrdialogs --disable-infobars https://chingup.com/rpi_pos/
else
    echo "No internet connection" >> /home/chingup/internet_check.log
    # Open the offline page
    chromium-browser --kiosk --noerrdialogs --disable-infobars --incognito /home/chingup/emv_reader/html2/index.html
fi


# Make the script executable:
# bash
# Copy code
# sudo chmod +x  internet.sh
# 2. Modify the autostart file to run the script at boot
# Edit the autostart file:
# bash
# Copy code /home/chingup/emv_reader/internet.sh
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Add the following line to run your script on boot:
# bash
# Copy code
# @/home/chingup/emv_reader/internet.sh
# 3. Reboot and test
# Reboot your Raspberry Pi:

# bash
# Copy code
# sudo reboot