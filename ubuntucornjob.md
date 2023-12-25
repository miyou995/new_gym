# sudo nano /etc/systemd/system/open-gym.service

[Unit]
Description=Open the gym

[Service]
User=taki
Group=taki
WorkingDirectory=/home/taki/gym/new_gym/backend/
ExecStart=/home/taki/gym/venv/bin/python /home/taki/gym/new_gym/backend/manage.py open_gym


[Install]
WantedBy=multi-user.target


# sudo nano /etc/systemd/system/open-gym.timer

[Unit]
Description=Run the open gym every day at 4 am

[Timer]
OnCalendar=*-*-* 04:00:00
Unit=open-gym.service
Persistent=true

[Install]
WantedBy=timers.target


