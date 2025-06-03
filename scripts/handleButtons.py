#!/usr/bin/env python3

import sys

import logging
from evdev import InputDevice, list_devices, categorize, ecodes, KeyEvent

logger = logging.getLogger(__name__)

# Get device 
try:
    devices = [InputDevice(fn) for fn in list_devices()]
    i = 0
    print("")
    print("Choose the Buttons USB Encoder device from the list")
    for dev in devices:
        print(i, dev.name)
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