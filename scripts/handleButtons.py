#!/usr/bin/env python3

import sys

import logging
import subprocess
from evdev import InputDevice, list_devices, categorize, ecodes, KeyEvent

logger = logging.getLogger(__name__)

# Functions
def playTestSound():
    subprocess.call(["aplay", "/usr/share/sounds/alsa/Front_Center.wav"])

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
    "K1": playTestSound,
    "K2": playTestSound,
    "K3": playTestSound,
    "K4": playTestSound,
    "K5": playTestSound,
}

# Get device 
try:
    devices = [InputDevice(fn) for fn in list_devices()]
    i = 0
    print("")
    print("Choose the Buttons USB Encoder device from the list")

    for device in devices:
        print(i, device.name)
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