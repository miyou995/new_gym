source with multiple deploy https://www.digitalocean.com/community/questions/how-to-deploy-multiple-django-apps-as-subdomains-using-nginx-and-gunicorn


# adduser taki

ssh root@your_server_ip

adduser taki

usermod -aG sudo taki
su - taki

## Setting Up a Basic Firewall
sudo ufw app list
sudo ufw allow OpenSSH
sudo ufw enable # pres y after 
sudo ufw status 



sudo apt-mark hold pyhton # to exclude python from beiing upgraded

# sudo apt update
# sudo apt upgrade

sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx

# sudo -u postgres psql

CREATE DATABASE octogym_db;
CREATE USER octopus WITH PASSWORD 'miyou0209';
ALTER ROLE octopus SET client_encoding TO 'utf8';
ALTER ROLE octopus SET default_transaction_isolation TO 'read committed';
ALTER ROLE octopus SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE octogym_db TO octopus;
\q

# CONFIGURE DJANGO
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
virtualenv venv

source venv/bin/activate

## clone the repo 

## add local_settings.py
cd /new_gym/config

sudo nano local_settings.py


# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = 'QCqcqscrtgjczvgrezg0hzd6t%82b3ol#^)6(94^o+nto(5h#kg#f7z!yh8'
DEBUG = False

ALLOWED_HOSTS = ['*'] # a modifier apres l'integration du nom de domaine

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "octogym_db",
        'USER': "octopus",
        'PASSWORD': "miyou0209",
        'HOST': "localhost",
        'PORT': "5432",
    }
}

pip install -r requirements.txt

python manage.py makemigrations

# ERROR cairo
no library called "libcairo-2" was found

# solution 

sudo apt-get install libpangocairo-1.0-0
.
python manage.py makemigrations
python manage.py migrate


sudo ufw allow 8000

gunicorn --bind 0.0.0.0:8000 config.wsgi

# Gunicorn configuration

sudo nano /etc/systemd/system/new_gym.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/new_gym.sock

[Install]
WantedBy=sockets.target


sudo nano /etc/systemd/system/new_gym.service

[Unit]
Description=gunicorn daemon
Requires=new_gym.socket
After=network.target

[Service]
User=taki
Group=www-data
WorkingDirectory=/home/taki/octogym/new_gym/
ExecStart=/home/taki/octogym/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/new_gym.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target




sudo systemctl enable new_gym.socket
sudo systemctl enable new_gym.service 

sudo systemctl start new_gym.socket
sudo systemctl start new_gym.service 
# possible command check errors 
sudo journalctl -u new_gym.socket

sudo systemctl daemon-reload
sudo systemctl restart new_gym

# NGINX CONFIGURATION

sudo nano /etc/nginx/sites-available/new_gym

server {
    listen 80;
    server_name 192.168.1.250;
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /media/ {
        root /home/taki/octogym/new_gym/;    
    }
    location /static/ {
        root /home/taki/octogym/new_gym/build/;    
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

sudo ln -s /etc/nginx/sites-available/new_gym /etc/nginx/sites-enabled/new_gym

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
  
python manage.py loaddata fixture/whole.json ,

# command

sudo systemctl reload nginx
sudo systemctl restart marchesa

add allowwed hosts

# Custom domaine
@  A Record  178.62.41.8
www  CNAME  maisonlamarchesa.com

ALLOWED_HOSTS = ['178.62.41.8' ,'www.maisonlamarchesa.com', 'maisonlamarchesa.com']

sudo nano /etc/nginx/sites-available/taksit

server {
    listen: 80;
    server_name 178.62.41.8 www.maisonlamarchesa.com maisonlamarchesa.com;
}

sudo systemctl restart nginx
sudo systemctl restart marchesa

# Configuration SSL

sudo nano /etc/nginx/nginx.conf
add 
client_max_body_size 20M;

# Add SSL

sudo apt install certbot python3-certbot-nginx

sudo nano /etc/nginx/sites-available/marchesa
sudo nano /etc/nginx/sites-available/kahraba

check  -> sudo nginx -t

sudo systemctl reload nginx
sudo ufw status

sudo ufw allow 'Nginx Full'
sudo ufw delete allow 'Nginx HTTP'

sudo certbot --nginx -d maisonlamarchesa.com -d www.maisonlamarchesa.com

sudo systemctl status certbot.timer
sudo certbot renew --dry-run

# print errors 

sudo cat /var/log/syslog
sudo tail -30 /var/log/nginx/error.log


grep -r 178.62.41.8 /etc/nginx/sites-enabled/*

sudo journalctl -u marchesa.socket

curl --unix-socket /run/marchesa.sock localhost

sudo systemctl status marchesa
sudo journalctl -u marchesa

sudo systemctl restart marchesa

sudo ln -s /etc/nginx/sites-available/marchesa
   









   