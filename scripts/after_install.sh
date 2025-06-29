#!/bin/bash
set -e

echo "Running after_install.sh"

# Install Python packages (virtualenv optional but here global)
pip3 install --upgrade pip
pip3 install -r /home/ec2-user/app/requirements.txt

# Ensure uvicorn will be installed
pip3 install uvicorn

# Apache reverse proxy config
cat >/etc/httpd/conf.d/app.conf <<'EOF'
<VirtualHost *:80>
    DocumentRoot /var/www/html

    ProxyPreserveHost On

    <Directory "/var/www/html">
        AllowOverride None
        Require all granted
    </Directory>

    ProxyPass "/mysql/" "http://127.0.0.1:8000/mysql/"
    ProxyPassReverse "/mysql/" "http://127.0.0.1:8000/mysql/"

    ProxyPass "/docs" "http://127.0.0.1:8000/docs"
    ProxyPassReverse "/docs" "http://127.0.0.1:8000/docs"

</VirtualHost>
EOF

echo "Restarting Apache to pick up new config"
/usr/sbin/apachectl restart
