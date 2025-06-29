#!/bin/bash
echo "========== ApplicationStart Hook =========="
echo "Starting FastAPI server..."

cd /home/ec2-user/app/api_service

# Set up virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
pip install --upgrade pip
pip install -r /home/ec2-user/app/requirements.txt

echo "Launching uvicorn server..."
nohup uvicorn main:app --host 0.0.0.0 --port 80 > /home/ec2-user/app/uvicorn.log 2>&1 &

echo "FastAPI server started successfully."
