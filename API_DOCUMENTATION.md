# Smart Plant Watering System - API Documentation

## Base URL
`http://localhost:8000/api/`

## Authentication
All endpoints (except registration and login) require a token in the Authorization header:
```
Authorization: Token YOUR_AUTH_TOKEN
```

---

## User Endpoints

### 1. Register User
- **Endpoint:** `POST /api/users/register/`
- **Permission:** Public
- **Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securePassword123",
  "password_confirm": "securePassword123"
}
```
- **Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "token": "abc123def456ghi789"
}
```

### 2. Get Current User Profile
- **Endpoint:** `GET /api/users/me/`
- **Permission:** Authenticated
- **Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 3. Get Auth Token (Login)
- **Endpoint:** `POST /api-token-auth/`
- **Permission:** Public
- **Request Body:**
```json
{
  "username": "john_doe",
  "password": "securePassword123"
}
```
- **Response:**
```json
{
  "token": "abc123def456ghi789"
}
```

### 4. Logout
- **Endpoint:** `POST /api/users/logout/`
- **Permission:** Authenticated
- **Response:**
```json
{
  "message": "Logged out successfully"
}
```

---

## Plant Endpoints

### 1. Get All Plants (for current user)
- **Endpoint:** `GET /api/plants/`
- **Permission:** Authenticated
- **Response:**
```json
[
  {
    "id": 1,
    "name": "Monstera Deliciosa",
    "type": "Tropical Plant",
    "location": "Living Room",
    "moisture": 45,
    "last_watered": "2024-04-04T10:30:00Z",
    "description": "A beautiful tropical plant",
    "care_requirements": {
      "id": 1,
      "water_frequency": "Every 7 days",
      "light_requirement": "Bright indirect light",
      "temperature": "68-86°F",
      "humidity": null
    },
    "watering_history": [],
    "created_at": "2024-04-04T10:00:00Z"
  }
]
```

### 2. Create a New Plant
- **Endpoint:** `POST /api/plants/`
- **Permission:** Authenticated
- **Request Body:**
```json
{
  "name": "Monstera Deliciosa",
  "type": "Tropical Plant",
  "location": "Living Room",
  "moisture": 50,
  "description": "A beautiful tropical plant",
  "care_requirements": {
    "water_frequency": "Every 7 days",
    "light_requirement": "Bright indirect light",
    "temperature": "68-86°F",
    "humidity": "60-80%"
  }
}
```

### 3. Get Plant Details
- **Endpoint:** `GET /api/plants/{id}/`
- **Permission:** Authenticated
- **Response:** Same as Get All Plants (single plant object)

### 4. Update Plant
- **Endpoint:** `PUT /api/plants/{id}/`
- **Permission:** Authenticated (owner only)
- **Request Body:** Same as Create Plant

### 5. Delete Plant
- **Endpoint:** `DELETE /api/plants/{id}/`
- **Permission:** Authenticated (owner only)

### 6. Water a Plant
- **Endpoint:** `POST /api/plants/{id}/water/`
- **Permission:** Authenticated (owner only)
- **Request Body:**
```json
{
  "notes": "Plant looks healthy"
}
```
- **Response:**
```json
{
  "message": "Monstera Deliciosa has been watered!",
  "plant": {
    "id": 1,
    "name": "Monstera Deliciosa",
    "moisture": 65,
    "last_watered": "2024-04-06T14:25:00Z"
  }
}
```

### 7. Get Plants Needing Water
- **Endpoint:** `GET /api/plants/needing_water/`
- **Permission:** Authenticated
- **Response:** Array of plants with moisture < 40%

### 8. Get Plant Statistics
- **Endpoint:** `GET /api/plants/stats/`
- **Permission:** Authenticated
- **Response:**
```json
{
  "total_plants": 3,
  "needing_water": 1,
  "healthy": 2,
  "average_moisture": 48.5
}
```

---

## Watering History Endpoints

### 1. Get All Watering History
- **Endpoint:** `GET /api/watering-history/`
- **Permission:** Authenticated (returns only current user's plants)
- **Response:**
```json
[
  {
    "id": 1,
    "watered_at": "2024-04-06T14:25:00Z",
    "moisture_before": 45,
    "moisture_after": 65,
    "notes": "Plant looks healthy"
  }
]
```

### 2. Get Watering History for Specific Plant
- **Endpoint:** `GET /api/watering-history/by_plant/?plant_id=1`
- **Permission:** Authenticated
- **Response:** Array of watering history for specified plant

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Admin Panel
Access at: `http://localhost:8000/admin/`

Login with your superuser credentials created during setup.
