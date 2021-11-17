import os
from flask import Flask, Response, request, jsonify
import waitress

from job_scheduler import K8sJobScheduler

JOB_SCHEDULER = K8sJobScheduler()
app = Flask(__name__)

@app.route("/", methods = ["GET"])
def base():
    return jsonify("Base path")

@app.route("/create")
def create():
    request_data = request.get_json()
    job_name = request_data.get("job_name")
    gcs_path = request_data.get("gcs_path")
    run_command = request_data.get("run_command")

    if None not in (job_name, gcs_path, run_command):
        JOB_SCHEDULER.create_job(job_name, gcs_path, run_command)
        return Response(f"Submitting job: {job_name}", 200)
    else:
        return Response(f"Bad Request, parameter missing", 400)

@app.route("/status", methods = ["GET"])
def status():
    job_name = request.args.get("job_name")
    if not job_name:
        return Response("Missing required 'job_name' parameter", 400)

    return jsonify(JOB_SCHEDULER.get_job_status(job_name))

if __name__ == "__main__":
    waitress.serve(app, host="0.0.0.0")