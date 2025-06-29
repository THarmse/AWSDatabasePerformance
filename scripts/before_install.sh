#!/bin/bash
set -e

echo "Stopping existing uvicorn if running"
pkill -f uvicorn || true
