#!/bin/bash
set -eux

gsutil cp -r $1/* /workspace
pip install -r requirements.txt --no-cache-dir
$2
echo "Run command finished, copying files back to $1/output"
gsutil cp -r /workspace $1/output