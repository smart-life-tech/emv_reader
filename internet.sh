#sudo nano /home/pi/kiosk-check-internet.sh
#!/bin/bash

# Check for internet connection
wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    # Internet is available, boot into the online page
    chromium-browser --remote-debugging-port=9222 --kiosk --noerrdialogs --disable-infobars  https://chingup.com/rpi_pos/
else
    # No internet connection, boot into the offline page
    chromium-browser --kiosk --noerrdialogs --disable-infobars --incognito /home/pi/emv_reader/html2/index.html
fi
# Make the script executable:
# bash
# Copy code
# sudo chmod +x /home/pi/kiosk-check-internet.sh
# 2. Modify the autostart file to run the script at boot
# Edit the autostart file:
# bash
# Copy code
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Add the following line to run your script on boot:
# bash
# Copy code
# @/home/pi/kiosk-check-internet.sh
# 3. Reboot and test
# Reboot your Raspberry Pi:

# bash
# Copy code
# sudo reboot