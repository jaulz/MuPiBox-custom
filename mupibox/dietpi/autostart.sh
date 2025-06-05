#!/bin/bash

echo "echo '' && echo '' && echo 'Please wait, MuPiBox-Installer starts soon...' && sleep 10" >> /home/dietpi/.bashrc
echo "cd; curl -L https://raw.githubusercontent.com/splitti/MuPiBox/main/autosetup/autosetup.sh | bash" >> /home/dietpi/.bashrc

# Setup custom scripts
git clone https://github.com/jaulz/MuPiBox-custom.git /home/dietpi/MuPiBox-custom

. /home/dietpi/MuPiBox-custom/scripts/setup.sh

# Reboot at last
reboot
