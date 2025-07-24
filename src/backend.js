import axios from 'axios';

// Base configuration
const apiClient = axios.create({
  baseURL: 'http://172.26.50.145', // Base IP
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // Optional: request timeout in ms
});

// Sign In API
export const signIn = (email, password) => {
  return apiClient.post('/signIn', {
      email,
      password,
    });
};