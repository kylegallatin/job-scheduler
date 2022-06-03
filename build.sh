#!/bin/bash
docker build -t gcr.io/serene-radius-314018/job-scheduler/job-scheduler:0.0.3 job_scheduler
docker push gcr.io/serene-radius-314018/job-scheduler/job-scheduler:0.0.3
kubectl --context gke_serene-radius-314018_us-central1-c_soapbox-text-cluster delete -f job_scheduler/templates/job_scheduler_gke.yaml
kubectl --context gke_serene-radius-314018_us-central1-c_soapbox-text-cluster apply -f job_scheduler/templates/job_scheduler_gke.yaml
