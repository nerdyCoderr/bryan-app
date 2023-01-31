# INSTALLATION FOR VENV (unused)

https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
-Windows
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate

-Ubuntu/Rasp
sudo apt-get install -y python3-venv
python -m venv env
source env/bin/activate

pip install -r requirements.txt

# INSTALLATION FOR REACT

sudo apt install nginx
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt install nodejs

cd client
npm install

# INSTALLATION FOR OPENCV

https://pimylifeup.com/raspberry-pi-opencv/
pip install opencv-python #for windows

# EXPORT PYTHON PACKAGES

pip freeze > requirements.txt

# SETUP NGINGX

sudo apt-get install nginx
sudo systemctl start nginx
sudo systemctl status nginx
sudo systemctl enable nginx
sudo nano /etc/nginx/sites-available/default

---

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

## }

sudo nginx -t
sudo systemctl restart nginx
Add an entry in your local hosts file to map the subdomain to your local IP address:
127.0.0.1 flask.com

# STARTING FLASK AND REACT AFTER BOOT

Create the following file /etc/systemd/system/my_project.service:

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
Then you can run:

sudo systemctl start my_project  
sudo systemctl status my_project
If bad, tweak and try:

sudo systemctl restart my_project
sudo systemctl status my_project
If Good:

sudo systemctl enable my_project
