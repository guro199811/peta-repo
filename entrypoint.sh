#!/bin/sh

# Wait for the database to start
#sleep 3

# Navigate to the web-files/website directory inside a cointainer
cd /app

# Set the FLASK_APP environment variable
export FLASK_APP=main.py

# Check if the DYNO environment variable is set (Heroku)
if [ -n "$DYNO" ]; then
  export PORT=$PORT
else
#For local dev set port to 5000
  export PORT=5000
fi

echo "--RUN BABEL --"

# Extract new messages and update the .pot file
pybabel extract -F babel.cfg -o messages.pot .


# Initialize or update the catalog for each language

# Do this step manually whenever you add new languages
#pybabel init -i messages.pot -d translations -l en
#pybabel init -i messages.pot -d translations -l ru


# Update the .po files for each language after extracting new messages
pybabel update -i messages.pot -d translations -l en

# Compile the .po files to .mo files

echo "-- COMPILE BABEL --"
pybabel compile -d translations

echo "-- EXPORT BABEL FILES --"
export FLASK_RUN_EXTRA_FILES=app/translations/en/LC_MESSAGES/messages.mo

echo "-- RUN FLASK SCRIPT -- "
# Run database migrations
flask db init

echo "--Migrating--"
#STOPPING assumtions on database
flask db stamp head
flask db migrate
flask db upgrade

echo "-- RUN PREMADE -- "
python premade.py


echo "-- RUN FLASK APP -- "
python3 -m flask --app ./main.py run --host=0.0.0.0 --port=$PORT
