from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# File path for read/write operations
file_path = 'pys\data.txt'

@app.route('/api/read', methods=['GET'])
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

@app.route('/api/reboot', methods=['POST'])
def reboot():
    if 1:
        print("rebooted")
        os.system('sudo reboot')
        return jsonify({"status": "success", "content": "rebooted"}), 200
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    if 1:
        print("shutdown")
        os.system('sudo shutdown -h now')
        
        return jsonify({"status": "success", "content": "shutdown"}), 200
    else:
        return jsonify({"status": "error", "message": "File not found"}), 404   
     
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
