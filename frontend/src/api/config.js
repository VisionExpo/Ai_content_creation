import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Adjust this to match your FastAPI server URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
