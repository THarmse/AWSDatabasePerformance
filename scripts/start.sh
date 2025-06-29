#!/bin/bash
set -e

# Kill old process if running
pkill uvicorn || true

# Start FastAPI app with Uvicorn behind Apache
nohup uvicorn api_service.main:app --host 127.0.0.1 --port 8000 > /var/www/app/uvicorn.log 2>&1 &
