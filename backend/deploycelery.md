#   most people will only start one node:
CELERYD_NODES="worker1"
#   but you can also start multiple and configure settings
#   for each in CELERYD_OPTS
#CELERYD_NODES="worker1 worker2 worker3"
#   alternatively, you can specify the number of nodes to start:
#CELERYD_NODES=10

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/mnt/c/Users/amd/Desktop/Octogym/ubvenv/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="salle_activite"
# or fully qualified:
# CELERY_APP="proj.tasks:app"

# Where to chdir at start.
CELERYD_CHDIR="/mnt/c/Users/amd/Desktop/Octogym/backend"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"
# Configure node-specific settings by appending node name to arguments:
#CELERYD_OPTS="--time-limit=300 -c 8 -c:worker2 4 -c:worker3 2 -Ofair:worker1"

# Set logging level to DEBUG
#CELERYD_LOG_LEVEL="DEBUG"

# %n will be replaced with the first part of the node name.
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"

# Workers should run as an unprivileged user.
#   You need to create this user manually (or you can choose
#   a user/group combination that already exists (e.g., nobody).
CELERYD_USER="taki"
# CELERYD_GROUP="celery"
CELERYD_LOG_LEVEL="INFO"
# If enabled PID and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1





/etc/systemd/system/celery.service

[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=taki
Group=www-data

EnvironmentFile=/mnt/c/Users/amd/Desktop/Octogym/ubvenv/bin/celery
WorkingDirectory=/mnt/c/Users/amd/Desktop/Octogym/backend
ExecStart=/home/user/.virtualenvs/venv/bin/celery multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}
ExecStop=/home/user/.virtualenvs/venv/bin/celery ${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}
ExecReload=/home/user/.virtualenvs/venv/bin/celery ${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}

[Install]
WantedBy=multi-user.target