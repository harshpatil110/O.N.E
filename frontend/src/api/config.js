import axios from 'axios';

const VITE_API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const authAxios = axios.create({
  baseURL: VITE_API_URL,
  timeout: 180000, // 180 seconds to allow multi-step MCP agent executions
});

authAxios.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});
