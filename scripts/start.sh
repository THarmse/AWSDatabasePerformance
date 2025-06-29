#!/bin/bash
set -ex
echo "Running start.sh"

cd /home/ec2-user/app

# Activate virtual environment
source venv/bin/activate

# Kill any existing uvicorn on port 8000
if lsof -i:8000; then
    echo "Stopping existing uvicorn process"
    kill $(lsof -t -i:8000) || true
fi

# Start uvicorn in background
nohup uvicorn api_service.main:app --host 127.0.0.1 --port 8000 > uvicorn.log 2>&1 &
