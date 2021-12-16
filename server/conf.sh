#!/bin/bash

#==== For Twin3d by miksolo ====
# This script for common configuration
#===============================

LOGGING_TO_DRIVE=1


LOG_DIR=$DIR/logs

MEM_DIR=/dev/shm/3d_capture
mkdir -p $MEM_DIR
mkdir -p $MEM_DIR/logs
mkdir -p $DIR/logs


if [[ $LOGGING_TO_DRIVE -eq 1 ]]; then
  export LOG_DIR=$DIR/logs
else
  export LOG_DIR=$MEM_DIR/logs
fi



if [[ $SCANNER == "SMALL" ]]; then
  
  SCANNER_MQTT_IP="192.160.21.19"
  PLUG_IP="192.160.21.140"
  PLUG_TOKEN="56a298c71d5d4ac8a13f6244971dd031"

elif [[ $SCANNER == "BIG" ]]; then
  
  SCANNER_MQTT_IP="192.160.21.48"
  PLUG_IP="192.160.21.125"
  PLUG_TOKEN="5608394216efaf02f2f04032de74052a"
  #192.160.21.49 	a8:a1:59:5d:dc:26 tac@cisco.com

elif [[ $SCANNER == "PHONES" ]];then
  echo "Phones"
  users+=("pi")
  ips+=("192.160.21.10") #raspberrypi10
  
  RASP_IP="192.160.21.10"
  RASP_USER="pi"
  IPHONE_SAVED_DATA="/home/pi/iphone_saved_data"
  ANDROID_DIR="/home/$RASP_USER/servers/android"
  ANDROID_IMGS_DIR="Internal\ shared\ storage/DCIM/Camera"

  # Variebles local to raspberry pi!
  IPHONE_DIR="/home/$RASP_USER/servers/iphone"
  IPHONE_SAVED_DATA="/home/$RASP_USER/iphone_saved_data"

  PHONE_CONTROL_DIR="/home/$RASP_USER/git/3d_automation/phone_scripts"
  
else

  #ips+=("192.160.21.6")
  #users+=("pi") #pass = воздух787
  #ips+=("192.160.21.8")
  #users+=("dev1")
  #cameras+=(20)
  #ips+=("192.160.21.2")
  #users+=("dev1")
  #ips+=("192.160.21.22")
  #users+=("dev1")
  #ips+=("192.160.21.23")
  #users+=("dev1")
  #ips+=("192.160.21.122")
  #users+=("dev1")
  #cameras+=(19)
  #ips+=("192.160.21.8")
  #users+=("dev1")
  #cameras+=(20)


  #ips+=("192.160.21.7") # raspberrypi
  #users+=("pi") #pass = twin787898
  echo "No scanner specified. Use < ./command SMALL > for example. "
  exit 1
fi


declare -a ips ; declare -a users ;  declare -a cameras #declare arrays

REMOTE_SAVE_DIR="$HOME/Pictures/3d/SAVE_$SCANNER"
TARGET_DIR=git/3d_automation/scrach

LOCAL_SHOTS_DIR=$TARGET_DIR/temp




GIT_DIRECTORY="/home/pi/git/3d_automation"