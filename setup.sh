echo Updating PIP
su -c 'python3 -m pip install -U pip'
echo Installing requirements
su -c 'python3 -m pip install -U requests parse streamlink'
echo Install finished.