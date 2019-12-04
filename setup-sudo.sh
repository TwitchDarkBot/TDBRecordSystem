echo Updating PIP
sudo 'python3 -m pip install -U pip'
echo Installing requirements
sudo 'python3 -m pip install -U requests parse'
echo Install finished.
echo Running setup
python3 setup_copy.py
