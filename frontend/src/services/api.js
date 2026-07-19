import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
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
