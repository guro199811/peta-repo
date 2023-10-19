#!/bin/sh

# Wait for the database to start
sleep 3

# Navigate to the web-files/website directory
cd /app

# Set the FLASK_APP environment variable
export FLASK_APP=main.py

echo "-- RUN FLASK SCRIPT -- "
# Run database migrations
flask db init
flask db migrate
flask db upgrade

echo "-- RUN PREMADE PY -- "
python premade.py
python3 -m flask --app ./main.py run --host=0.0.0.0
# python main.py