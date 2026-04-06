#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from plants_api.models import Plant
from django.contrib.auth.models import User

print(f"Total Plants in Database: {Plant.objects.count()}")
print(f"Total Users in Database: {User.objects.count()}")

# List all plants
all_plants = Plant.objects.all()
if all_plants.exists():
    print("\nPlants:")
    for plant in all_plants:
        print(f"  - ID: {plant.id}, Name: {plant.name}, Owner: {plant.owner.username if plant.owner else 'None'}, Moisture: {plant.moisture}%")
else:
    print("No plants found in database")

# List all users
all_users = User.objects.all()
if all_users.exists():
    print("\nUsers:")
    for user in all_users:
        print(f"  - ID: {user.id}, Username: {user.username}, is_staff: {user.is_staff}, Plants: {user.plants.count()}")
else:
    print("No users found in database")
