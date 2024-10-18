#sudo nano /home/chingup/emv_reader/internet.sh
#!/bin/bash
# Wait 10 seconds to ensure network is ready
#sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Play the custom video
#omxplayer --no-keys -o local /path/to/your/video.mp4
# Wait for video to finish (if needed)
#sudo cp /home/chingup/Downloads/main_logo_trans_network-500px.png /usr/share/plymouth/themes/my-splash/
#sudo systemctl restart readwrite.service
#journalctl -u readwrite.service -f
# chromium-browser --remote-debugging-port=9222  https://chingup.com/rpi_pos/
#wait 
#sleep 1

truncate -s 0 /home/chingup/emv_reader/pic.txt
truncate -s 0 /home/chingup/internet_check.log
python /home/chingup/emv_reader/pic.py &
#!/bin/bash
#chromium-browser --start-fullscreen /home/chingup/emv_reader/start.html &
 
# Check if internet is available by pinging google.com (no https://)
wget -q --spider http://google.com 
sleep 8
# Check the exit status of the ping command
# If the exit status is 0, internet is available
if [ $? -eq 0 ]; then
    echo "Internet is available" >> /home/chingup/internet_check.log
    
    # Open the online page
    #pkill chromium-browser
    #sleep 5
    chromium-browser --remote-debugging-port=9222 --kiosk --noerrdialogs --disable-infobars https://chingup.com/rpi_pos/
    echo "done" >> /home/chingup/emv_reader/pic.txt
else
    echo "No internet connection" >> /home/chingup/internet_check.log
    # Open the offline page
    #pkill chromium-browser
    
    chromium-browser --kiosk --start-fullscreen --noerrdialogs --disable-infobars --incognito /home/chingup/emv_reader/html2/index.html
    echo "done" >> /home/chingup/emv_reader/pic.txt
fi
sleep 5
echo "doneggggg" >> /home/chingup/emv_reader/pic.txt
sleep 6
#DISPLAY=:0 XAUTHORITY=/home/chingup/.Xauthority /usr/bin/python3 /home/chingup/emv_reader/needed/screenControl.py &
echo "screen control started suceesfully" >> /home/chingup/internet_check.log
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
#@sh -c 'sudo PYTHONPATH=$PYTHONPATH:/home/chingup/.local/lib/python3.9/site-packages python3 /home/chingup/needed/kills.py'
# @lxpanel --profile LXDE-pi
# @pcmanfm --desktop --profile LXDE-pi
# @xscreensaver -no-splash
# #@chromium-browser --kiosk --remote-debugging-port=9222 http://chingup.com/rpi_pos
# #@sh -c 'sleep 10 && chromium-browser --kiosk --remote-debugging-port=9222 http://chingup.com/rpi_pos'
# #@chromium-browser --kiosk chingup.com/rpi_pos --remote-debugging-port=9222
# #@sh -c 'sudo PYTHONPATH=$PYTHONPATH:/home/chingup/.local/lib/python3.9/site-packages python3 /home/chingup/latest.py'
# #@sh -c 'sudo PYTHONPATH=$PYTHONPATH:/home/chingup/.local/lib/python3.9/site-packages python3 /home/chingup/needed/kills.py'
# @/home/chingup/emv_reader/internet.sh
# @sh -c 'sudo DISPLAY=:0 XAUTHORITY=/home/chingup/.Xauthority python3 /home/chingup/emv_reader/needed/screenControl.py'
# @sh -c 'sudo DISPLAY=:0 XAUTHORITY=/home/chingup/.Xauthority python /home/chingup/emv_reader/needed/screenControl.py >> /home/chingup/screenControl.log 2>&1'
