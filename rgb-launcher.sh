#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

sudo pigpiod
python3 /home/pi/repos/raspberrypi-ledstrip/fading.py
