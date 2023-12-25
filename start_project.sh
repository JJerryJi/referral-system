#!/bin/bash

# Start Django server
python /app/backend/manage.py makemigrations
python /app/backend/manage.py migrate
python /app/backend/manage.py runserver 0.0.0.0:8000 &

# Navigate to frontend directory and start npm
cd frontend
npm start &

# Move back to the main directory and start Uvicorn server for backend
cd ../backend
uvicorn websocket:app --reload --host 0.0.0.0 --port 8001 &
celery -A referral worker --loglevel=INFO &

# Keep the script running
while true; do
    sleep 60  # Adjust this sleep duration as needed
done