# Script to check battery level of DS4 controllers, on Linux
# reference: https://github.com/thankjura/ds4battery/blob/master/extension.js

import os

DEVICE_PREFIX_DUALSHOCK = "sony_controller_battery_"
DEVICE_PREFIX_DUALSENSE = "ps-controller-battery-"
POWER_DIR_PATH = '/sys/class/power_supply/'


# lists of DS4 devices, example when everything is updated:
# [{
#   'name': 'sony_controller_battery_a4:53:85:9d:7e:fb',
#   'power': 60,
#   'charging': True,
#   'color': '#304688' # <- TODO
# }]
def getDevices():
    devices = []

    for dir in [x[1] for x in os.walk(POWER_DIR_PATH)][0]:
        if (dir.startswith(DEVICE_PREFIX_DUALSHOCK) or dir.startswith(DEVICE_PREFIX_DUALSHOCK)):
            device = {
                'name': dir
            }
            devices.append(device)
    
    return devices


def updatePowerLevels(devices):
    for device in devices:
        with open(POWER_DIR_PATH + device['name'] + '/capacity', 'r') as f:
            device['power'] = f.readline().strip()
    return devices


def updateChargingStatuses(devices):
    for device in devices:
        with open(POWER_DIR_PATH + device['name'] + '/status', 'r') as f:
            device['charging'] = f.readline().strip()
    return devices


def printDevices(devices):
    print(f'{"Device":>41}{"Power":>16}{"Status":>15}')
    for device in devices:
        print(f'{device["name"]:>41}{device["power"]:>15}%{device["charging"]:>15}')


devices = getDevices()
updatePowerLevels(devices)
updateChargingStatuses(devices)
printDevices(devices)
