import axios from 'axios';

// Get or generate unique session ID
let sessionId = localStorage.getItem('evident_ai_session_id');
if (!sessionId) {
  sessionId = typeof crypto.randomUUID === 'function' 
    ? crypto.randomUUID() 
    : Math.random().toString(36).substring(2) + Date.now().toString(36);
  localStorage.setItem('evident_ai_session_id', sessionId);
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercept requests to add Session ID
api.interceptors.request.use((config) => {
  config.headers['X-Session-ID'] = sessionId;
  return config;
});


export async function uploadDocuments(files) {
  const formData = new FormData();
  for (const file of files) {
    formData.append('files', file);
  }
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
}

export async function askQuestion(question) {
  const response = await api.post('/ask', { question });
  return response.data;
}

export async function getDocuments() {
  const response = await api.get('/documents');
  return response.data;
}

export async function deleteDocument(name) {
  const response = await api.delete(`/documents/${encodeURIComponent(name)}`);
  return response.data;
}

export default api;
