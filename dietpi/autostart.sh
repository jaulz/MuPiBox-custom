#!/bin/bash

echo "echo '' && echo '' && echo 'Please wait, MuPiBox-Installer starts soon...' && sleep 10" >> /home/dietpi/.bashrc
echo "cd; curl -L https://raw.githubusercontent.com/splitti/MuPiBox/main/autosetup/autosetup.sh | bash" >> /home/dietpi/.bashrc

# Install required utilities
sudo apt-get --yes install python3-evdev vim >&3 2>&3

# Clone custom scripts
git clone https://github.com/jaulz/MuPiBox-custom.git /home/dietpi/MuPiBox-custom

# Set up buttons
sudo apt-get --yes python3-evdev vim >&3 2>&3

sudo cp -v /home/dietpi/MuPiBox-custom/services/mupi_buttons.service /etc/systemd/system/mupi_buttons.service
sudo systemctl start mupi_buttons.service
sudo systemctl enable mupi_buttons.service

reboot
