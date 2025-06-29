#!/bin/bash
set -ex
echo "Starting FastAPI app"

cd /home/ec2-user/app
source venv/bin/activate
nohup uvicorn api_service.main:app --host 127.0.0.1 --port 8000 --workers 2 > app.log 2>&1 &
