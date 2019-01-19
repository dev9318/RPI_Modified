git add .
git commit -m "Update code"
git fetch upstream
git merge upstream/master -m " Merge remote-tracking branch 'upstream/master' "
git push origin master
