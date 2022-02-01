#!/bin/bash
docker build -t gcr.io/serene-radius-314018/job-scheduler/job-scheduler:0.0.1 job_scheduler
kubectl --context docker-desktop delete -f job_scheduler/templates/job_scheduler.yaml
kubectl --context docker-desktop apply -f job_scheduler/templates/job_scheduler.yaml