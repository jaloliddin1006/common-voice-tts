# common-voice-tts


git clone https://github.com/jaloliddin1006/common-voice-tts.git

#
virtualenv venv
#
source venv/bin/activate
#
pip install -r requirements.txt
#
pip install gunicorn

#
deactivate
#
sudo su
#
nano /etc/systemd/system/tts.socket
#
```
[Unit]
Description=tts socket

[Socket]
ListenStream=/run/tts.sock

[Install]
WantedBy=sockets.target
```


#
nano /etc/systemd/system/tts.service

#
```
[Unit]
Description=tts schedule daemon
Requires=tts.socket
After=network.target

[Service]
User=root
WorkingDirectory=/home/defonic/common-voice-tts/
ExecStart=/home/defonic/common-voice-tts/venv/bin/gunicorn \
          --access-logfile - \
####          --workers 3 \
          --bind unix:/run/tts.sock \
          core.wsgi:application

[Install]
WantedBy=multi-user.target
```
#

systemctl daemon-reload
#
systemctl start tts
#
systemctl enable tts
#
systemctl status tts
#

# nginx and domein settings
#
apt-get update
#
apt-get install nginx
#
nano /etc/nginx/sites-available/tts
#
```
server {
    server_name onlinelibrary.uz tts.mamatmusayev.uz;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/defonic/common-voice-tts/staticfiles;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/tts.sock;
    }
}
```

#
ln -s /etc/nginx/sites-available/tts /etc/nginx/sites-enabled
#
nginx -t
#
systemctl restart nginx
#
systemctl status nginx
#

# SSL certbot

