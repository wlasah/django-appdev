#!/bin/bash
# Render build script - runs before starting the web service

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting Django migrations..."
python manage.py migrate --verbosity=2

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if it doesn't exist..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='wlasah').exists():
    User.objects.create_superuser('wlasah', 'admin@example.com', 'password')
    print("Superuser created: wlasah")
else:
    print("Superuser already exists")
END

echo "Build complete!"
