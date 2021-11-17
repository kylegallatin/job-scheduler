# Job Scheduler

## Development
Setup the pre-commit hooks for automated Python formatting.

```bash
pip install yapf
wget -O ../.git/hooks/pre-commit https://raw.githubusercontent.com/google/yapf/main/plugins/pre-commit.sh
chmod +x ../.git/hooks/pre-commit
```

## Test and Debugging
curl -X POST -H 'Content-Type: application/json' localhost:8080/create -d '{"gcs_path:gs://soapbx-alpha/kyle-test61a13a18-d81d-4004-9fe6-71e2a3b9fd10/training_test", "job_name":"test1", "run_command":"python train.py"}'

kdd run -i --tty python-dev --image=gcr.io/serene-radius-314018/python/python-base:0.0.2 --restart=Never -- sh 