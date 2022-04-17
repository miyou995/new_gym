# adduser taki 

usermod -aG sudo taki
su - taki

sudo apt-mark hold pyhton # to exclude python from beiing upgraded

# sudo apt update
# sudo apt upgrade

sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx

# sudo -u postgres psql

CREATE DATABASE starmania_db;
CREATE USER octopus WITH PASSWORD 'miyou0209';
ALTER ROLE octopus SET client_encoding TO 'utf8';
ALTER ROLE octopus SET default_transaction_isolation TO 'read committed';
ALTER ROLE octopus SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE starmania_db TO octopus;

# CONFIGURE DJANGO

virtualenv venv

clone the repo 

add local_settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "starmania_db",
        'USER': "octopus",
        'PASSWORD': "miyou0209",
        'HOST': "localhost",
        'PORT': "5432",
    }
}

python manage.py makemigrations

# ERROR cairo
no library called "libcairo-2" was found

# solution 

sudo apt-get install libpangocairo-1.0-0
.
python manage.py makemigrations
python manage.py migrate


gunicorn --bind 0.0.0.0:8000 config.wsgi

# Gunicorn configuration

sudo nano /etc/systemd/system/gunicorn.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target


sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=taki
Group=www-data
WorkingDirectory=/home/taki/star/starmania/starmania
ExecStart=/home/taki/star/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target


sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# possible command check errors sudo journalctl -u gunicorn.socket

sudo systemctl daemon-reload
sudo systemctl restart gunicorn

# NGINX CONFIGURATION

sudo nano /etc/nginx/sites-available/starmania

server {
    listen 80;
    server_name 167.71.3.168 starmania.dz www.starmania.dz;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/taki/star/starmania/starmania;
    }
    
    location /media/ {
        root /home/taki/star/starmania/starmania;    
    }
    location /assets/ {
        root /home/taki/star/starmania/starmania;    
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

sudo ln -s /etc/nginx/sites-available/starmania /etc/nginx/sites-enabled

sudo nginx -t

sudo systemctl restart nginx
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'

# Possible command sudo tail -F /var/log/nginx/error.log

#migrate sqlite to postgresql if it have to

1* 
python manage.py shell
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()

python manage.py loaddata fixture/whole.json

# command

sudo systemctl reload nginx
sudo systemctl restart gunicorn

add allowwed hosts

ALLOWED_HOSTS = ['167.71.3.168' ,'www.starmania.dz', 'starmania.dz']

# Configuration SSL

# sudo nano /etc/nginx/nginx.conf
add 
client_max_body_size 20M;

# Add SSL

sudo apt install certbot python3-certbot-nginx

sudo nano /etc/nginx/sites-available/starmania

check  -> sudo nginx -t

sudo systemctl reload nginx
sudo ufw status

sudo ufw allow 'Nginx Full'
sudo ufw delete allow 'Nginx HTTP'

sudo certbot --nginx -d starmania.dz -d www.starmania.dz

sudo systemctl status certbot.timer
sudo certbot renew --dry-run

# print errors 

sudo cat /var/log/syslog