#!/bin/sh
sleep 5;
cd /home/pi/Desktop/RPI_Modified;
python3 gui.py >> /home/pi/rpi/gui_log.txt 2>&1
