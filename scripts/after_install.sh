#!/bin/bash
echo "========== AfterInstall Hook =========="
echo "Setting permissions on deployed files..."

# Set ownership (optional, adapt as needed)
chown -R ec2-user:ec2-user /home/ec2-user/app

# Make all scripts executable
chmod +x /home/ec2-user/app/scripts/*.sh

echo "Permissions set successfully."
