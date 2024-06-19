#!/bin/sh

cd /app

echo "-- RUN PREMADE --"
python3 ./backing-pet/premade.py

echo "-- RUN FLASKAPP --"
python3 -m flask --app ./backing-pet/main.py run --host=0.0.0.0 --port=5000