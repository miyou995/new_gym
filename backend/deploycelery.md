# new config  ( tested )
sudo mkdir -p /var/log/celery
sudo touch /var/log/celery/gym_access.log
sudo touch /var/log/celery/gym_error.log
sudo touch /var/log/celery/gym_access_log.log

sudo chown -R taki:www-data /var/log/celery


## sudo nano /etc/systemd/system/celery.service


[Unit]
Description=Celery Service for octogym
After=network.target

[Service]
User=taki
Group=taki
WorkingDirectory=/home/taki/gym/new_gym/backend

ExecStart=/home/taki/gym/venv/bin/celery -A config worker \
          --concurrency=20 \
          --loglevel=INFO \
          --logfile /var/log/celery/gym_access_log.log \
          --access-logfile /var/log/celery/gym_access.log \
          --error-logfile /var/log/celery/gym_error.log \
Restart=always


[Install]
WantedBy=multi-user.target


# real time ubuntu access log 
sudo tail -f /var/log/celery/gym_access.log


## sudo nano /etc/systemd/system/celerybeat.service


[Unit]
Description=Celery Service for octogym
After=network.target

[Service]
User=taki
Group=taki
WorkingDirectory=/home/taki/gym/new_gym/backend

ExecStart=/home/taki/gym/venv/bin/celery -A config beat \
          --concurrency=20 \
          --loglevel=INFO \
          --logfile /var/log/celery/gym_access_log.log \
          --access-logfile /var/log/celery/gym_access.log \
          --error-logfile /var/log/celery/gym_error.log \
Restart=always


[Install]
WantedBy=multi-user.target