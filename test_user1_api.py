#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from plants_api.models import Plant
from rest_framework.authtoken.models import Token

# Get user1
user1 = User.objects.filter(username='user1').first()
if not user1:
    print("❌ user1 not found")
    sys.exit(1)

print(f"✅ user1 found (ID: {user1.id})")

# Check plants owned by user1
plants = Plant.objects.filter(owner=user1)
print(f"\n📊 Plants owned by user1: {plants.count()}")
for p in plants:
    print(f"   - {p.name} (ID: {p.id}, Owner: {p.owner.username})")

# Get or create token
token, created = Token.objects.get_or_create(user=user1)
print(f"\n🔑 Token for user1: {token.key[:20]}...")

# Test the API response directly
from rest_framework.test import APIRequestFactory
from plants_api.views import PlantViewSet

factory = APIRequestFactory()
request = factory.get('/api/plants/')
request.user = user1

viewset = PlantViewSet()
viewset.request = request
viewset.format_kwarg = None

response = viewset.list(request)
print(f"\n📡 API Response for /plants/:")
print(f"   Status: {response.status_code}")
print(f"   Data count: {len(response.data) if isinstance(response.data, list) else 'N/A'}")
if isinstance(response.data, list) and response.data:
    print(f"   First plant: {response.data[0]}")
else:
    print(f"   Data: {response.data}")
