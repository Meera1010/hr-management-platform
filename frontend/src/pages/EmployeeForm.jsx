import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function EmployeeForm() {
  const navigate = useNavigate();
  const [departments, setDepartments] = useState([]);
  const [formData, setFormData] = useState({
    employee_code: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    department_id: '',
    designation: '',
    joining_date: '',
    employment_type: 'Full Time'
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await api.get('/departments/');
        setDepartments(response.data.data);
      } catch (err) {
        console.error('Failed to fetch departments');
      }
    };
    fetchDepartments();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/employees/', formData);
      navigate('/hr/employees');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create employee');
    }
  };

  return (
    <div className="container mt-4">
      <h2>Add New Employee</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      
      <div className="card">
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="row mb-3">
              <div className="col-md-6">
                <label className="form-label">Employee Code</label>
                <input type="text" className="form-control" name="employee_code" value={formData.employee_code} onChange={handleChange} required />
              </div>
              <div className="col-md-6">
                <label className="form-label">Email</label>
                <input type="email" className="form-control" name="email" value={formData.email} onChange={handleChange} required />
              </div>
            </div>

            <div className="row mb-3">
              <div className="col-md-6">
                <label className="form-label">First Name</label>
                <input type="text" className="form-control" name="first_name" value={formData.first_name} onChange={handleChange} required />
              </div>
              <div className="col-md-6">
                <label className="form-label">Last Name</label>
                <input type="text" className="form-control" name="last_name" value={formData.last_name} onChange={handleChange} required />
              </div>
            </div>

            <div className="row mb-3">
              <div className="col-md-6">
                <label className="form-label">Phone</label>
                <input type="text" className="form-control" name="phone" value={formData.phone} onChange={handleChange} />
              </div>
              <div className="col-md-6">
                <label className="form-label">Joining Date</label>
                <input type="date" className="form-control" name="joining_date" value={formData.joining_date} onChange={handleChange} required />
              </div>
            </div>

            <div className="row mb-3">
              <div className="col-md-4">
                <label className="form-label">Department</label>
                <select className="form-select" name="department_id" value={formData.department_id} onChange={handleChange} required>
                  <option value="">Select Department</option>
                  {departments.map(d => (
                    <option key={d.id} value={d.id}>{d.name}</option>
                  ))}
                </select>
              </div>
              <div className="col-md-4">
                <label className="form-label">Designation</label>
                <input type="text" className="form-control" name="designation" value={formData.designation} onChange={handleChange} required />
              </div>
              <div className="col-md-4">
                <label className="form-label">Employment Type</label>
                <select className="form-select" name="employment_type" value={formData.employment_type} onChange={handleChange}>
                  <option value="Full Time">Full Time</option>
                  <option value="Part Time">Part Time</option>
                  <option value="Contract">Contract</option>
                  <option value="Intern">Intern</option>
                </select>
              </div>
            </div>

            <div className="mt-4">
              <button type="submit" className="btn btn-primary me-2">Save Employee</button>
              <button type="button" className="btn btn-secondary" onClick={() => navigate('/hr/employees')}>Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default EmployeeForm;
