#!/bin/bash
echo "========== AfterInstall Hook =========="
echo "Setting permissions on deployed files..."

chown -R ec2-user:ec2-user /home/ec2-user/app
chmod +x /home/ec2-user/app/scripts/*.sh

echo "Permissions set successfully."
