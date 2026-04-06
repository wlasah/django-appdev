import urllib.request
import json
import sys

data = {
    'username': 'testuser999',
    'email': 'testuser999@example.com',
    'password': 'password123',
    'password_confirm': 'password123'
}

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/users/register/',
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        print('Status: ' + str(response.status))
        result = response.read().decode()
        print('Response: ' + result)
except urllib.error.HTTPError as e:
    print('Status: ' + str(e.code))
    error_response = e.read().decode()
    print('Error Response: ' + error_response)
    sys.exit(1)
