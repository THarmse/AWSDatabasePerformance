#!/bin/bash
set -ex
echo "Running BeforeInstall script"

# Clean old app dir
rm -rf /home/ec2-user/app
mkdir -p /home/ec2-user/app
