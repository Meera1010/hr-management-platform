import api from './api';

export const okrApi = {
  getObjectives: (params) => api.get('/okrs/objectives', { params }),
  createObjective: (data) => api.post('/okrs/objectives', data),
  addKeyResult: (objectiveId, data) => api.post(`/okrs/objectives/${objectiveId}/key-results`, data),
  updateKrProgress: (krId, data) => api.post(`/okrs/key-results/${krId}/update-progress`, data),
  getReviewCycles: () => api.get('/okrs/review-cycles'),
  get360Feedback: () => api.get('/okrs/360-feedback'),
  getPips: () => api.get('/okrs/pips'),
};

export default okrApi;
