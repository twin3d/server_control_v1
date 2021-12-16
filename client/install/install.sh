#!/bin/bash

#==== For Twin3d by miksolo ====
# This script installs client for network discovery as a service
#===============================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"


# Installing python packages

if [ "$(pip3 --version)" -ne 0 ]; then
    sudo apt update
    sudo apt install python3-pip
fi

pip3 install -r $DIR/requirements.txt

client_target_dir=$(realpath $DIR/..)

#Create config
mkdir -p "$client_target_dir/configuration"
cp "$client_target_dir/config.ini" "$client_target_dir/configuration/configuration.ini"

# Create unit file
USER_SYSTEMD_DIR=/home/$USER/.config/systemd/user
mkdir -p $USER_SYSTEMD_DIR

cp "scanner_watchdog.service" "scanner_watchdog.service_temp"

sed -i "s#%CLIENT_PATH#$client_target_dir#g" "scanner_watchdog.service_temp"
sed -i "s#%USER#$USER#g" "scanner_watchdog.service_temp"

cp "scanner_watchdog.service_temp" "$USER_SYSTEMD_DIR/scanner_watchdog.service"

rm "scanner_watchdog.service_temp"

systemctl --user daemon-reload && systemctl --user restart scanner_watchdog.service
systemctl --user restart scanner_watchdog.service
systemctl --user enable scanner_watchdog.service