#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from plants_api.models import Plant
from plants_api.views import is_admin
from django.contrib.auth.models import User

# Get the admin user (wlasah)
admin_user = User.objects.get(username='wlasah')

# Test if is_admin works
print(f"Admin user 'wlasah' is_admin check: {is_admin(admin_user)}")

# Test the admin_stats logic
plants = Plant.objects.all()
print(f"\nTotal Plants: {plants.count()}")
print(f"Plants needing water (moisture < 50): {plants.filter(moisture__lt=50).count()}")
print(f"Healthy plants (moisture >= 50): {plants.filter(moisture__gte=50).count()}")

if plants.count() > 0:
    avg_moisture = sum([p.moisture for p in plants]) / max(plants.count(), 1)
    print(f"Average moisture: {avg_moisture:.2f}%")
else:
    print("Average moisture: 0%")

print("\n--- Simulated admin_stats response ---")
response_data = {
    'total_plants': plants.count(),
    'needing_water': plants.filter(moisture__lt=50).count(),
    'healthy': plants.filter(moisture__gte=50).count(),
    'average_moisture': sum([p.moisture for p in plants]) / max(plants.count(), 1) if plants.count() > 0 else 0
}
print(response_data)
