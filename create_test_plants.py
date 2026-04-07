#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
except Exception as e:
    print(f"Django setup error: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from plants_api.models import Plant

# Get user4
user = User.objects.filter(username='user4').first()
if not user:
    print('User4 not found')
    # List available users
    users = User.objects.all()
    print(f"Available users: {[u.username for u in users]}")
    sys.exit(1)

# Create some test plants
plants_data = [
    {'name': 'Monstera Deliciosa', 'type': 'Tropical Plant', 'location': 'Living Room', 'moisture': 65},
    {'name': 'Fiddle Leaf Fig', 'type': 'Houseplant', 'location': 'Bedroom', 'moisture': 45},
    {'name': 'Snake Plant', 'type': 'Succulent', 'location': 'Kitchen', 'moisture': 30},
]

for data in plants_data:
    plant, created = Plant.objects.get_or_create(
        owner=user,
        name=data['name'],
        defaults={
            'type': data['type'],
            'location': data['location'],
            'moisture': data['moisture'],
            'description': f'A beautiful {data["type"]}'
        }
    )
    if created:
        print(f'Created plant: {plant.name}')
    else:
        print(f'Plant already exists: {plant.name}')

print(f'\nTotal plants for user4: {Plant.objects.filter(owner=user).count()}')
