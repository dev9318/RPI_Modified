#!/bin/sh
cd /home/pi/Desktop/RPI_Modified
git add .
git commit -m "Update code"
git fetch upstream
git merge upstream/master -m " Merge remote-tracking branch 'upstream/master' "
git push origin master
sleep 5;
killall python3
cd /home/pi/Desktop/RPI_Modified;
python3 gui.py >> /home/pi/Desktop/gui_log.txt 2>&1
