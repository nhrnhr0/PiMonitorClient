# env setup
sudo apt install python3.8-venv -y
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
sudo cp prod.env .env

# supervisor
sudo apt update
sudo apt install supervisor -y
sudo apt install unclutter -y
sudo mkdir /var/log/gunicorn
sudo apt install cec-utils
sudo cp ./pi_monitor.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart piMonitor
