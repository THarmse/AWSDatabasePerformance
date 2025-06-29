#!/bin/bash
echo "========== ApplicationStart Hook =========="
echo "Stopping placeholder healthcheck server if running..."
pkill -f "http.server"

echo "Starting FastAPI server..."

cd /home/ec2-user/app/api_service

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r /home/ec2-user/app/requirements.txt

nohup uvicorn main:app --host 0.0.0.0 --port 80 > /home/ec2-user/app/uvicorn.log 2>&1 &
