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

# test server
curl -v "http://localhost:8080"

# test API
curl -X POST -H 'Content-Type: application/json' "http://localhost:8080/create" -d '{"gcs_path":"gs://soapbx-alpha/kyle-test61a13a18-d81d-4004-9fe6-71e2a3b9fd10/training_test", "job_name":"test", "run_command":"python train.py"}'
curl "http://localhost:8080/job_status?job_name=test"

# get phase of the job
curl "http://localhost:8080/status?job_name=test" | jq .phase
```

## Development 
Setup the pre-commit hooks for automated Python formatting.

```bash
pip install yapf
wget -O .git/hooks/pre-commit "https://raw.githubusercontent.com/google/yapf/main/plugins/pre-commit.sh"
chmod +x .git/hooks/pre-commit
```