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

# Add Oracle Instant Client repo
sudo curl -o /etc/yum.repos.d/oracle-instantclient.repo https://yum.oracle.com/public-yum-ol8.repo

# Clean and refresh metadata
sudo yum clean all
sudo yum makecache

# Install Oracle Instant Client Basic and Devel packages
sudo yum install -y oracle-instantclient-basic oracle-instantclient-devel

echo "BeforeInstall script completed successfully."
