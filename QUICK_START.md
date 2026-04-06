# Django Backend - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Prerequisites
- Python 3.8 or higher installed
- pip (Python package manager)

### Step 1: Open Terminal in the Backend Folder
```powershell
cd "e:\Smart Plant Watering System\django-backend"
```

### Step 2: Create Virtual Environment
```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment
```powershell
# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```
You should see `(venv)` at the beginning of your terminal line.

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Apply Migrations (Create Database)
```powershell
python manage.py migrate
```

### Step 6: Create Admin Account
```powershell
python manage.py createsuperuser
```
Follow the prompts to create a username, email, and password.

### Step 7: Start the Server
```powershell
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### ✅ Django Backend is Running!

---

## 📱 Testing the Backend

### 1. Admin Panel
Open browser: `http://localhost:8000/admin/`
- Login with your superuser credentials
- Create test plants manually

### 2. Register a New User
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

### 3. Login and Get Token
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### 4. Add a Plant
Replace `YOUR_TOKEN` with the token from step 3:
```bash
curl -X POST http://localhost:8000/api/plants/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monstera",
    "type": "Tropical Plant",
    "location": "Living Room",
    "moisture": 50,
    "care_requirements": {
      "water_frequency": "Every 7 days",
      "light_requirement": "Bright indirect light",
      "temperature": "65-75°F"
    }
  }'
```

---

## 🔗 Next Steps

1. **Update React Web App** to use backend API
   - Replace AsyncStorage with API calls
   - Add login screen
   - Connect plant endpoints

2. **Update React Native Mobile App** to use backend API
   - Replace AsyncStorage with API calls
   - Add login/register screens
   - Connect plant endpoints

See `API_DOCUMENTATION.md` for all available endpoints.

---

## 🐛 Troubleshooting

### Issue: `python: command not found`
**Solution:** Python is not installed or not in PATH
- Download Python from https://www.python.org/
- During installation, check "Add Python to PATH"

### Issue: `No module named 'django'`
**Solution:** Dependencies not installed
```powershell
pip install -r requirements.txt
```

### Issue: `db.sqlite3 not found`
**Solution:** Migrations not applied
```powershell
python manage.py migrate
```

### Issue: Can't connect from React app
**Solution:** CORS not configured properly
- Check that your app's URL is in `CORS_ALLOWED_ORIGINS` in `config/settings.py`
- Make sure Django server is running on port 8000

---

## 📚 Useful Commands

```powershell
# Create new app
python manage.py startapp myapp

# Make migrations
python manage.py makemigrations

# Show migrations
python manage.py showmigrations

# Run tests
python manage.py test

# Create superuser
python manage.py createsuperuser

# Change password
python manage.py changepassword username

# Reset database (careful!)
python manage.py flush

# Shell (interactive Python)
python manage.py shell
```

---

## 📖 Documentation

- Django Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- CORS Setup: https://github.com/adamchainz/django-cors-headers
