#!/bin/bash
set -eux

gsutil cp -r $1/* /workspace
pip install -r requirements.txt --no-cache-dir
exec $2
gsutil cp -r /workspace $1/output