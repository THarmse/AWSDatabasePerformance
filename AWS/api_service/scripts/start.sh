#!/bin/bash
echo "ApplicationStart hook running"
cd /home/ec2-user/app/aws/api_service
nohup uvicorn main:app --host 0.0.0.0 --port 80 &
