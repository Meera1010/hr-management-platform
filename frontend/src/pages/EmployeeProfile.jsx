import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';

function EmployeeProfile() {
  const { id } = useParams();
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEmployee = async () => {
      try {
        const response = await api.get(`/employees/${id}`);
        setEmployee(response.data.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch employee details');
        setLoading(false);
      }
    };
    fetchEmployee();
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="alert alert-danger">{error}</div>;
  if (!employee) return <div>Employee not found</div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Employee Profile</h2>
        <Link to="/hr/employees" className="btn btn-secondary">Back to List</Link>
      </div>

      <div className="card">
        <div className="card-header bg-dark text-white">
          <h4>{employee.first_name} {employee.last_name}</h4>
        </div>
        <div className="card-body row">
          <div className="col-md-6">
            <p><strong>Employee Code:</strong> {employee.employee_code}</p>
            <p><strong>Email:</strong> {employee.email}</p>
            <p><strong>Phone:</strong> {employee.phone}</p>
            <p><strong>Status:</strong> {employee.status}</p>
          </div>
          <div className="col-md-6">
            <p><strong>Designation:</strong> {employee.designation}</p>
            <p><strong>Employment Type:</strong> {employee.employment_type}</p>
            <p><strong>Joining Date:</strong> {new Date(employee.joining_date).toLocaleDateString()}</p>
            <p><strong>Department ID:</strong> {employee.department_id}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EmployeeProfile;
