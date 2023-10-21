#!/bin/sh

# Wait for the database to start
#sleep 3

# Navigate to the web-files/website directory
cd /app

# Set the FLASK_APP environment variable
export FLASK_APP=main.py

# Check if the DYNO environment variable is set (Heroku specific)
if [ -n "$DYNO" ]; then
  # Set the PORT to the Heroku environment variable
  export PORT=$PORT
else
  # Set the PORT to 5000 for local development
  export PORT=5000
fi

echo "-- RUN FLASK SCRIPT -- "
# Run database migrations
flask db init
flask db migrate
flask db upgrade

echo "-- RUN PREMADE -- "
python premade.py

echo "-- RUN FLASK APP -- "
python3 -m flask --app ./main.py run --host=0.0.0.0 --port=$PORT
