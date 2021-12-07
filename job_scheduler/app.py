import logging
from flask import Flask, Response, request, jsonify
import waitress
from google.cloud import storage

from job_scheduler import K8sJobScheduler

JOB_SCHEDULER = K8sJobScheduler()
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)
app = Flask(__name__)
# storage_client = storage.Client()
# bucket_name="gs://soapbx-alpha"
# bucket = storage_client.get_bucket(bucket_name)


@app.route("/")
def base():
    return Response("", 200)


@app.route("/create", methods=['GET', 'POST'])
def create():
    request_data = request.get_json()
    job_name = request_data.get("job_name")
    gcs_path = request_data.get("gcs_path")
    # TODO move default to config
    run_command = request_data.get("run_command", "python train.py")

    if None not in (job_name, gcs_path, run_command):

        return Response(
            str(JOB_SCHEDULER.create_job(job_name, gcs_path, run_command)), 200
        )
    else:
        return Response(f"Bad Request, parameter missing", 400)


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    request_data = request.get_json()
    job_name = request_data.get("job_name")
    if job_name:

        return Response(str(JOB_SCHEDULER.delete_job(job_name)), 200)
    else:
        return Response(f"Bad Request, missing parameter 'job_name'", 400)


@app.route("/job_status", methods=["GET"])
def job_status():
    job_name = request.args.get("job_name")
    if not job_name:
        return Response("Missing required 'job_name' parameter", 400)

    return jsonify(JOB_SCHEDULER.get_job_status(job_name))


@app.route("/status", methods=["GET"])
def status():
    job_name = request.args.get("job_name")
    if not job_name:
        return Response("Missing required 'job_name' parameter", 400)
    return jsonify(JOB_SCHEDULER.get_pod_status(job_name))


# @app.route("/upload", methods=["POST"])
# def upload():

# @app.route('/logs')
# def logs():
#     return render_template(
#         "stream.html",
#         user=request.args["user"],
#         title=request.args["title"],
#         fileList=request.args["fileList"]
#     )

# @app.route('/logs')
# def logs():
#     title = request.args["title"]
#     call(["./tail_logs.sh", title, "&"])
#     def generate(title):
#         with open(f'{title}.log') as f:
#             while True:
#                 yield f.read()
#                 sleep(1)
#     return app.response_class(generate(title), mimetype='text/plain')

if __name__ == "__main__":
    waitress.serve(app, host="0.0.0.0")
