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

echo "-- RUN FLASK SCRIPT -- "
# Run database migrations
flask db init
flask db migrate
flask db upgrade

echo "-- RUN PREMADE -- "
python premade.py

echo "-- RUN FLASK APP -- "
python3 -m flask --app ./main.py run --host=0.0.0.0 --port=$PORT
