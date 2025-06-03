#!/usr/bin/env bash

sudo systemctl stop mupi_check_monitor.service

echo "{ \"monitor\": \"On\" }" > /home/dietpi/.mupibox/Sonos-Kids-Controller-master/server/config/monitor.json
