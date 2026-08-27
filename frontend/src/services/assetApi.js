import api from './api';

export const assetApi = {
  getCategories: () => api.get('/assets/categories'),
  createCategory: (data) => api.post('/assets/categories', data),
  getAssets: (params) => api.get('/assets', { params }),
  createAsset: (data) => api.post('/assets', data),
  assignAsset: (assetId, data) => api.post(`/assets/${assetId}/assign`, data),
  returnAsset: (assetId, data) => api.post(`/assets/${assetId}/return`, data),
  getMyAssets: () => api.get('/assets/my-assets'),
  getItTickets: () => api.get('/assets/tickets'),
  createItTicket: (data) => api.post('/assets/tickets', data),
};

export default assetApi;
