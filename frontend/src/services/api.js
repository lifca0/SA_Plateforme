import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token à chaque requête
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth
export const login = (email, password) => api.post('/login', { email, password });
export const getMe = () => api.get('/me');

// Data
export const getData = () => api.get('/data');
export const getItem = (id) => api.get(`/data/${id}`);
export const createData = (data) => api.post('/data', data);
export const updateData = (id, data) => api.put(`/data/${id}`, data);
export const deleteData = (id) => api.delete(`/data/${id}`);

export default api;