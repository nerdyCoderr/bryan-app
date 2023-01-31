## REPLICATE THE DATA FOLDER

Go to the root directory and run the `folder_tree_maker.py`

```
python folder_tree_maker.py
```

## INSTALLATION FOR VENV (unused)

1. Create a virtual environment with pip:

- Windows:

```
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```

- Ubuntu/Rasp:

```
sudo apt-get install -y python3-venv
python -m venv env
source env/bin/activate
```

2. Install the required packages:

```
pip install -r requirements.txt
```

## INSTALLATION FOR REACT

1. Install nginx:

```
sudo apt install nginx
```

2. Install Node.js:

```
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash - sudo apt install nodejs
```

3. Navigate to the client directory and run

```
npm install
```

## INSTALLATION FOR OPENCV

1. Follow the instructions from this link: https://pimylifeup.com/raspberry-pi-opencv/
2. Windows:

```
pip install opencv-python
```

## SETUP NGINX

1. Install nginx:

```
sudo apt-get install nginx
```

2. Start nginx:

```
sudo systemctl start nginx
```

3. Check nginx status:

```
sudo systemctl status nginx
```

4. Enable nginx:

```
sudo systemctl enable nginx
```

5. Edit nginx configuration file:

```
sudo nano /etc/nginx/sites-available/default
```

```
server {
    listen 80;
    server_name flask.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

6. Test nginx configuration:

```
sudo nginx -t
```

7. Restart nginx:

```
sudo systemctl restart nginx
```

8. Add the following entry to your local hosts file:

```
127.0.0.1 flask.com
```

## STARTING FLASK AND REACT AFTER BOOT

1. Create a service file:

```
sudo nano /etc/systemd/system/my_project.service
```

```
[Unit]
Description=My Project
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/project/
ExecStart=/usr/bin/python /home/pi/project/script.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Start the service:

```
sudo systemctl start my_project
```

3. Check service status:

```
sudo systemctl status my_project
```

4. Restart service if needed:

```
sudo systemctl restart my_project
```

5. Enable the service:

```
sudo systemctl enable my_project
```
