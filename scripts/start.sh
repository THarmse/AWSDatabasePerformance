#!/bin/bash
echo "Starting FastAPI server..."

cd /home/ec2-user/app

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

nohup uvicorn main:app --host 0.0.0.0 --port 80 > uvicorn.log 2>&1 &
