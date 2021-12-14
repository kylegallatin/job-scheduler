#!/bin/bash
docker build -t job-scheduler job_scheduler
kubectl --context docker-desktop delete -f job_scheduler/templates/job_scheduler.yaml
kubectl --context docker-desktop apply -f job_scheduler/templates/job_scheduler.yaml