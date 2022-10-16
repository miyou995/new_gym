[Unit]
Description=Celery Service for celeryproject atlas
After=network.target

[Service]
Type=forking
User=celery
Group=celery
Environment="ENV_PATH=.envs/.prod.env"
EnvironmentFile=/etc/conf.d/celery-project
WorkingDirectory=/home/taki/new_gym/backend
ExecStart=/home/taki/venv/bin/celery 'start celery -A ${CELERY_APP} worker --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
  
  
ExecStop=/home/taki/venv/bin/celery 'stopwait ${CELERYD_NODES} --pidfile=${CELERYD_PID_FILE}'
  
ExecReload=/home/taki/venv/bin/celery 'restart ${CELERYD_NODES} -A ${CELERY_APP} worker --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
  

[Install]
WantedBy=multi-user.target

# /etc/conf.d/celery-project



# App instance to use
# comment out this line if you don't use an app
CELERY_APP="config"

# Name of nodes to start
# here we have a single node
CELERYD_NODES="celeryproject"
# or we could have three nodes:
# CELERYD_NODES="celeryproject1 celeryproject2 celeryproject3"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"

# Absolute or relative path to the 'celery' command:
# I'm using virtualenvwrapper, and celery is installed in the 'celery_project' virtual environment
CELERY_BIN="/home/taki/venv/bin/celery"

# How to call manage.py
# CELERYD_MULTI="multi"

# - %n will be replaced with the first part of the nodename.
# - %I will be replaced with the current child process index
#   and is important when using the prefork pool to avoid race conditions.
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="INFO"

# The below lines should be uncommented if using the celerybeat-project.service
# unit file, but are unnecessary otherwise


# CELERY SERVICE

[Unit]
Description=Celery Service for celeryproject atlas
After=network.target

[Service]
Type=forking
User=taki
Group=www-data
Environment="ENV_PATH=.envs/.prod.env"
EnvironmentFile=/etc/conf.d/celery-project
WorkingDirectory=/home/taki/new_gym/backend
ExecStart=/home/taki/venv/bin/celery multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/home/taki/venv/bin/celery multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/home/taki/venv/bin/celery multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

[Install]
WantedBy=multi-user.target



## start service 
sudo systemctl daemon-reload
sudo systemctl start celerygym.service
