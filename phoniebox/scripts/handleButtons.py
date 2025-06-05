#!/usr/bin/env python3

import sys

import json
import requests
import logging
import subprocess
from evdev import InputDevice, list_devices, categorize, ecodes, KeyEvent
import argparse
import zmq
from typing import (List, Dict, Optional)

logger = logging.getLogger(__name__)

url = f"tcp://localhost:5555"

context = zmq.Context.instance()


default_ignore_response = False
default_ignore_errors = False

def enque_raw(request, ignore_response: Optional[bool] = None, ignore_errors: Optional[bool] = None):
    if ignore_response is None:
        ignore_response = default_ignore_response
    if ignore_errors is None:
        ignore_errors = default_ignore_errors

    if ignore_response is False and 'id' not in request:
        request['id'] = True

    queue = context.socket(zmq.REQ)
    queue.setsockopt(zmq.RCVTIMEO, 200)
    queue.setsockopt(zmq.LINGER, 200)
    queue.connect(url)
    queue.send_string(json.dumps(request))

    try:
        server_response = json.loads(queue.recv())
    except Exception as exception:
        if ignore_errors is False:
            print(exception)
        print(f"While waiting for server response: {exception}")
        return None

    if 'error' in server_response:
        if ignore_errors is False:
            print(server_response['error'].get('message', 'No error message provided'))

        print("Ignored response error: "
                        f"{server_response['error'].get('message', 'No error message provided')}")
        return None

    if ignore_response is True:
        return None

    return server_response['result']

def enque(package: str, plugin: str, method: Optional[str] = None,
            args: Optional[List] = None, kwargs: Optional[Dict] = None,
            ignore_response: Optional[bool] = None,
            ignore_errors: Optional[bool] = None):
    request = {'package': package, 'plugin': plugin}
    if method is not None:
        request['method'] = method
    if args is not None:
        request['args'] = args
    if kwargs is not None:
        request['kwargs'] = kwargs
    return enque_raw(request, ignore_response, ignore_errors)

# Functions
def playTestSound():
    subprocess.call(["aplay", "/usr/share/sounds/alsa/Rear_Left.wav"])

def togglePlay():
    response = enque('player', 'ctrl', 'toggle', args={})

def turnVolumeUp():
    response = enque('volume', 'ctrl', 'change_volume', args={ 'step': '10' })

def turnVolumeDown():
    response = enque('volume', 'ctrl', 'change_volume', args={ 'step': '-10' })

def playNextTrack():
    response = enque('player', 'ctrl', 'next', args={})

def playPreviousTrack():
    response = enque('player', 'ctrl', 'prev', args={})

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
    "K1": togglePlay, # togglePlay,
    "K2": turnVolumeUp,
    "K3": turnVolumeDown,
    "K4": playNextTrack,
    "K5": playPreviousTrack,
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
                except KeyError:
                    logger.warning("Button " + keycode + " not mapped to any function.")
                except Exception as exception:
                    print(f"While waiting for server response: {exception}")
except Exception as exception: 
    logger.error('An error with Buttons USB Encoder occurred: %s', repr(exception))