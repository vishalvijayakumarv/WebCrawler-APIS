from flask import Flask, jsonify, request, Response  # Import Response for SSE
from flask_cors import CORS  # Import CORS
import json
import os
import time
import threading

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

@app.route('/api/log-streams', methods=['GET'])
def list_log_streams():
    log_streams = {
        "log_streams": [
            "job-1-log-stream",
            "job-2-log-stream",
            "job-3-log-stream",
            "job-4-log-stream"
            # "job-5-log-stream",
            # "job-6-log-stream",
            # "job-7-log-stream",
            # "job-8-log-stream",
            # "job-9-log-stream",
            # "job-10-log-stream",
            # "job-12-log-stream",
            # "job-13-log-stream",
            # "job-14-log-stream",
            # "job-15-log-stream",
            # "job-16-log-stream",
            # "job-17-log-stream",
            # "job-18-log-stream",
            # "job-19-log-stream",
            # "job-20-log-stream"
        ]
    }
    return jsonify(log_streams)

def generate_fake_logs(log_stream_name):
    while True:
        time.sleep(1)  # Simulate log generation delay
        yield f"data: Log from {log_stream_name} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

@app.route('/api/live-log', methods=['GET', 'POST'])
def live_log():
    if request.method == 'POST':
        data = request.get_json()
        log_stream_name = data.get('log_stream_name')
        
        if not log_stream_name:
            return jsonify({"error": "Missing log_stream_name"}), 400
        
        return jsonify({"message": "Log stream started"}), 200
    
    elif request.method == 'GET':
        log_stream_name = request.args.get('log_stream_name')
        
        if not log_stream_name:
            return jsonify({"error": "Missing log_stream_name"}), 400
        
        return Response(generate_fake_logs(log_stream_name), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
