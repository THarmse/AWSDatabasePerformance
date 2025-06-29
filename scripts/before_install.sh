#!/bin/bash
echo "========== BeforeInstall Hook =========="
echo "Cleaning up old app directory..."

rm -rf /home/ec2-user/app

echo "Old app directory removed."
