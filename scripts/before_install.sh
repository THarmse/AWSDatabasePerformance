#!/bin/bash
set -ex
echo "Running BeforeInstall script"

# Clean old app dir
rm -rf /home/ec2-user/app
mkdir -p /home/ec2-user/app

# Core build tools for Python packages
sudo yum install -y gcc gcc-c++ make python3-devel

# Install unixODBC (required for pyodbc)
sudo yum install -y unixODBC unixODBC-devel

# Add Microsoft repo GPG key and repo for ODBC Driver 17
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo curl -o /etc/yum.repos.d/msprod.repo https://packages.microsoft.com/config/rhel/8/prod.repo

# Clean and refresh metadata
sudo yum clean all
sudo yum makecache

# Install Microsoft ODBC Driver 17 for SQL Server
sudo ACCEPT_EULA=Y yum install -y msodbcsql17

# Wait for files to appear (Oracle)
echo "Waiting for Oracle Instant Client RPMs to appear..."
for i in {1..60}; do
  if ls /home/ec2-user/app/oracle_rpms/*.rpm >/dev/null 2>&1; then
    echo "RPMs detected!"
    break
  fi
  echo "Still waiting..."
  sleep 1
done

# Set wide open permissions
echo "Setting permissions..."
sudo chmod 777 /home/ec2-user/app/oracle_rpms
sudo chmod 777 /home/ec2-user/app/oracle_rpms/*.rpm

# Log contents
echo "RPM directory listing:"
ls -lh /home/ec2-user/app/oracle_rpms

# Install Oracle Instant Client RPMs
echo "Installing Oracle Instant Client RPMs..."
sudo yum install -y /home/ec2-user/app/oracle_rpms/oracle-instantclient-basic-23.8.0.25.04-1.el8.x86_64.rpm
sudo yum install -y /home/ec2-user/app/oracle_rpms/oracle-instantclient-devel-23.8.0.25.04-1.el8.x86_64.rpm



# Clean and refresh metadata
sudo yum clean all
sudo yum makecache

echo "BeforeInstall script completed successfully."
