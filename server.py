from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import json
import os
import time

app = Flask(__name__, static_folder='pwa', static_url_path='')
CORS(app)

# Disable caching for static files
@app.after_request
def add_header(response):
    if 'text/html' in response.content_type or 'text/css' in response.content_type or 'javascript' in response.content_type:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

DATA_FILE = 'schedule_data_sandbox.json'
DATA_FILE_CREWS = 'schedule_data_crews.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "workers": [],
        "slots": [
            {"time": "06:00", "desc": ""},
            {"time": "08:00", "desc": ""},
            {"time": "10:00", "desc": ""},
            {"time": "14:00", "desc": ""},
            {"time": "18:00", "desc": ""}
        ],
        "assignments": {},
        "darkMode": False
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_crews_data():
    if os.path.exists(DATA_FILE_CREWS):
        with open(DATA_FILE_CREWS, 'r') as f:
            return json.load(f)
    ts = int(time.time() * 1000)
    return {
        "workers": [],
        "slots": [
            {"id": "slot_" + str(ts) + "_1", "time": "06:00", "desc": ""},
            {"id": "slot_" + str(ts + 1) + "_2", "time": "08:00", "desc": ""},
            {"id": "slot_" + str(ts + 2) + "_3", "time": "10:00", "desc": ""},
            {"id": "slot_" + str(ts + 3) + "_4", "time": "14:00", "desc": ""},
            {"id": "slot_" + str(ts + 4) + "_5", "time": "18:00", "desc": ""}
        ],
        "assignments": {},
        "slotDates": {}
    }

def save_crews_data(data):
    with open(DATA_FILE_CREWS, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.json
    save_data(data)
    return jsonify({"status": "saved"})

@app.route('/api/data/crews', methods=['GET'])
def get_crews_data():
    return jsonify(load_crews_data())

@app.route('/api/data/crews', methods=['POST'])
def post_crews_data():
    data = request.json
    save_crews_data(data)
    return jsonify({"status": "saved"})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
