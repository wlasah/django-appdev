import requests
import json

data = {
    'username': 'testadmin123',
    'email': 'testadmin@example.com',
    'password': 'admin123456',
    'password_confirm': 'admin123456'
}

print("Testing registration endpoint...")
print(f"Sending: {json.dumps(data, indent=2)}")

try:
    response = requests.post(
        'http://127.0.0.1:8000/api/users/register/',
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
