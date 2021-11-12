import os
from flask import Flask, request, jsonify
import waitress

from job_scheduler import K8sJobScheduler

JOB_MANAGER = K8sJobScheduler()

app = Flask(__name__)

@app.route("/")
def base():
    return "Base path"

@app.route("/create")
def create():
    pass

@app.route("/status")
def status():
    job_name = request.args.get("job_name")
    if not job_name:
        return jsonify("Missing required 'job_name' parameter")

    return jsonify(JOB_MANAGER.get_status(job_name))

if __name__ == "__main__":
    waitress.serve(app, host="0.0.0.0")