#!/usr/bin/env bash
#exec {tracefd}>/home/dietpi/.mupibox/autosetup.log; BASH_XTRACEFD=$tracefd; PS4=':$LINENO+'; set -x

# Install required utilities
sudo apt-get --yes install vim >&3 2>&3

# Set up buttons
sudo apt-get --yes python3-evdev >&3 2>&3

sudo cp -v /home/dietpi/MuPiBox-custom/services/mupi_buttons.service /etc/systemd/system/mupi_buttons.service
sudo systemctl start mupi_buttons.service
sudo systemctl enable mupi_buttons.service