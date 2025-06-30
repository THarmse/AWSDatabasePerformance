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

# Install Microsoft ODBC Driver 17 for SQL Server
sudo su
curl https://packages.microsoft.com/config/rhel/8/prod.repo > /etc/yum.repos.d/msprod.repo
exit
sudo yum install -y msodbcsql17

# Install Oracle Instant Client
sudo yum install -y oracle-instantclient-release-el8
sudo yum install -y oracle-instantclient-basic oracle-instantclient-devel