import api from './api';

export const expenseApi = {
  getCategories: () => api.get('/expenses/categories'),
  getClaims: () => api.get('/expenses/claims'),
  submitClaim: (data) => api.post('/expenses/claims', data),
  getTravelRequests: () => api.get('/expenses/travel-requests'),
  createTravelRequest: (data) => api.post('/expenses/travel-requests', data),
};

export default expenseApi;
