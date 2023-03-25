import os
import base64

BASE_PATH = os.getenv('BASE_PATH')

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
    image_location = '/home/pi/Desktop/PiMonitorClient/img.png'
    if os.path.exists(image_location):
        os.remove(image_location)
    os.system('export DISPLAY=:0 && export XAUTHORITY=/home/pi/.Xauthority && sudo scrot -q 5 ' + image_location)
    img_str = ''
    try:
        with open(image_location, 'rb') as image_file:
            img_str = base64.b64encode(image_file.read())
            img_str = img_str.decode('utf-8')
    except:
        img_str = ''
    return img_str