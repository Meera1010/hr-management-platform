import api from './api';

export const complianceApi = {
  getGrievances: () => api.get('/compliance/grievances'),
  submitGrievance: (data) => api.post('/compliance/grievances', data),
  getPolicies: () => api.get('/compliance/policies'),
  acknowledgePolicy: (policyId) => api.post(`/compliance/policies/${policyId}/acknowledge`),
  getAuditLogs: () => api.get('/compliance/audit-logs'),
};

export default complianceApi;
