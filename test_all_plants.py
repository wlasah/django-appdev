#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from plants_api.models import Plant
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from plants_api.views import PlantViewSet

# Get admin user
admin_user = User.objects.get(username='wlasah')
token, _ = Token.objects.get_or_create(user=admin_user)

print(f"Admin user: {admin_user.username}")
print(f"Is staff: {admin_user.is_staff}")
print(f"\nTotal plants in DB: {Plant.objects.count()}")

# Create a mock request as if it came from the admin
factory = APIRequestFactory()
request = factory.get('/api/plants/all_plants/')
request.user = admin_user

# Create viewset and call all_plants
viewset = PlantViewSet()
viewset.request = request
viewset.format_kwarg = None
viewset.action = 'all_plants'  # Set the action so get_serializer_class works

response = viewset.all_plants(request)
print(f"\nResponse status: {response.status_code}")
print(f"Response data count: {len(response.data) if isinstance(response.data, list) else 'N/A'}")
if isinstance(response.data, list):
    print(f"\nFirst plant in response:")
    if len(response.data) > 0:
        print(f"  {response.data[0]}")
else:
    print(f"Response: {response.data}")
