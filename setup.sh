# env setup
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
echo 'WS_SERVER_URL=wss://pi-monitor.boost-pop.com/ws/socket-server/' >> .env


# supervisor
sudo apt update -y && sudo apt install supervisor -y
sudo apt install unclutter -y
sudo mkdir /var/log/gunicorn
sudo cp ./pi_monitor.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart piMonitor
