# Django Backend Setup Instructions

## Initial Setup

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/
   - Make sure to check "Add Python to PATH" during installation

2. **Create a virtual environment**
   ```
   python -m venv venv
   ```

3. **Activate virtual environment**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```
   python manage.py migrate
   ```

6. **Create a superuser (admin account)**
   ```
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```
   python manage.py runserver
   ```

The server will run on: http://127.0.0.1:8000/

## Admin Panel
Access at: http://127.0.0.1:8000/admin/

## API Endpoints
- Plants: http://127.0.0.1:8000/api/plants/
- Users: http://127.0.0.1:8000/api/users/
- Watering History: http://127.0.0.1:8000/api/watering-history/
