import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

function Employees() {
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState('');
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  // Edit Modal State
  const [editingEmp, setEditingEmp] = useState(null);
  const [formData, setFormData] = useState({});
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [empRes, deptRes] = await Promise.all([
        api.get('/employees/'),
        api.get('/departments/')
      ]);
      const empList = Array.isArray(empRes.data) ? empRes.data : (empRes.data?.data || []);
      const deptList = Array.isArray(deptRes.data) ? deptRes.data : (deptRes.data?.data || []);
      setEmployees(empList);
      setDepartments(deptList);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch employee records');
      setLoading(false);
    }
  };

  const handleOpenEdit = (emp) => {
    setEditingEmp(emp);
    setFormData({
      first_name: emp.first_name || '',
      last_name: emp.last_name || '',
      email: emp.email || '',
      phone: emp.phone || '',
      designation: emp.designation || '',
      department_id: emp.department_id || '',
      employment_type: emp.employment_type || 'Full Time',
      status: emp.status || 'Active'
    });
  };

  const handleSaveEdit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.put(`/employees/${editingEmp.id}`, formData);
      setSuccessMsg(`Employee ${formData.first_name} updated successfully!`);
      setEditingEmp(null);
      fetchData();
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to update employee');
    } finally {
      setSaving(false);
    }
  };

  const handleToggleStatus = async (emp) => {
    const nextStatus = emp.status === 'Active' ? 'Inactive' : 'Active';
    if (window.confirm(`Change status of ${emp.first_name} ${emp.last_name} to ${nextStatus}?`)) {
      try {
        await api.put(`/employees/${emp.id}`, { status: nextStatus });
        setSuccessMsg(`Status updated to ${nextStatus}`);
        fetchData();
        setTimeout(() => setSuccessMsg(''), 3000);
      } catch (err) {
        setError(err.message || 'Failed to toggle status');
      }
    }
  };

  const filteredEmployees = employees.filter(emp => {
    const term = search.toLowerCase();
    const matchesSearch = `${emp.first_name} ${emp.last_name} ${emp.email} ${emp.employee_code} ${emp.designation}`.toLowerCase().includes(term);
    const matchesStatus = statusFilter ? emp.status === statusFilter : true;
    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return (
      <div className="container mt-4 text-center py-5">
        <div className="spinner-border text-primary" role="status"></div>
        <div className="mt-2 text-muted">Loading employee directory...</div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2>Employee Directory</h2>
          <p className="text-muted mb-0">Manage employee records, roles, departments, and employment status.</p>
        </div>
        <Link to="/hr/employees/new" className="btn btn-primary shadow-sm">
          + Add Employee
        </Link>
      </div>

      {successMsg && <div className="alert alert-success alert-dismissible fade show">{successMsg}</div>}
      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card shadow-sm border-0 mb-4">
        <div className="card-body">
          <div className="row g-3">
            <div className="col-md-7">
              <input
                type="text"
                className="form-control"
                placeholder="Search employees by name, code, email, designation..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <div className="col-md-3">
              <select
                className="form-select"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="">All Statuses</option>
                <option value="Active">Active</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
            <div className="col-md-2">
              <button
                className="btn btn-outline-secondary w-100"
                onClick={() => { setSearch(''); setStatusFilter(''); }}
              >
                Reset
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="card shadow-sm border-0">
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-striped table-hover mb-0 align-middle">
              <thead className="table-dark">
                <tr>
                  <th>Code</th>
                  <th>Full Name</th>
                  <th>Email & Phone</th>
                  <th>Designation</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredEmployees.length > 0 ? (
                  filteredEmployees.map(emp => (
                    <tr key={emp.id}>
                      <td><span className="badge bg-light text-dark border font-monospace">{emp.employee_code}</span></td>
                      <td><strong>{emp.first_name} {emp.last_name}</strong></td>
                      <td>
                        <div>{emp.email}</div>
                        {emp.phone && <small className="text-muted">{emp.phone}</small>}
                      </td>
                      <td>{emp.designation || '-'}</td>
                      <td>
                        <span className={`badge bg-${emp.status === 'Active' ? 'success' : 'secondary'}`}>
                          {emp.status}
                        </span>
                      </td>
                      <td>
                        <Link to={`/hr/employees/${emp.id}`} className="btn btn-sm btn-outline-info me-2">
                          View
                        </Link>
                        <button
                          className="btn btn-sm btn-outline-primary me-2"
                          onClick={() => handleOpenEdit(emp)}
                        >
                          ✏️ Edit
                        </button>
                        <button
                          className={`btn btn-sm ${emp.status === 'Active' ? 'btn-outline-danger' : 'btn-outline-success'}`}
                          onClick={() => handleToggleStatus(emp)}
                        >
                          {emp.status === 'Active' ? 'Deactivate' : 'Activate'}
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="6" className="text-center py-4 text-muted">
                      No employees match your search criteria.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Edit Modal */}
      {editingEmp && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }} tabIndex="-1">
          <div className="modal-dialog modal-dialog-centered modal-lg">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit Employee: {editingEmp.first_name} {editingEmp.last_name}</h5>
                <button type="button" className="btn-close" onClick={() => setEditingEmp(null)}></button>
              </div>
              <form onSubmit={handleSaveEdit}>
                <div className="modal-body">
                  <div className="row g-3">
                    <div className="col-md-6">
                      <label className="form-label fw-semibold">First Name *</label>
                      <input
                        type="text"
                        className="form-control"
                        value={formData.first_name}
                        onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                        required
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold">Last Name *</label>
                      <input
                        type="text"
                        className="form-control"
                        value={formData.last_name}
                        onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                        required
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold">Email *</label>
                      <input
                        type="email"
                        className="form-control"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        required
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold">Phone</label>
                      <input
                        type="text"
                        className="form-control"
                        value={formData.phone}
                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold">Designation</label>
                      <input
                        type="text"
                        className="form-control"
                        value={formData.designation}
                        onChange={(e) => setFormData({ ...formData, designation: e.target.value })}
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold">Department</label>
                      <select
                        className="form-select"
                        value={formData.department_id}
                        onChange={(e) => setFormData({ ...formData, department_id: e.target.value })}
                      >
                        <option value="">Select Department</option>
                        {departments.map(d => (
                          <option key={d.id} value={d.id}>{d.name}</option>
                        ))}
                      </select>
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold">Employment Type</label>
                      <select
                        className="form-select"
                        value={formData.employment_type}
                        onChange={(e) => setFormData({ ...formData, employment_type: e.target.value })}
                      >
                        <option value="Full Time">Full Time</option>
                        <option value="Part Time">Part Time</option>
                        <option value="Contract">Contract</option>
                        <option value="Intern">Intern</option>
                      </select>
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold">Status</label>
                      <select
                        className="form-select"
                        value={formData.status}
                        onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                      >
                        <option value="Active">Active</option>
                        <option value="Inactive">Inactive</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setEditingEmp(null)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary" disabled={saving}>
                    {saving ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Employees;

