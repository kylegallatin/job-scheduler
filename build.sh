#!/bin/bash
docker build -t job-scheduler job_scheduler
kubectl --context gke_serene-radius-314018_us-central1-c_soapbox-text-cluster delete -f job_scheduler/templates/job_scheduler_gke.yaml
kubectl --context gke_serene-radius-314018_us-central1-c_soapbox-text-cluster apply -f job_scheduler/templates/job_scheduler_gke.yaml
