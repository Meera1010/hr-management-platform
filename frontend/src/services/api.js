const BASE_URL = 'http://localhost:5001/api';

const getHeaders = () => {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

async function handleResponse(response) {
  const data = await response.json();
  if (!response.ok) {
    return { success: false, message: data.message || 'Something went wrong' };
  }
  return { success: true, data: data.data || data };
}

async function fetchWithAuth(endpoint, options = {}) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...getHeaders(),
      ...options.headers,
    },
  });
  return handleResponse(response);
}

const api = {
  get: (endpoint) => fetchWithAuth(endpoint, { method: 'GET' }),
  post: (endpoint, body) => fetchWithAuth(endpoint, { method: 'POST', body: JSON.stringify(body) }),
  put: (endpoint, body) => fetchWithAuth(endpoint, { method: 'PUT', body: JSON.stringify(body) }),
  delete: (endpoint) => fetchWithAuth(endpoint, { method: 'DELETE' }),
};

export default api;

// Keep original exports but adapt to new api pattern
export const getUsers = async () => {
  const res = await api.get('/users/');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getUser = async (id) => {
  const res = await api.get(`/users/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const createUser = async (data) => {
  const res = await api.post('/users/', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateUser = async (id, data) => {
  const res = await api.put(`/users/${id}`, data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const deactivateUser = async (id) => {
  const res = await api.delete(`/users/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getRoles = async () => {
  const res = await api.get('/roles/');
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getRole = async (id) => {
  const res = await api.get(`/roles/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

// Jobs API
export const getJobs = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  const res = await api.get(`/jobs/?${query}`);
  if (!res.success) throw new Error(res.message);
  return res;
};

export const searchJobs = async (q) => {
  const res = await api.get(`/jobs/search?q=${encodeURIComponent(q)}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const getJob = async (id) => {
  const res = await api.get(`/jobs/${id}`);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const createJob = async (data) => {
  const res = await api.post('/jobs/', data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const updateJob = async (id, data) => {
  const res = await api.put(`/jobs/${id}`, data);
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const changeJobStatus = async (id, status) => {
  const res = await fetchWithAuth(`/jobs/${id}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status })
  });
  if (!res.success) throw new Error(res.message);
  return res.data;
};

export const archiveJob = async (id) => {
  const res = await api.delete(`/jobs/${id}`);
  if (!res.success) throw new Error(res.message);
  return res;
};
