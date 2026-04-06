"""
Script to create an admin user
Run with: python manage.py shell < create_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create admin user
admin_user = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123456'
)

# Create token for API access
token, created = Token.objects.get_or_create(user=admin_user)

print("✓ Admin user created successfully!")
print(f"  Username: admin")
print(f"  Email: admin@example.com")
print(f"  Password: admin123456")
print(f"  Token: {token.key}")
print(f"\nLogin at: http://localhost:3000/login")
print(f"Admin panel: http://127.0.0.1:8000/admin/")
