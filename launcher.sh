#!/bin/sh
sleep 5;
cd /home/pi/rpi/;
python3 gui.py >> /home/pi/rpi/gui_log.txt 2>&1
