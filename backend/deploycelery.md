# create new user celery 
sudo useradd celery -d /home/celery -b /bin/bash

# create home dir foir user celery and logs folders

sudo mkhomedir_helper celery


sudo mkdir /var/log/celery
sudo chown -R celery:celery /var/log/celery
sudo chmod -R 755 /var/log/celery

sudo mkdir /var/run/celery
sudo chown -R celery:celery /var/run/celery
sudo chmod -R 755 /var/run/celery

# Next, we create a file /etc/conf.d/celery-project 
## if it dont want to create error !! conf.d folder does not exist 
   mkdir conf.d

sudo nano /etc/conf.d/celery-project

# See
# http://docs.celeryproject.org/en/latest/userguide/daemonizing.html#usage-systemd
# and https://www.willandskill.se/en/celery-4-with-django-on-ubuntu-18-04/

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="config"

# Name of nodes to start
# here we have a single node
CELERYD_NODES="celerygym"
# or we could have three nodes:
# CELERYD_NODES="celeryproject1 celeryproject2 celeryproject3"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"

# Absolute or relative path to the 'celery' command:
# I'm using virtualenvwrapper, and celery is installed in the 'celery_project' virtual environment
## CELERY_BIN="/home/username/Env/celery_project/bin/celery"

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
# if you use celery beat uncomment this lines 

# CELERYBEAT_PID_FILE="/var/run/celery/celerygym_beat.pid"
# CELERYBEAT_LOG_FILE="/var/log/celery/celerygym_beat.log"









# create the service for celery project in our case celerygym
sudo nano /etc/systemd/system/celerygym.service
sudo nano /etc/systemd/system/celery.service


[Unit]
Description=Celery Service for octogym atlas

After=network.target

[Service]
Type=forking
User=celery
Group=celery
Environment="ENV_PATH=.envs/.prod.env"
EnvironmentFile=/etc/conf.d/celerygym
WorkingDirectory=/home/taki/new_gym/backend
ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
Restart=always

[Install]
WantedBy=multi-user.target


## if you use celery beat ( create celery beat service ) pas encore tester 



sudo nano /etc/systemd/system/celerybeatgym.service 

[Unit]
Description=Celery Beat Service for octogym atlas 
After=network.target

[Service]
Type=simple
User=celery
Group=celery
Environment="ENV_PATH=.envs/.prod.env"
EnvironmentFile=/etc/conf.d/celerygym
WorkingDirectory=/home/taki/new_gym/backend
ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat  \
    --pidfile=${CELERYBEAT_PID_FILE} \
    --logfile=${CELERYBEAT_LOG_FILE} \
    --loglevel=${CELERYD_LOG_LEVEL} \
    --schedule=/home/celery/celerybeat-schedule'
Restart=always

[Install]
WantedBy=multi-user.target

# start service
sudo systemctl start celerygym.service
## sudo systemctl start celerybeatgym.service

# check status
sudo systemctl status celerygym.service

# enable service celerygym
sudo systemctl enable celerygym.service

# ############ configure redis #####################
# ############ configure redis #####################
# ############ configure redis #####################
# ############ configure redis #####################


# install redis 
sudo apt-get install redis-server

pip install redis
 
# Autostart Redis on server restart
$ sudo systemctl enable redis-server.service



/etc/systemd/system/celery.service

[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=taki
Group=www-data

EnvironmentFile=/etc/conf.d/celerygym
WorkingDirectory=/home/taki/new_gym/backend
ExecStart=/home/taki/venv/bin/celery multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}
ExecStop=/home/taki/venv/bin/celery ${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}
ExecReload=/home/taki/venv/bin/celery ${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}

[Install]
WantedBy=multi-user.target



<!-- TRY THIS  -->
sudo nano /etc/systemd/system/celerygym.service



[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=/etc/default/celeryd
WorkingDirectory=/home/taki/new_gym/backend
ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}"'
ExecReload=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi restart $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
Restart=always

[Install]
WantedBy=multi-user.target



ExecStart='${CELERY_BIN} ${CELERy_NODES} \
  -A ${CELERY_APP} worker --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop='${CELERY_BIN} stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload='${CELERY_BIN} restart ${CELERYD_NODES} \
  -A ${CELERY_APP} worker --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'


  ExecStart='${CELERY_BIN} ${CELERy_NODES} \
  -A ${CELERY_APP} worker --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop='${CELERY_BIN} stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload='${CELERY_BIN} restart ${CELERYD_NODES} \
  -A ${CELERY_APP} worker --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'




[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/home/taki/new_gym/backend
ExecStart='${CELERY_BIN} ${CELERy_NODES} \
  -A ${CELERY_APP} worker --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop='${CELERY_BIN} stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload='${CELERY_BIN} restart ${CELERYD_NODES} \
  -A ${CELERY_APP} worker --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'


[Install]
WantedBy=multi-user.target
