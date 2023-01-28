# INSTALLATION FOR VENV
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

# EXPORT PYTHON PACKAGES
pip freeze > requirements.txt