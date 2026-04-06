# Smart Plant Watering System - Django Backend

Complete Django REST API backend for connecting your web and mobile apps to a shared database.

## 📁 Project Structure

```
django-backend/
├── config/                 # Django configuration
│   ├── settings.py        # Main settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI config
│   └── __init__.py
├── plants_api/            # Main app
│   ├── models.py          # Database models (Plant, CareRequirements, WateringHistory)
│   ├── views.py           # API endpoints
│   ├── serializers.py     # Data serializers
│   ├── urls.py            # API URLs
│   ├── admin.py           # Admin panel setup
│   ├── tests.py           # Unit tests
│   ├── apps.py
│   ├── migrations/        # Database migrations
│   └── __init__.py
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
├── setup.md              # Detailed setup instructions
├── QUICK_START.md        # Quick start guide
├── API_DOCUMENTATION.md  # Complete API reference
├── INTEGRATION_GUIDE.md  # How to integrate with frontend apps
└── README.md             # This file
```

## 🎯 Features

✅ **User Authentication** - Register, login, token-based auth
✅ **Plant Management** - Create, update, delete plants
✅ **Watering Tracking** - Record watering history with moisture levels
✅ **Care Requirements** - Store plant care instructions
✅ **Statistics** - Get dashboards stats (total plants, needing water, etc.)
✅ **REST API** - Full REST API endpoints
✅ **CORS Support** - Connect from web and mobile apps
✅ **Admin Panel** - Django admin interface for management

## 📊 Database Models

### User
- Extends Django's built-in User model
- Each plant belongs to a specific user

### Plant
- `name`: Plant name
- `type`: Plant type (e.g., Tropical, Succulent)
- `location`: Where the plant is located
- `moisture`: Current moisture level (0-100%)
- `last_watered`: Last watering timestamp
- `owner`: Links to User
- `created_at`, `updated_at`: Timestamps

### CareRequirements
- `water_frequency`: How often to water (e.g., "Every 7 days")
- `light_requirement`: Light needs
- `temperature`: Ideal temperature range
- `humidity`: Optional humidity requirement
- `plant`: Links to specific plant (one-to-one)

### WateringHistory
- `watered_at`: When the plant was watered
- `moisture_before`: Moisture level before watering
- `moisture_after`: Moisture level after watering
- `notes`: Optional notes
- `plant`: Links to specific plant (many-to-one)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Navigate to backend folder
cd "Smart Plant Watering System\django-backend"

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Setup Database
```bash
# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### 3. Run Server
```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`

### 4. Access Admin Panel
Go to: `http://localhost:8000/admin/`

For detailed setup, see [setup.md](setup.md) or [QUICK_START.md](QUICK_START.md)

## 🔗 API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api-token-auth/` - Login (get token)
- `POST /api/users/logout/` - Logout
- `GET /api/users/me/` - Get current user

### Plants
- `GET /api/plants/` - List all plants
- `POST /api/plants/` - Create plant
- `GET /api/plants/{id}/` - Get plant details
- `PUT /api/plants/{id}/` - Update plant
- `DELETE /api/plants/{id}/` - Delete plant
- `POST /api/plants/{id}/water/` - Water a plant
- `GET /api/plants/needing_water/` - Plants needing water
- `GET /api/plants/stats/` - Get statistics

### Watering History
- `GET /api/watering-history/` - All history
- `GET /api/watering-history/by_plant/?plant_id=1` - History for specific plant

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete details.

## 🔌 Integration

### Web App (React)
Create `src/services/api.js` to handle API calls. See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md#web-app-integration).

### Mobile App (React Native)
Update `src/services/api.js` to use the backend. See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md#mobile-app-integration).

Key changes:
- Replace AsyncStorage with API calls
- Add login/register screens
- Update plant state management
- Connect to backend endpoints

## 🧪 Testing API

### Using cURL
```bash
# Register
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123","password_confirm":"pass123"}'

# Login
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# Get plants (replace TOKEN)
curl -X GET http://localhost:8000/api/plants/ \
  -H "Authorization: Token TOKEN"
```

### Using Postman
1. Download [Postman](https://www.postman.com/)
2. Import the API endpoints
3. Set `Authorization` header with token for authenticated requests

## 🔧 Configuration

### CORS Settings
Update `config/settings.py` to allow frontend domains:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # Web app
    "http://192.168.1.100:8081",  # Mobile app
]
```

### Environment Variables
Copy `.env.example` to `.env` and customize:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📚 Documentation

- **Setup**: [setup.md](setup.md)
- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **API Reference**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Integration**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **Django Docs**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/

## ⚠️ Important Notes

1. **Local Development Only**: The current settings are for development. For production:
   - Change `DEBUG = False` in settings
   - Use a strong `SECRET_KEY`
   - Update `ALLOWED_HOSTS`
   - Use environment variables for sensitive data

2. **Database Switch**: Currently using SQLite. To migrate to MySQL/PostgreSQL:
   - Install database driver: `pip install mysqlclient` or `pip install psycopg2`
   - Update `DATABASES` in `config/settings.py`
   - Run migrations: `python manage.py migrate`

3. **CORS**: Allow your app domains in settings if frontend fails to connect

## 🐛 Troubleshooting

**Server won't start?**
- Check Python is installed: `python --version`
- Verify dependencies: `pip install -r requirements.txt`
- Apply migrations: `python manage.py migrate`

**Can't connect from frontend?**
- Ensure Django server is running
- Check CORS_ALLOWED_ORIGINS in settings
- Verify correct API_BASE_URL in frontend

**Database errors?**
- Reset database: `python manage.py flush` (deletes all data)
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`

## 📞 Support

For issues with:
- **Django**: https://docs.djangoproject.com/
- **Django REST**: https://www.django-rest-framework.org/
- **CORS**: https://github.com/adamchainz/django-cors-headers

---

**Created**: April 6, 2026
**Version**: 1.0
**Python**: 3.8+
**Django**: 4.2.0
