#!/usr/bin/env python
"""
Create test plant data for all users to verify the system works end-to-end
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from plants_api.models import Plant
from datetime import datetime, timedelta

# Sample plants to create
PLANTS_DATA = {
    'user1': [
        {'name': 'Monstera Deliciosa', 'type': 'Tropical Plant', 'location': 'Living Room', 'moisture': 65},
        {'name': 'Snake Plant', 'type': 'Succulent', 'location': 'Bedroom', 'moisture': 30},
    ],
    'user2': [
        {'name': 'Fiddle Leaf Fig', 'type': 'Houseplant', 'location': 'Office', 'moisture': 45},
    ],
    'user4': [
        {'name': 'Pothos', 'type': 'Vine', 'location': 'Bathroom', 'moisture': 50},
        {'name': 'Spider Plant', 'type': 'Houseplant', 'location': 'Kitchen', 'moisture': 55},
        {'name': 'ZZ Plant', 'type': 'Succulent', 'location': 'Living Room', 'moisture': 25},
    ],
    'admin': [
        {'name': 'Orchid', 'type': 'Exotic', 'location': 'Study', 'moisture': 70},
    ],
}

try:
    created_count = 0
    for username, plants in PLANTS_DATA.items():
        user = User.objects.filter(username=username).first()
        if not user:
            print(f'❌ User {username} not found')
            continue
        
        print(f'\n👤 Creating plants for {username}:')
        
        for plant_data in plants:
            # Set last_watered to a random time in the past 7 days
            last_watered = datetime.now() - timedelta(days=2)
            
            plant, created = Plant.objects.get_or_create(
                owner=user,
                name=plant_data['name'],
                defaults={
                    'type': plant_data['type'],
                    'location': plant_data['location'],
                    'moisture': plant_data['moisture'],
                    'last_watered': last_watered,
                    'description': f'A beautiful {plant_data["type"]}'
                }
            )
            
            if created:
                print(f'  ✅ Created: {plant.name} ({plant_data["type"]}) - Moisture: {plant_data["moisture"]}%')
                created_count += 1
            else:
                print(f'  ⚠️ Already exists: {plant.name}')
    
    # Print summary
    total_plants = Plant.objects.count()
    print(f'\n' + '='*50)
    print(f'✅ Summary: Created {created_count} new plants')
    print(f'📊 Total plants in database: {total_plants}')
    print(f'='*50)
    
    # Show breakdown by user
    print(f'\n📈 Plants by user:')
    for user in User.objects.all().order_by('username'):
        count = user.plants.count()
        if count > 0:
            print(f'  {user.username}: {count} plants')

except Exception as e:
    print(f'❌ Error: {e}', file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
