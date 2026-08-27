import api from './api';

export const payrollApi = {
  getStructures: () => api.get('/payroll/structures'),
  createStructure: (data) => api.post('/payroll/structures', data),
  getEmployeeSalaries: () => api.get('/payroll/employee-salaries'),
  setEmployeeSalary: (data) => api.post('/payroll/employee-salaries', data),
  getRuns: () => api.get('/payroll/runs'),
  executeRun: (data) => api.post('/payroll/runs/execute', data),
  getPayslips: (employeeId) => api.get('/payroll/payslips', { params: { employee_id: employeeId } }),
  getTaxDeclarations: () => api.get('/payroll/tax-declarations'),
  submitTaxDeclaration: (data) => api.post('/payroll/tax-declarations', data),
};

export default payrollApi;
