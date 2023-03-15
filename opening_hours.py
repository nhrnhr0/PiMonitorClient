import json
import datetime
import os

from os_commands import get_current_hdmi_status, turn_off_hdmi_cec, turn_on_hdmi_cec
OPENING_HOURS_FILE_PATH = './opening_hours.txt'

current_opening_hours = None
def set_opening_hours(data):
    global current_opening_hours
    if current_opening_hours != data:
        print("Setting new opening hours")
        with open(OPENING_HOURS_FILE_PATH, 'w') as f:
            f.write(json.dumps(data))
        current_opening_hours = data
        check_and_update_tv_status(get_current_hdmi_status())
def check_and_update_tv_status(current_hdmi_status):
    if current_hdmi_status == 'on':
        if is_open():
            print("TV is on and should be on")
            return
        else:
            print("TV is on but should be off")
            # turn off the tv
            turn_off_hdmi_cec()
    else:
        if is_open():
            print("TV is off but should be on")
            # turn on the tv
            turn_on_hdmi_cec()
        else:
            print("TV is off and should be off")
            return

def is_open():
    if current_opening_hours is None:
        return True 
    # {"opening_hours": [{"weekday": 1, "from_hour": "07:00:00", "to_hour": "19:00:00"}, {"weekday": 2, "from_hour": "07:00:00", "to_hour": "19:00:00"}, {"weekday": 3, "from_hour": "07:00:00", "to_hour": "19:00:00"}, {"weekday": 4, "from_hour": "07:00:00", "to_hour": "20:00:00"}, {"weekday": 5, "from_hour": "07:00:00", "to_hour": "20:01:00"}], "manual_turn_off": false}
    if current_opening_hours['manual_turn_off']:
        return False
    current_weekday = (datetime.datetime.today().weekday() + 2)%7
    current_time = datetime.datetime.now().time()
    print('current_weekday' + str(current_weekday))
    print('current_time' + str(current_time)
    for opening_hours in current_opening_hours['opening_hours']:
        if opening_hours['weekday'] == current_weekday:
            from_hour = datetime.datetime.strptime(opening_hours['from_hour'], '%H:%M:%S').time()
            to_hour = datetime.datetime.strptime(opening_hours['to_hour'], '%H:%M:%S').time()
            if from_hour <= current_time and current_time <= to_hour:
                return True
    return False
# try to read the opening hours from the opening_hours.txt file
def init_opening_hours():
    global current_opening_hours
    if current_opening_hours is not None:
        print("Opening hours already initialized")
        return
    try:
        with open(OPENING_HOURS_FILE_PATH, 'r') as f:
            data = json.loads(f.read())
            set_opening_hours(data)
    except:
        print("Failed to read opening hours")
        pass
init_opening_hours()