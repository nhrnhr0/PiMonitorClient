import os
import base64
import subprocess

BASE_PATH = os.getenv('BASE_PATH')
def refresh_page():
    # send F5 key to chromium
    os.system('xdotool key F5')
    pass
def deploy():
    # run `deploy.sh`
    os.system('bash ' + BASE_PATH + '/deploy.sh')
    pass
def system_update():
    os.system('sudo apt-get update && sudo apt-get upgrade -y')
    pass
def get_current_hdmi_status():
    get_hdmi_status = os.popen('echo "pow 0" | cec-client -s -d 1').read()
    if 'power status: on' in get_hdmi_status:
        hdmi_status = 'on'
    elif 'power status: off' in get_hdmi_status:
        hdmi_status = 'off'
    elif 'power status: standby' in get_hdmi_status:
        hdmi_status = 'standby'
    else:
        hdmi_status = 'unknown - ' + str(get_hdmi_status)
    return hdmi_status

def turn_on_hdmi_cec():
    os.system("echo 'on 0' | cec-client -s -d 1")


def turn_off_hdmi_cec():
    os.system("echo 'standby 0' | cec-client -s -d 1")


def set_hdmi_active_source():
    os.system('echo "as" | cec-client RPI -s -d 1')
def is_kiosk_running():
    # check if chromium is running
    get_chromium_status = os.popen('ps -A | grep chromium').read()
    if 'chromium' in get_chromium_status:
        return True
    else:
        return False

def deploy_code():
    # run `deploy.sh`
    
    os.system('bash ' + BASE_PATH + '/deploy.sh')
    pass
def refresh_page():
    # send F5 key to chromium
    os.system('xdotool key F5')
    pass
def run_script(script):
    # run the script
    os.system(script)
    pass
def update_software():
    # run sudo apt-get update && sudo apt-get upgrade -y
    os.system('sudo apt-get update && sudo apt-get upgrade -y')
    pass

def take_screenshot():
    env = {'DISPLAY': ':0', 'XAUTHORITY': '/home/pi/.Xauthority'}
    img_str = ''
    try:
        screenshot = subprocess.check_output(['sudo', '-E', 'scrot', '-q', '5', '-e', 'cat $f'], env=env)
        img_str = base64.b64encode(screenshot).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print('Error:', e)
        img_str = ''
    except Exception as e:
        print('Unexpected error:', e)
        img_str = ''
    return img_str
