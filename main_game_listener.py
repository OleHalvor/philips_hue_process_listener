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

def flash():
    flash_duration = 0.2
    previous_brightnesses = get_current_brightness()
    setBrightness(254)
    time.sleep(flash_duration)
    setBrightness(0)
    time.sleep(flash_duration)
    setBrightness(previous_brightnesses)

def get_current_temperature():
    for light in lightsToControl:
        return b.get_light(light)['state']['ct']


def get_current_brightness():
    for light in lightsToControl:
        return b.get_light(light)['state']['bri']


def setColorTemperature(ct):
    if ct < 0:
        ct = 0
    print("setting color",ct)
    for light in lightsToControl:
        b.set_light(light, 'ct', ct)


def setBrightness(bri):
    print("setting brgihtness",bri)
    for light in lightsToControl:
        b.set_light(light, 'bri', bri)


base_brightness = get_current_brightness()  # 1 - 254
last_set_brightness = get_current_brightness()
bri_last_iteration = get_current_brightness()

base_temperature = get_current_temperature()  # 155 - 453
last_set_temperature = get_current_temperature()
temp_last_iteration = get_current_temperature()

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
            print("App has closed: ", running_app)
            running_apps.remove(running_app)
            break
    for app in found_apps:
        if app not in running_apps:
            new_apps.append(app)
            running_apps.append(app)
            print("new app found: ", app)

    for app in new_apps:
        if app["flash"]:
            flash()
            break
    if len(found_apps) > 0:
        highest_priority_app = found_apps[0]
        if not current_app == highest_priority_app:
            # New highest priority app detected, change lights
            if "color_temperature" in highest_priority_app:
                last_set_temperature = highest_priority_app["color_temperature"]
                setColorTemperature(highest_priority_app["color_temperature"])
            else:
                last_set_temperature = base_temperature
                setColorTemperature(base_temperature)
            if "brightness" in highest_priority_app:
                last_set_brightness = highest_priority_app["brightness"]
                setBrightness(highest_priority_app["brightness"])
            else:
                print("setting base brightness",base_brightness)
                last_set_brightness = base_brightness
                setBrightness(base_brightness)
            current_app = highest_priority_app
            print("new priority app", highest_priority_app)
        else:
            if current_app == highest_priority_app:
                if "color_temperature" in highest_priority_app and not get_current_temperature() == highest_priority_app["color_temperature"]:
                    time.sleep(1)
                    print("external temperature detected, saving new base value",get_current_temperature())
                    base_temperature = get_current_temperature()
                    base_brightness = get_current_brightness()
                if "brightness" in highest_priority_app and not get_current_brightness() == highest_priority_app["brightness"]:
                    time.sleep(1)
                    # Not a new app, but missmatch of brightness
                    print("external brightness detected, saving new base value",get_current_brightness())
                    base_brightness = get_current_brightness()
    elif not current_app == "base":
        print("setting base")
        last_set_temperature = base_temperature
        setColorTemperature(base_temperature)
        last_set_brightness = base_brightness
        setBrightness(base_brightness)
        current_app = "base"

    if len(found_apps) == 0 and last_set_brightness == base_brightness and not get_current_brightness() == last_set_brightness:
        time.sleep(1)
        print("external brightness detected, saving new base value",get_current_brightness())
        base_brightness = get_current_brightness()
    if len(found_apps) == 0 and last_set_temperature == base_temperature and not get_current_temperature() == last_set_temperature:
        time.sleep(1)
        print("external temperature detected, saving new base value",get_current_temperature())
        base_temperature = get_current_temperature()

    time.sleep(1)
    bri_last_iteration = get_current_brightness()
    temp_last_iteration = get_current_temperature()
