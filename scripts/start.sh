#!/bin/bash
set -e

echo "Starting uvicorn server"
/usr/local/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --root-path /mysql/ --log-level info &
