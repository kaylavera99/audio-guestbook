#!/bin/bash
source /home/pi/audio-guestbook/venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
cd /home/pi/audio-guestbook
flask run --host=0.0.0.0 --port=5000
