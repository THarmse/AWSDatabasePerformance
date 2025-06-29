#!/bin/bash
set -ex
echo "Running start.sh"

cd /home/ec2-user/app

# Activate virtual environment
source venv/bin/activate

# Kill any previous uvicorn process on port 8000
if lsof -i:8000; then
    echo "Killing existing uvicorn"
    kill $(lsof -t -i:8000) || true
fi

# Start uvicorn server in background
nohup python3 -m uvicorn api_service.main:app --host 127.0.0.1 --port 8000 > /home/ec2-user/app/uvicorn.log 2>&1 &
