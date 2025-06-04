#!/usr/bin/env bash

exec 3>/home/dietpi/.mupibox/autosetup.log; BASH_XTRACEFD=3; PS4=':$LINENO+'; set -x

# Install required utilities
sudo apt-get --yes install vim >&3 2>&3

# Set up buttons
sudo apt-get --yes python3-evdev >&3 2>&3

sudo cp -v /home/dietpi/MuPiBox-custom/services/mupi_buttons.service /etc/systemd/system/mupi_buttons.service
sudo systemctl start mupi_buttons.service
sudo systemctl enable mupi_buttons.service