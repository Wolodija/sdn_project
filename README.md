virtualenv -p python3 .venv
source .venv/bin/activate
pip3 install -r requirements.txt
# floodlight and mininet should be running
python main.py
