#!/bin/bash
clear

FLAG="$1"
FULL="Full"
echo Starting Update...

sleep 3

sudo apt update

if [ "$FLAG" == "$FULL" ]; then
echo Beginning Full Upgrade...
sleep 5
sudo apt full-upgrade
else
echo To run a full upgrade, Type \"Full\" into the argument.
fi

sudo reboot --r now

