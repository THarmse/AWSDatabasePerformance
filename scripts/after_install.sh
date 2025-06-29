#!/bin/bash
set -ex
echo "Running AfterInstall script"

cd /home/ec2-user/app
python3 -m venv venv
source venv/bin/activate

echo "Upgrading pip"
pip install --upgrade pip

echo "Installing requirements.txt"
pip install -r requirements.txt

echo "AfterInstall script complete"
