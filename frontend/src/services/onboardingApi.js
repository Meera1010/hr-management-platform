import api from './api';

export const onboardingApi = {
  getChecklists: () => api.get('/lifecycle/onboarding/checklists'),
  initiateOnboarding: (data) => api.post('/lifecycle/onboarding/checklists/initiate', data),
  toggleTask: (taskId) => api.post(`/lifecycle/onboarding/tasks/${taskId}/toggle`),
  getResignations: () => api.get('/lifecycle/resignations'),
  submitResignation: (data) => api.post('/lifecycle/resignations', data),
  updateClearance: (resignationId, data) => api.post(`/lifecycle/resignations/${resignationId}/clearance`, data),
  getFnFSettlements: () => api.get('/lifecycle/fnf-settlements'),
  calculateFnF: (data) => api.post('/lifecycle/fnf-settlements/calculate', data),
};

export default onboardingApi;
