import axios from 'axios';
import { Sweet, User, AuthResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const register = async (user: User): Promise<AuthResponse> => {
  const response = await api.post('/auth/register', user);
  return response.data;
};

export const login = async (username: string, password: string): Promise<AuthResponse> => {
  const response = await api.post('/auth/login', { username, password });
  return response.data;
};

export const getSweets = async (): Promise<Sweet[]> => {
  const response = await api.get('/sweets');
  return response.data;
};

export const searchSweets = async (params: any): Promise<Sweet[]> => {
  const response = await api.get('/sweets/search', { params });
  return response.data;
};

export const createSweet = async (sweet: Omit<Sweet, 'id'>): Promise<Sweet> => {
  const response = await api.post('/sweets', sweet);
  return response.data;
};

export const updateSweet = async (id: number, sweet: Partial<Sweet>): Promise<Sweet> => {
  const response = await api.put(`/sweets/${id}`, sweet);
  return response.data;
};

export const deleteSweet = async (id: number): Promise<void> => {
  await api.delete(`/sweets/${id}`);
};

export const purchaseSweet = async (id: number, quantity: number = 1): Promise<any> => {
  const response = await api.post(`/sweets/${id}/purchase`, { quantity });
  return response.data;
};

export default api;
