# EnvironmentFile
# See
# http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html#available-options

## sudo nano /etc/conf.d/celery

CELERY_APP="config"
CELERYD_NODES="worker"
CELERYD_OPTS="--time-limit=300 --concurrency=20"
CELERY_BIN="/home/taki/gym/venv/bin/celery"
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n.log"
CELERYD_LOG_LEVEL="INFO"


# service file 
## sudo nano /etc/systemd/system/celery.service


[Unit]
Description=Celery Service for octogym
After=network.target

[Service]
Type=forking
User=taki
EnvironmentFile=-/etc/conf.d/celery
WorkingDirectory=/home/taki/gym/new_gym/backend/


ExecStart=/home/taki/gym/venv/bin/celery -A $CELERY_APP ${CELERYD_NODES} --logfile=INFO --concurrency=20
ExecStop=${CELERY_BIN} stopwait ${CELERYD_NODES} 
ExecReload=${CELERY_BIN} restart ${CELERYD_NODES} -A $CELERY_APP --logfile=${CELERYD_LOG_FILE} --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS

[Install]
WantedBy=multi-user.target



ExecStart=/home/taki/gym/venv/bin/celery -A config worker --concurrency=20 --loglevel=INFO




# working one 

                                 
[Unit]
Description=Celery Service for octogym
After=network.target

[Service]
User=taki
Group=taki
WorkingDirectory=/home/taki/gym/new_gym/backend
ExecStart=/home/taki/gym/venv/bin/celery -A config worker --concurrency=20 --loglevel=INFO
Restart=always


[Install]
WantedBy=multi-user.target






##create logs dir and files
sudo mkdir -p /var/log/celery
sudo touch /var/log/celery/gym_access.log
sudo touch /var/log/celery/gym_error.log
sudo chown -R taki:www-data /var/log/celery



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
          --access-logfile /var/log/celery/gym_access.log \
          --error-logfile /var/log/celery/gym_error.log \
Restart=always


[Install]
WantedBy=multi-user.target

# real time ubuntu access log 
sudo tail -f /var/log/gunicorn/gym_access.log

