#!/bin/bash
set -ex
echo "Running ApplicationStart script"

# Kill any old uvicorn
pkill -f uvicorn || true

cd /home/ec2-user/app/api_service
source ../venv/bin/activate

# Start uvicorn in background
nohup uvicorn main:app --host 127.0.0.1 --port 8000 > /home/ec2-user/app/uvicorn.log 2>&1 &
