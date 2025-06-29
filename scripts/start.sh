#!/bin/bash
echo "========== ApplicationStart Hook =========="
echo "Stopping any existing uvicorn server..."
pkill -f "uvicorn" || true

echo "Starting FastAPI server on localhost:8000..."

cd /home/ec2-user/app/api_service

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r /home/ec2-user/app/requirements.txt

nohup uvicorn main:app --host 127.0.0.1 --port 8000 > /home/ec2-user/app/uvicorn.log 2>&1 &
