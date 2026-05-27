@echo off
echo Committing and pushing changes to GitHub...
git add .
git commit -m "Update Aerosol Tracker data"
git push
echo Done!
pause
