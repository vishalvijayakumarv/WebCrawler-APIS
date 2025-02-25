from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the path to JSON files
def get_json_data(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "Failed to load data from {}".format(filename)}

@app.route('/api/list-containers', methods=['GET'])
def list_containers():
    data = get_json_data('containers.json')
    return jsonify(data)

@app.route('/api/list-services', methods=['GET'])
def list_services():
    data = get_json_data('services.json')
    return jsonify(data)

@app.route('/api/notification', methods=['GET'])
def list_notifications():
    data = get_json_data('notifications.json')
    return jsonify(data)

@app.route('/api/send-scraper', methods=['POST'])
def send_job():
    data = request.get_json()
    url = data.get('url')
    job_name = data.get('job_name')
    
    if not url or not job_name:
        return jsonify({"error": "Missing url or job_name"}), 400
    
    print(f"Job Name: {job_name}")
    print(f"Website: {url}")
    
    return jsonify({"message": "Job received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
