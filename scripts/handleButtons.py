#!/usr/bin/env python3

import sys

from evdev import InputDevice, list_devices

try:
    devices = [InputDevice(fn) for fn in list_devices()]
    i = 0
    print("")
    print("Choose the Buttons USB Encoder device from the list")
    for dev in devices:
        print(i, dev.name)
        i += 1

    dev_id = int(input('Device Number: '))

    print(devices[dev_id].name)
except KeyboardInterrupt:
    sys.exit("Aborted to register Buttons USB Encoder.")