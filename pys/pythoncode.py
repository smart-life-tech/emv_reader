from flask import Flask, request, jsonify,render_template

from flask_cors import CORS
import os
import subprocess
import time
app = Flask(__name__,static_folder='static')
CORS(app)  # Enable CORS for all routes
# File path for read/write operations
file_path = '/home/chingup/emv_reader/pys/data.txt'
#file_path='pys/data.txt'
 # Define the path to the secret file
secret_file_path = os.path.expanduser("~/.hidden_dir/secret_file.txt")
#secret_file_path = os.path.expanduser("C:/Users/USER/Documents/raspberrypi/emv_reader/testing/data.txt")
battery_data = {
    'Battery: ': 85,  # Example battery level
    'Status: ': 'charging'  # Example charging status
}

@app.route('/battery', methods=['POST'])
def battery_status():
    data = request.get_json()
    battery_data['Battery'] = data.get('Battery')
    battery_data['Status'] = data.get('Status')
    print(f"Battery Level: {battery_data['Battery']}, Charging Status: {battery_data['Status']}")
    return jsonify({"message": "Data received"}), 200

@app.route('/battery', methods=['GET'])
def get_battery_status():
    return jsonify(battery_data), 200


@app.route('/offline')
def home():
    return render_template('index.html')

@app.route('/activate')
def activate():
    return render_template('activate.html')

@app.route('/settings')
def settings():
    return render_template('checkint.html')
@app.route('/api/read', methods=['GET', 'OPTIONS'])
def read_file():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return jsonify({"status": "success", "content": content}), 200
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404

@app.route('/api/write', methods=['POST'])
def write_file():
    data = request.json.get('content')
    if data:
        with open(file_path, 'w') as file:
            file.write(data)
        return jsonify({"status": "success", "message": "Content written to file"}), 200
    else:
        return jsonify({"status": "error", "message": "No content to write"}), 400

@app.route('/api/reboot', methods=['POST', 'OPTIONS'])
def reboot():
    if 1:
        print("rebooted")
        os.system('sudo reboot')
        return jsonify({"status": "success", "content": "rebooted"}), 200
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404

@app.route('/api/shutdown', methods=['POST', 'OPTIONS'])
def shutdown():
    if 1:
        print("shutdown")
        os.system('sudo shutdown -h now')
        
        return jsonify({"status": "success", "content": "shutdown"}), 200
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404   

@app.route('/api/get_brn',methods=['GET', 'OPTIONS'])
def get_brn():
    if os.path.exists(secret_file_path):
        with open(secret_file_path, 'r') as file:
            content = file.read()
        secret_lines = content.strip().splitlines()
        pos_id = secret_lines[0].split(': ')[1]
        brn = secret_lines[1].split(': ')[1]
        return jsonify({"status": "success", "content": brn}), 200
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404
@app.route('/api/get_pos_id',methods=['GET', 'OPTIONS'])
def get_pos_id():
    if os.path.exists(secret_file_path):
        with open(secret_file_path, 'r') as file:
            content = file.read()
        secret_lines = content.strip().splitlines()
        pos_id = secret_lines[0].split(': ')[1]
        brn = secret_lines[1].split(': ')[1]
        return jsonify({"status": "success", "content": pos_id}), 200
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404

# Path to the wpa_supplicant config file
WPA_SUPPLICANT_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"
# Function to update wpa_supplicant.conf with new network info
#WPA_SUPPLICANT_CONF = "pys/wpa_supplicant.conf"
# Route to handle WiFi connection data
@app.route('/connect', methods=['POST'])
def connect_to_wifi():
    try:
        # Get the JSON payload (SSID and password)
        data = request.json
        ssid = data.get('ssid')
        password = data.get('password')

        if not ssid or not password:
            return jsonify({"status": "error", "message": "SSID and password required"}), 400

        # Update wpa_supplicant.conf with new network info
        update_wpa_supplicant(ssid, password)
        time.sleep(2)
        # Restart networking services
        os.system("sudo systemctl restart networking.service")
        time.sleep(1)
        # os.system("sudo systemctl restart dhcpcd.service")
        os.system("sudo systemctl restart wpa_supplicant.service")
        time.sleep(1)
        subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])
        time.sleep(1)
        # reboot the system
        os.system('sudo reboot')

        return jsonify({"status": "success", "message": "WiFi connection updated!, restarting"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def update_wpa_supplicant(ssid, password):
    # Create the network block for the wpa_supplicant configuration
    # network_config = f"""
    # network={{
    #     ssid="{ssid}"
    #     psk="{password}"
    # }}
    # """
    # Create a new network block
    if password:
        network_config = f"""
        network={{
        ssid="{ssid}"
        psk="{password}"
        key_mgmt=WPA-PSK
        }}
        """
    else:
        network_config = f"""
        network={{
        ssid="{ssid}"
        key_mgmt=NONE
        }}
        """

    # Append the new network to wpa_supplicant.conf
    with open(WPA_SUPPLICANT_CONF, "a") as f:
        f.write(network_config)
    print(f"Added network '{ssid}' to wpa_supplicant.conf")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
