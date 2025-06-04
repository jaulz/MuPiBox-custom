#!/usr/bin/env python3

import sys

import requests
import logging
import subprocess
from evdev import InputDevice, list_devices, categorize, ecodes, KeyEvent
import argparse

logger = logging.getLogger(__name__)

# Functions
def togglePlay():
    response = requests.get(url="http://localhost:5005/local")
    response.raise_for_status()
    
    data = response.json()
    
    if data.pause == True:
        requests.get(url="http://localhost:5005/play")
    else:
        requests.get(url="http://localhost:5005/pause")

def playTestSound2():
    subprocess.call(["aplay", "/usr/share/sounds/alsa/Front_Left.wav"])

def playTestSound3():
    subprocess.call(["aplay", "/usr/share/sounds/alsa/Front_Right.wav"])

def playTestSound4():
    subprocess.call(["aplay", "/usr/share/sounds/alsa/Rear_Left.wav"])

def playTestSound5():
    subprocess.call(["aplay", "/usr/share/sounds/alsa/Rear_Right.wav"])

# Mapping from keycode to buttons interface
keycodeToButtonInterface = {
    "BTN_JOYSTICK-BTN_TRIGGER": "K1",
    "BTN_THUMB": "K2",
    "BTN_THUMB2": "K3",
    "BTN_TOP": "K4",
    "BTN_TOP2": "K5",
}

# Mapping from button interface to function
buttonInterfaceToFunction = {
    "K1": togglePlay,
    "K2": playTestSound2,
    "K3": playTestSound3,
    "K4": playTestSound4,
    "K5": playTestSound5,
}

# Parse arguments
parser = argparse.ArgumentParser("handleButtons.py")
parser.add_argument("--deviceId", help="Device ID", type=int, nargs='?')
args = parser.parse_args()
print(args.deviceId)

# Get device 
devices = [InputDevice(fn) for fn in list_devices()]

if args.deviceId is not None:
    currentDevice = devices[args.deviceId]
else:
    try:
        i = 0
        print("")
        print("Choose the Buttons USB Encoder device from the list")

        for device in devices:
            print(i, device.path, device.name, device.phys)
            i += 1

        deviceId = int(input('Device Number: '))
        currentDevice = devices[deviceId]
    except KeyboardInterrupt:
        sys.exit("Aborted to register Buttons USB Encoder.")

# Handle events
try:
    for event in currentDevice.read_loop():
        if event.type == ecodes.EV_KEY:
            keyEvent = categorize(event)

            if keyEvent.keystate == KeyEvent.key_down:
                keycode = keyEvent.keycode

                if type(keycode) is list:
                    keycode = '-'.join(sorted(keycode))

                try:
                    print(keycode)
                    buttonInterface = keycodeToButtonInterface[keycode]
                    print(buttonInterface)
                    function = buttonInterfaceToFunction[buttonInterface]

                    function()
                    #function_name = button_map[button_string]
                    #function_args = button_map[button_string + "_args"]
                    #try:
                    #    getattr(function_calls, function_name)(function_args)
                    #except Exception:
                    #    logger.warning(
                    #        "Function " + function_name
                    #        + " not found in function_calls.py (mapped from button: " + button_string + ")")
                except KeyError:
                    logger.warning("Button " + keycode + " not mapped to any function.")
except Exception as exception: 
    logger.error('An error with Buttons USB Encoder occurred: %s', repr(exception))