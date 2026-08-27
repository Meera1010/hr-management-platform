import api from './api';

export const workforceApi = {
  getPlans: () => api.get('/workforce/plans'),
  getAttritionRisks: () => api.get('/workforce/attrition-risks'),
  evaluateRisk: (employeeId) => api.post(`/workforce/evaluate-attrition/${employeeId}`),
  getBenchmarks: () => api.get('/workforce/benchmarks'),
};

export default workforceApi;
