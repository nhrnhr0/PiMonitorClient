import websocket
import _thread
import time
import rel
import json
import pyautogui
import base64
from io import BytesIO
from device_id import get_device_id
from dotenv import load_dotenv

import os
monitor_thread = None
def on_message(ws, message):
    print(message)
    message_type= json.loads(message)['type']
    if message_type == 'command':
        command = json.loads(message)['data']['command']
        if command == 'hdmi_cec_off':
            print("Turning off HDMI CEC")
            os.system("echo 'standby 0' | cec-client -s -d 1")
        elif command == 'hdmi_cec_on':
            print("Turning on HDMI CEC")
            os.system("echo 'on 0' | cec-client -s -d 1")
            
    pass

def on_error(ws, error):
    print(error)
    exit(1)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    monitor_thread.join()
    exit(1)


def on_open(ws):
    print("Opened connection")
    # start to monitor, send a status every 5 seconds
    global monitor_thread
    if not monitor_thread is None:
        monitor_thread.join()
    monitor_thread = _thread.start_new_thread(monitor, (ws,))


def monitor(ws):
    while True:
        
        myScreenshot = pyautogui.screenshot()
        # encodeed = myScreenshot.tobytes()
        buffered = BytesIO()
        myScreenshot.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        img_str = img_str.decode('utf-8')
        device_id = get_device_id()
        ws.send(json.dumps({"type": "status","device":device_id, "data": {"status": "connected", "time": time.time(),
                                                       'img': img_str}}))
        time.sleep(30)



if __name__ == "__main__":
    load_dotenv()
    get_device_id()
    websocket.enableTrace(False)
    server_url = os.getenv('WS_SERVER_URL')
    ws = websocket.WebSocketApp(server_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    ws.run_forever(dispatcher=rel, reconnect=5)
    # print("Starting rel dispatcher")
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    try:
        rel.dispatch()
    except:
        time.sleep(3)
        pass
    
    # print("Exiting rel dispatcher")
