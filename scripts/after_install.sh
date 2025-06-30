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

    ProxyPass /docs http://127.0.0.1:8000/docs
    ProxyPassReverse /docs http://127.0.0.1:8000/docs
</VirtualHost>
EOF

# Restart Apache
systemctl restart httpd
