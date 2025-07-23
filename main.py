from flask import Flask, jsonify, request
import datetime
import json
import os
from pdf_utils import generate_pdf

app = Flask(__name__)
LOG_FILE = "renew_log.json"

expiry_state = {
    "domain": "demo.smartcert.io",
    "start_time": datetime.datetime.now().isoformat()
}

@app.route("/check", methods=["GET"])
def check_cert():
    now = datetime.datetime.now()
    start_time = datetime.datetime.fromisoformat(expiry_state["start_time"])
    delta = (now - start_time).seconds
    seconds_left = max(0, 60 - delta)
    expires_on = now + datetime.timedelta(seconds=seconds_left)
    return jsonify({
        "domain": expiry_state["domain"],
        "days_left": 0,
        "expires_on": expires_on.strftime("%Y-%m-%d %H:%M:%S"),
        "seconds_left": seconds_left
    })

@app.route("/renew", methods=["POST"])
def renew_cert():
    expiry_state["start_time"] = datetime.datetime.now().isoformat()
    log_entry = {
        "domain": expiry_state["domain"],
        "status": "Renewed",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    logs.append(log_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    generate_pdf(logs)
    return jsonify({"message": "Renewal successful", "log": log_entry})

@app.route("/log", methods=["GET"])
def get_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route("/export/pdf", methods=["GET"])
def export_pdf():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
        path = generate_pdf(logs)
        return jsonify({"message": "PDF generated", "path": path})
    return jsonify({"message": "No log found."})