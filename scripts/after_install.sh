#!/bin/bash
set -ex
echo "Running AfterInstall script"

cd /home/ec2-user/app

echo "Listing contents for debugging:"
ls -la

if [ ! -f requirements.txt ]; then
  echo "ERROR: requirements.txt is missing or not a file!"
  exit 1
fi

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
