cd /home/enlightened/Desktop/try/RPi-Logs
git add .
git commit -m "Update logs"
git fetch upstream
git merge upstream/master -m " Merge remote-tracking branch 'upstream/master' "
git push origin master
