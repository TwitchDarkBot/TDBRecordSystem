echo Updating PIP
su -c 'python3 -m pip install -U pip'
echo Installing requirements
su -c 'python3 -m pip install -U requests parse'
echo Install finished.
python3 setup_copy.py