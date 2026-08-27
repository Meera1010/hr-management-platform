import api from './api';

export const timesheetApi = {
  getTimesheets: () => api.get('/timesheets/weekly'),
  createTimesheet: (data) => api.post('/timesheets/weekly', data),
  getShifts: () => api.get('/timesheets/shifts'),
  getRosters: () => api.get('/timesheets/rosters'),
  getOvertimeClaims: () => api.get('/timesheets/overtime-claims'),
};

export default timesheetApi;
