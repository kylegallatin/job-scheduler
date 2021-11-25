# Job Scheduler

## Setup
Setup the pre-commit hooks for automated Python formatting.

```bash
pip install yapf
wget -O .git/hooks/pre-commit "https://raw.githubusercontent.com/google/yapf/main/plugins/pre-commit.sh"
chmod +x .git/hooks/pre-commit
```

## Deploy
```bash
kubectl --context $CONTEXT apply -f templates/job_scheduler.yaml
```

## Development 

To test the creation and status of a job, run:
```bash
kubectl --context $CONTEXT port-forward service/job-scheduler 8080:8080
curl -X POST -H 'Content-Type: application/json' localhost:8080/create -d '{"gcs_path":"gs://soapbx-alpha/kyle-test61a13a18-d81d-4004-9fe6-71e2a3b9fd10/training_test", "job_name":"test", "run_command":"python train.py"}'
curl http://localhost:8080/job_status?job_name=test
curl http://localhost:8080/status?job_name=test
```

To run a separate debugging container in the cluster:
```bash
kdd run -i --tty python-dev --image=gcr.io/serene-radius-314018/python/python-base:0.0.2 --restart=Never -- sh
kdd delete po python-dev
``` 