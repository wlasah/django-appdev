# Integration Guide - Frontend Apps with Django Backend

This guide shows how to update your React Web App and React Native Mobile App to use the Django backend.

## 🌐 Web App Integration (Smart-Plant-Watering-System)

### 1. Create API Service File
Create `src/services/api.js`:

```javascript
// src/services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (userData) => api.post('/users/register/', userData),
  login: (username, password) => 
    axios.post(`${API_BASE_URL}-token-auth/`, { username, password }),
  logout: () => api.post('/users/logout/'),
  getCurrentUser: () => api.get('/users/me/'),
};

// Plants API
export const plantsAPI = {
  getAllPlants: () => api.get('/plants/'),
  getPlant: (id) => api.get(`/plants/${id}/`),
  createPlant: (plantData) => api.post('/plants/', plantData),
  updatePlant: (id, plantData) => api.put(`/plants/${id}/`, plantData),
  deletePlant: (id) => api.delete(`/plants/${id}/`),
  waterPlant: (id, notes = '') => api.post(`/plants/${id}/water/`, { notes }),
  getPlantsNeedingWater: () => api.get('/plants/needing_water/'),
  getStats: () => api.get('/plants/stats/'),
};

// Watering History API
export const historyAPI = {
  getHistory: () => api.get('/watering-history/'),
  getPlantHistory: (plantId) => api.get(`/watering-history/by_plant/?plant_id=${plantId}`),
};

export default api;
```

### 2. Update App Context to Use Backend
Modify `src/context/AppContext.js` (or create one):

```javascript
import React, { createContext, useState, useCallback } from 'react';
import { plantsAPI, authAPI } from '../services/api';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('auth_token'));

  // Auth functions
  const login = useCallback(async (username, password) => {
    try {
      setLoading(true);
      const response = await authAPI.login(username, password);
      const token = response.data.token;
      localStorage.setItem('auth_token', token);
      setToken(token);
      
      const userResponse = await authAPI.getCurrentUser();
      setUser(userResponse.data);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response.data.detail || 'Login failed' };
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (userData) => {
    try {
      setLoading(true);
      const response = await authAPI.register(userData);
      localStorage.setItem('auth_token', response.data.token);
      setToken(response.data.token);
      setUser(response.data.user);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response.data };
    } finally {
      setLoading(false);
    }
  }, []);

  // Plant functions
  const fetchPlants = useCallback(async () => {
    try {
      setLoading(true);
      const response = await plantsAPI.getAllPlants();
      setPlants(response.data);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const addPlant = useCallback(async (plantData) => {
    try {
      setLoading(true);
      const response = await plantsAPI.createPlant(plantData);
      setPlants([...plants, response.data]);
      return { success: true, plant: response.data };
    } catch (error) {
      return { success: false, error: error.response.data };
    } finally {
      setLoading(false);
    }
  }, [plants]);

  const waterPlant = useCallback(async (plantId, notes) => {
    try {
      const response = await plantsAPI.waterPlant(plantId, notes);
      const updatedPlants = plants.map(p => 
        p.id === plantId ? response.data.plant : p
      );
      setPlants(updatedPlants);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }, [plants]);

  return (
    <AppContext.Provider value={{
      plants,
      user,
      loading,
      login,
      register,
      fetchPlants,
      addPlant,
      waterPlant,
    }}>
      {children}
    </AppContext.Provider>
  );
};
```

### 3. Install axios
```bash
npm install axios
```

---

## 📱 Mobile App Integration (Smart-Plant-Watering-System-Mobile)

### 1. Create API Service File
Create `src/services/api.js`:

```javascript
// src/services/api.js
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'http://192.168.x.x:8000/api'; // Change to your machine IP

// Fetch helper with token
const fetchWithToken = async (endpoint, options = {}) => {
  const token = await AsyncStorage.getItem('auth_token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers.Authorization = `Token ${token}`;
  }
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }
  
  return response.json();
};

export const authAPI = {
  register: (userData) => 
    fetchWithToken('/users/register/', {
      method: 'POST',
      body: JSON.stringify(userData),
    }),
  
  login: (username, password) => 
    fetch(`${API_BASE_URL}-token-auth/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    }).then(r => r.json()),
  
  getCurrentUser: () => fetchWithToken('/users/me/'),
};

export const plantsAPI = {
  getAllPlants: () => fetchWithToken('/plants/', { method: 'GET' }),
  
  createPlant: (plantData) =>
    fetchWithToken('/plants/', {
      method: 'POST',
      body: JSON.stringify(plantData),
    }),
  
  waterPlant: (id, notes = '') =>
    fetchWithToken(`/plants/${id}/water/`, {
      method: 'POST',
      body: JSON.stringify({ notes }),
    }),
  
  getStats: () => fetchWithToken('/plants/stats/', { method: 'GET' }),
};
```

### 2. Update PlantContext to Use Backend
Modify `src/context/PlantContext.js`:

```javascript
import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { plantsAPI, authAPI } from '../services/api';

export const PlantContext = createContext();

export const PlantProvider = ({ children }) => {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  // Initialize - check if user is logged in
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const savedToken = await AsyncStorage.getItem('auth_token');
        if (savedToken) {
          setToken(savedToken);
          await fetchPlants();
        }
      } catch (error) {
        console.error('Auth check error:', error);
      } finally {
        setLoading(false);
      }
    };
    checkAuth();
  }, []);

  const fetchPlants = async () => {
    try {
      const data = await plantsAPI.getAllPlants();
      setPlants(data);
    } catch (error) {
      console.error('Error fetching plants:', error);
    }
  };

  const addPlant = async (plantData) => {
    try {
      const newPlant = await plantsAPI.createPlant(plantData);
      setPlants([...plants, newPlant]);
      return { success: true, plant: newPlant };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const waterPlant = async (plantId, notes = '') => {
    try {
      const response = await plantsAPI.waterPlant(plantId, notes);
      const updatedPlants = plants.map(p =>
        p.id === plantId ? response.plant : p
      );
      setPlants(updatedPlants);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  return (
    <PlantContext.Provider value={{
      plants,
      loading,
      addPlant,
      waterPlant,
      fetchPlants,
      token,
      setToken,
    }}>
      {children}
    </PlantContext.Provider>
  );
};
```

---

## ⚙️ Configuration

### For Web App (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

### For Mobile App
Update `src/services/api.js` with your machine's IP address:
- Find your IP: Open PowerShell and run `ipconfig`
- Look for "IPv4 Address" (typically 192.168.x.x)
- Update API_BASE_URL in api.js

Example:
```javascript
const API_BASE_URL = 'http://192.168.100.5:8000/api';
```

---

## 🔄 Common API Response Patterns

### Success - Get Plants
```javascript
[
  {
    "id": 1,
    "name": "Monstera",
    "type": "Tropical",
    "location": "Living Room",
    "moisture": 50,
    ...
  }
]
```

### Success - Create Plant
```javascript
{
  "id": 1,
  "name": "Monstera",
  ...
  "care_requirements": { ... }
}
```

### Error - Unauthorized (401)
```javascript
{ "detail": "Authentication credentials were not provided." }
```

---

## 🚀 Next Steps

1. Set up Django backend (see QUICK_START.md)
2. Test API with Postman or curl
3. Update web app with API service
4. Update mobile app with API service
5. Test login and plant operations
6. Deploy to production

---

## 📚 Useful Links

- API Documentation: See `API_DOCUMENTATION.md`
- Django REST Framework: https://www.django-rest-framework.org/
- React Documentation: https://react.dev/
- React Native Documentation: https://reactnative.dev/
