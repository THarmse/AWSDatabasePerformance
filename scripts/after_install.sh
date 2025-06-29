#!/bin/bash
set -ex
echo "Running AfterInstall script"

cd /home/ec2-user/app
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cat >/etc/httpd/conf.d/app_proxy.conf <<'EOF'
<VirtualHost *:80>
    DocumentRoot /var/www/html
    ProxyPreserveHost On

    ProxyPass "/mysql/" "http://127.0.0.1:8000/mysql/"
    ProxyPassReverse "/mysql/" "http://127.0.0.1:8000/mysql/"

    ProxyPass "/docs" "http://127.0.0.1:8000/docs"
    ProxyPassReverse "/docs" "http://127.0.0.1:8000/docs"
</VirtualHost>
EOF

systemctl restart httpd
