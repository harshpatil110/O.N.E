import axios from 'axios';

const VITE_API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const login = async (email, password) => {
  const response = await axios.post(`${VITE_API_URL}/api/v1/auth/login`, {
    email,
    password,
  });
  return response.data;
};
