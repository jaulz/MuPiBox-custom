#!/usr/bin/env bash

# Install required utilities
if ! dpkg -s "vim" &> /dev/null; then
    sudo apt-get --yes install vim
fi

# Set up buttons
if ! dpkg -s "python3-evdev" &> /dev/null; then
    sudo apt-get --yes install python3-evdev
fi

sudo cp -v ${0%/*}/../services/buttons.service /etc/systemd/system/buttons.service
sudo systemctl daemon-reload
sudo systemctl enable buttons.service
sudo systemctl restart buttons.service
