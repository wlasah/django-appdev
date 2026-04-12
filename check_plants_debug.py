#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_plant_system.settings')
django.setup()

from plants_api.models import Plant

print("[PLANTS DEBUG]")
all_plants = Plant.objects.all()
print(f"Total plants in DB: {all_plants.count()}")
print("\nPlant details:")
for plant in all_plants:
    owner_name = plant.owner.username if plant.owner else "Unknown"
    print(f"  - {plant.name} (ID: {plant.id}): moisture={plant.moisture}%, owner={owner_name}")

print("\n[STATS CALCULATION]")
healthy = all_plants.filter(moisture__gte=50).count()
needs_water = all_plants.filter(moisture__lt=50).count()
print(f"Healthy (moisture >= 50%): {healthy}")
print(f"Needs Water (moisture < 50%): {needs_water}")

critical = all_plants.filter(moisture__lt=30).count()
warning = all_plants.filter(moisture__gte=30, moisture__lt=50).count()
print(f"Critical (moisture < 30%): {critical}")
print(f"Warning (30% <= moisture < 50%): {warning}")
