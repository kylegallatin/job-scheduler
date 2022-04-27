#!/bin/bash
docker build -t job-scheduler job_scheduler
kubectl --context colima delete -f job_scheduler/templates/job_scheduler_local.yaml
kubectl --context colima apply -f job_scheduler/templates/job_scheduler_local.yaml