#sudo nano /etc/systemd/system/celery.service

[Unit]
Description=Celery Service for octogym atlas
After=network.target

[Service]
Type=forking
User=taki
Group=www-data
WorkingDirectory=/home/taki/gym/new_gym/backend
ExecStart=/home/taki/gym/venv/bin/celery -A config worker --concurrency=20 --loglevel=INFO
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target





## start service 
sudo systemctl daemon-reload
sudo systemctl start celerygym.service


[Unit]
Description=Celery Service for octogym atlas

[Service]
#Type=forking
User=taki
WorkingDirectory=/home/taki/gym/new_gym/backend
ExecStart=/home/taki/gym/venv/bin/celery -A config worker -l INFO --concurrency 2
Restart=always

[Install]
WantedBy=multi-user.target
