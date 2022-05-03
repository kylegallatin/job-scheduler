# Job Scheduler

## Build and Deploy Locally
```bash
# build image
docker build -t job-scheduler job_scheduler

# clean workspace then deploy
kubectl --context docker-desktop delete -f job_scheduler/templates/job_scheduler.yaml
kubectl --context docker-desktop apply -f job_scheduler/templates/job_scheduler.yaml

# expose port from cluster in another shell (restart this process if you redeploy)
kubectl --context docker-desktop port-forward service/job-scheduler 8080:8080

# get logs of the application
kubectl --context docker-desktop logs deploy/job-scheduler

# test server
curl -v "http://localhost:8080"

# upload files
curl -X POST -F "file1=@train.py" -F "file2=@requirements.txt" "http://localhost:8080/upload"

# test API
curl -X POST -H 'Content-Type: application/json' "http://localhost:8080/create" -d '{"gcs_path":"gs://soapbx-alpha/training_jobs/5c325a0e-5e12-11ec-a273-0278df424219", "job_name":"test", "run_command":"python train.py"}'

# get phase of the job
curl "http://localhost:8080/status?job_name=test" | jq .phase

# get the logs of the logs
curl "http://localhost:8080/logs?job_name=test"

# delete the job to free up the job name
curl -X POST -H 'Content-Type: application/json' "http://localhost:8080/delete" -d '{"job_name":"test"}'

# get job status
curl "http://localhost:8080/job_status?job_name=test"

# get the output 
gsutil ls gs://soapbx-alpha/training_jobs/5c325a0e-5e12-11ec-a273-0278df424219/output
```

## Development 
Setup the pre-commit hooks for automated Python formatting.

```bash
pip install yapf
wget -O .git/hooks/pre-commit "https://raw.githubusercontent.com/google/yapf/main/plugins/pre-commit.sh"
chmod +x .git/hooks/pre-commit
```