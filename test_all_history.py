#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from plants_api.models import WateringHistory
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from plants_api.views import WateringHistoryViewSet

# Get admin user
admin_user = User.objects.get(username='wlasah')
token, _ = Token.objects.get_or_create(user=admin_user)

print(f"Admin user: {admin_user.username}")
print(f"Is staff: {admin_user.is_staff}")
print(f"\nTotal watering history in DB: {WateringHistory.objects.count()}")

# Create a mock request as if it came from the admin
factory = APIRequestFactory()
request = factory.get('/api/watering-history/all_history/')
request.user = admin_user

# Create viewset and call all_history
viewset = WateringHistoryViewSet()
viewset.request = request
viewset.format_kwarg = None
viewset.action = 'all_history'

response = viewset.all_history(request)
print(f"\nResponse status: {response.status_code}")
print(f"Response data count: {len(response.data) if isinstance(response.data, list) else 'N/A'}")
if isinstance(response.data, list):
    print(f"\nWatering history entries from all users:")
    if len(response.data) > 0:
        print(f"First entry: {response.data[0]}")
        for entry in response.data[:3]:  # Show first 3
            print(f"  - Watered at: {entry['watered_at']}, Moisture: {entry['moisture_before']}% → {entry['moisture_after']}%")
else:
    print(f"Response: {response.data}")
