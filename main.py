import requests
from dotenv import load_dotenv
import os

from opening_hours import OPENING_HOURS_FILE_PATH, check_and_update_tv_status, set_opening_hours
from os_commands import get_current_hdmi_status, is_kiosk_running, set_hdmi_active_source, take_screenshot, turn_on_hdmi_cec
load_dotenv()
os.environ.setdefault('DISPLAY', ':0.0')
import websocket
import _thread
import time
import rel
import json
# import pyautogui
import base64
from io import BytesIO
from device_id import get_device_id



monitor_thread = None
def on_message(ws, message):
    print(message)
    json_message = json.loads(message)
    message_type= json_message['type']
    if message_type == 'command':
        command = json_message['command']
        if command == 'hdmi_cec_off':
            print("Turning off HDMI CEC")
            os.system("echo 'standby 0' | cec-client -s -d 1")
        elif command == 'hdmi_cec_on':
            print("Turning on HDMI CEC")
            os.system("echo 'on 0' | cec-client -s -d 1")
        elif command == 'reboot':
            print("Rebooting")
            os.system("sudo reboot")
        elif command == 'relaunch_kiosk_browser':
            print("Relaunching kiosk browser")
            # run `run_kiosk.sh`
            relaunch_kiosk_browser()
        elif command =='set_tv_url':
            print("Setting TV URL")
            url = json_message['url']
            # create url.txt file and write the url to it
            with open('./url.txt', 'w') as f:
                f.write(url)
            # relaunch the kiosk browser
            relaunch_kiosk_browser()
        else:
            print("Unknown command")
    elif message_type == 'opening_hours':
        print("Opening hours message")
        opening_hours = json_message['opening_hours']
        manual_turn_off = json_message['manual_turn_off']
        data = {'opening_hours': opening_hours, 'manual_turn_off': manual_turn_off}
        set_opening_hours(data)
        # write the opening hours to the opening_hours.txt file
        
            
        
        
    else:
        print("Unknown message type")
    pass
def relaunch_kiosk_browser():
    os.system("export DISPLAY=:0.0 && export XAUTHORITY=/home/pi/.Xauthority && /bin/bash ./run_kiosk.sh &")

def on_error(ws, error):
    print(error)
    time.sleep(5)
    exit(1)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###", close_status_code, close_msg)
    # global monitor_thread
    # monitor_thread.join()
    time.sleep(5)
    exit(1)


def on_open(ws):
    print("Opened connection")
    # start to monitor, send a status every 5 seconds
    global monitor_thread
    if not monitor_thread is None:
        monitor_thread.join()
    monitor_thread = _thread.start_new_thread(monitor, (ws,))

django_request_session = None


def send_fetch_to_django(img_str, device_id, t,hdmi_status):
    # send the image to the django server via http
    global django_request_session
    url = os.getenv('DJANGO_SERVER_URL') + 'pi_screenshot/' + device_id + '/'
    data = {'image': img_str, 'time': t, 'hdmi_status': hdmi_status}
    if django_request_session is None:
        django_request_session = requests.Session()
    try:
        r = django_request_session.post(url, data=data)
        print(r.status_code, r.reason)
    except Exception as e:
        print(e)
        print("Failed to send fetch to django")
        django_request_session = None
        pass


def monitor(ws):
    print("Starting monitor")
    while True:
        print("Sending status")
        
        t = time.time()
        device_id = get_device_id()
        
        hdmi_status = get_current_hdmi_status()
        img_str = take_screenshot()
        send_fetch_to_django(img_str,device_id, t,hdmi_status)
        ws.send(json.dumps({"type": "status","device":device_id, "data": {"status": "connected", "time": t, 'hdmi_status': hdmi_status,
                                                       }}))
        print("Sent status")
        check_and_update_tv_status(hdmi_status)
        time.sleep(30)


if __name__ == "__main__":
    
    # os.environ[''] = 
    print('starting')
    # turn the hdmi cec on
    # turn_on_hdmi_cec()
    
    # set the hdmi (rasberry PI) cec to be active source
    set_hdmi_active_source()
    # relaunch_kiosk_browser()
    device_id = get_device_id()
    websocket.enableTrace(False)
    server_url = os.getenv('WS_SERVER_URL')
    server_url = server_url  + device_id
    print('connecting to ', server_url)
    ws = websocket.WebSocketApp(server_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    # relaunch_kiosk_browser()
    if not is_kiosk_running():
        relaunch_kiosk_browser()
    ws.run_forever(dispatcher=rel, reconnect=5)
    # print("Starting rel dispatcher")
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    try:
        rel.dispatch()
    except:
        time.sleep(3)
        pass
    time.sleep(5)
    # print("Exiting rel dispatcher")
