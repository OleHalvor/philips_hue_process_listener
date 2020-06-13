from phue import Bridge
import time
import json
import os
import psutil

lightsToControl = ['Olli soverom lys', 'stue lys', 'inngang lys']

b = Bridge("192.168.1.133")
b.connect()
b.get_api()
print(json.dumps(b.get_api()['lights'], indent=4, sort_keys=True))


# If color is not same as last set: Save this color as the base color
history_of_set_temperatures = []

from programs import programs

print(programs)


current_app = None
running_apps = []

def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(["name", "exe", "cmdline"]):
        if name == p.info['name'] or \
                p.info['exe'] and os.path.basename(p.info['exe']) == name or \
                p.info['cmdline'] and p.info['cmdline'][0] == name:
            ls.append(p)
    return ls

def get_current_temperature():
    print("returning 100 hardiced current temp")
    return 100

max_temperature = 999
base_temperature = 250
last_set_temperature = base_temperature
last_command = None

def setColorTemperature(ct):
    for light in lightsToControl:
        last_set_temperature = ct
        b.set_light(light, 'ct', ct)

current_app = "ingen"
while True:
    found_apps = []
    new_apps = []

    for program in programs:
        if find_procs_by_name(program["process_name"]):
            found_apps.append(program)
    found_apps = sorted(found_apps, key=lambda k: k['priority'])

    for running_app in running_apps:
        if running_app not in found_apps:
            print("App has closed: ",running_app)
            running_apps.remove(running_app)
            break
    for app in found_apps:
        if app not in running_apps:
            new_apps.append(app)
            running_apps.append(app)
            print("new app found: ",app)
            break

    if len(found_apps) > 0:
        highest_priority_app = found_apps[0]
        if not current_app == highest_priority_app:
            setColorTemperature(highest_priority_app["color_temperature"])
            current_app = highest_priority_app
            print("setting",highest_priority_app)
        elif not get_current_temperature() == last_set_temperature:
            print("external temperature detected, setting new base")
            base_temperature = get_current_temperature()
    elif not current_app == "base":
        print("setting base")
        setColorTemperature(base_temperature)
        current_app="base"
    time.sleep(1)