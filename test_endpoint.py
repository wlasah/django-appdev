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
print(f"Admin token: {token.key [:10]}...")
print(f"Is staff: {admin_user.is_staff}")
print(f"\nTotal plants in DB: {Plant.objects.count()}")

# Create a mock request as if it came from the admin
factory = APIRequestFactory()
request = factory.get('/api/plants/admin_stats/')
request.user = admin_user

# Create viewset and call admin_stats
viewset = PlantViewSet()
viewset.request = request
viewset.format_kwarg = None

response = viewset.admin_stats(request)
print(f"\nResponse status: {response.status_code}")
print(f"Response data: {response.data}")
