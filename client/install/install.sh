#!/bin/bash

#==== For Twin3d by miksolo ====
# This script installs client for network discovery as a service
#===============================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

#USER_SYSTEMD_DIR=/home/$USER/.config/systemd/user
USER_SYSTEMD_DIR=/etc/systemd/system

# Installing python packages
echo -e "Checking python fiels"

if [ "$(pip3 --version)" -ne 0 ]; then
    sudo apt update
    sudo apt install python3-pip
fi

sudo pip3 install -r $DIR/requirements.txt

client_target_dir=$(realpath $DIR/..)

#Create config
mkdir -p "$client_target_dir/configuration"
cp "$client_target_dir/config.ini" "$client_target_dir/configuration/configuration.ini"

# Create unit file
echo -e "Creating systemctl unit from 'scanner_watchdog.service_temp'"

#mkdir -p $USER_SYSTEMD_DIR
cp "scanner_watchdog.service" "scanner_watchdog.service_temp"

sed -i "s#%CLIENT_PATH#$client_target_dir#g" "scanner_watchdog.service_temp"
sed -i "s#%USER#$USER#g" "scanner_watchdog.service_temp"

sudo cp "scanner_watchdog.service_temp" "$USER_SYSTEMD_DIR/scanner_watchdog.service"

[[ $? -eq 0 ]] && { echo -e "Systemctl unit copied"; }

rm "scanner_watchdog.service_temp"

#Systemctl activation
sudo systemctl  daemon-reload && systemctl restart scanner_watchdog.service
[[ $? -eq 0 ]] && { echo -e "Systemctl started"; }
sudo systemctl  enable scanner_watchdog.service
[[ $? -eq 0 ]] && { echo -e "Systemctl enabled"; }
