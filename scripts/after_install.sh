#!/bin/bash
echo "AfterInstall Hook: Moving new app into place"
mkdir -p /home/ec2-user/app
cp -r * /home/ec2-user/app/
