#!/bin/bash
set -ex
echo "Running AfterInstall script"

cd /home/ec2-user/app

# Create and activate venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Add Apache proxy configuration
cat <<EOF > /etc/httpd/conf.d/app.conf
<VirtualHost *:80>
    DocumentRoot /var/www/html

    ProxyPreserveHost On
    ProxyRequests Off

    <Proxy *>
        Require all granted
    </Proxy>

    ProxyPass /mysql/ http://127.0.0.1:8000/mysql/
    ProxyPassReverse /mysql/ http://127.0.0.1:8000/mysql/

    ProxyPass /AuroraMySQL/ http://127.0.0.1:8000/AuroraMySQL/
    ProxyPassReverse /AuroraMySQL/ http://127.0.0.1:8000/AuroraMySQL/

    ProxyPass /postgresql/ http://127.0.0.1:8000/postgresql/
    ProxyPassReverse /postgresql/ http://127.0.0.1:8000/postgresql/

    ProxyPass /AuroraPostgreSQL/ http://127.0.0.1:8000/AuroraPostgreSQL/
    ProxyPassReverse /AuroraPostgreSQL/ http://127.0.0.1:8000/AuroraPostgreSQL/

    ProxyPass /mariadb/ http://127.0.0.1:8000/mariadb/
    ProxyPassReverse /mariadb/ http://127.0.0.1:8000/mariadb/

    ProxyPass /mssql/ http://127.0.0.1:8000/mssql/
    ProxyPassReverse /mssql/ http://127.0.0.1:8000/mssql/

    ProxyPass /oracle/ http://127.0.0.1:8000/oracle/
    ProxyPassReverse /oracle/ http://127.0.0.1:8000/oracle/

    ProxyPass /dynamodb/ http://127.0.0.1:8000/dynamodb/
    ProxyPassReverse /dynamodb/ http://127.0.0.1:8000/dynamodb/

    ProxyPass /ibmdb2/ http://127.0.0.1:8000/ibmdb2/
    ProxyPassReverse /ibmdb2/ http://127.0.0.1:8000/ibmdb2/

    ProxyPass /docs http://127.0.0.1:8000/docs
    ProxyPassReverse /docs http://127.0.0.1:8000/docs
</VirtualHost>
EOF

# Restart Apache
systemctl restart httpd
# Install Oracle Instant Client RPMs
echo "Installing Oracle Instant Client RPMs..."
sudo yum install -y /home/ec2-user/app/oracle_rpms/oracle-instantclient-basic-23.8.0.25.04-1.el8.x86_64.rpm
sudo yum install -y /home/ec2-user/app/oracle_rpms/oracle-instantclient-devel-23.8.0.25.04-1.el8.x86_64.rpm