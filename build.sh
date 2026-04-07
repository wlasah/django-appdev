#!/bin/bash
# Render build script - runs before starting the web service

echo "Starting Django migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"
