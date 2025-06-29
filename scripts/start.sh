#!/bin/bash
echo "ApplicationStart Hook: Starting FastAPI with Uvicorn"
cd /home/ec2-user/app
nohup uvicorn api_service.main:app --host 0.0.0.0 --port 80 &
