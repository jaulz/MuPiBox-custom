#!/usr/bin/env bash

exec 3>/home/dietpi/.mupibox/autosetup.log; BASH_XTRACEFD=3; PS4=':$LINENO+'; set -x

# Install required utilities
if ! dpkg -s "vim" &> /dev/null; then
    sudo apt-get --yes install vim
fi

# Set up buttons
if ! dpkg -s "python3-evdev" &> /dev/null; then
    sudo apt-get --yes install python3-evdev
fi

sudo cp -v /home/dietpi/MuPiBox-custom/services/mupi_buttons.service /etc/systemd/system/mupi_buttons.service
sudo systemctl daemon-reload
sudo systemctl enable mupi_buttons.service
sudo systemctl restart mupi_buttons.service
