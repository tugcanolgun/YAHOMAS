# YAHOMAS

YAHOMAS stands for 'Yet Another HOtel MAnagement System'

This is an in-development project for SWE599 class in Bogazici University.

The aim is to build a guest management system for hotels.

Live preview can be seen at https://yahomas.tugcan.net

## Dependencies

This project required python 3.6 and up. Since type annotations are used in the project, for performance sake, I strongly recommend 3.7+

`python3.7 -m venv .env`

`source .env/bin/activate`

`pip install --upgrade pip`   *(optional)*

`pip install -r requirements`

## Running

For test purposes, start the app with using `./manage.py runserver`

Since this project uses `djangosecure`, it will ask you some details on first run. You can adjust database settings here. If you want to go with sqlite option, just type sqlite for the first question and type db.sqlite3 for the database.

## Deployment

Installing dependencies from `requirements.txt` already provides gunicorn but incase you want to install, `pip install gunicorn`

### systemd

`sudo vim /etc/systemd/system/yahomas.service`

and paste the following. **Do not forget to change the username**

```
[Unit]
Description=YAHOMAS
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/YAHOMAS
ExecStart=/home/user/YAHOMAS/.env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/user/YAHOMAS/gms/gms.sock gms.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Reverse proxy nginx

Configure the settings for your environment.

```
server {
    ...
    server_name yahomas.tugcan.net;

    location / {
        #try_files $uri $uri/ =404;
        include proxy_params;
        proxy_pass http://unix:/home/user/YAHOMAS/gms/gms.sock;
    }

    location /static/ {
        alias /home/user/static/YAHOMAS/;
    }

    location /media/ {
        #alias /home/user/static/YAHOMAS/media/;
        alias /home/user/YAHOMAS/media/;
    }
    ...
}
```

