#!/bin/bash
set -eux

gsutil cp gs://soapbx-alpha/data/recipenlg/full_dataset.csv /data
gsutil cp -r $1/* /workspace
pip install -r requirements.txt --no-cache-dir
$2
echo "Run command finished, copying files back to $1/output"
gsutil cp -r /workspace $1/output