const HOSTNAME = import.meta.env.VITE_API_HOST || '127.0.0.1';
const PORT = import.meta.env.VITE_API_PORT || '8000';

const API_BASE_URL = `http://${HOSTNAME}:${PORT}`;

export default API_BASE_URL;