import React, { useState, useEffect } from 'react';
import api from '../services/api';

function Departments() {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState('');

  // Modal / Form state
  const [showModal, setShowModal] = useState(false);
  const [editingDept, setEditingDept] = useState(null);
  const [formData, setFormData] = useState({ name: '', description: '', status: 'Active' });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchDepartments();
  }, []);

  const fetchDepartments = async () => {
    try {
      setLoading(true);
      const response = await api.get('/departments/');
      const list = Array.isArray(response.data) ? response.data : (response.data?.data || []);
      setDepartments(list);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch departments');
      setLoading(false);
    }
  };

  const handleOpenAdd = () => {
    setEditingDept(null);
    setFormData({ name: '', description: '', status: 'Active' });
    setError(null);
    setShowModal(true);
  };

  const handleOpenEdit = (dept) => {
    setEditingDept(dept);
    setFormData({ name: dept.name, description: dept.description || '', status: dept.status || 'Active' });
    setError(null);
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      if (editingDept) {
        await api.put(`/departments/${editingDept.id}`, formData);
        setSuccessMsg(`Department "${formData.name}" updated successfully!`);
      } else {
        await api.post('/departments/', formData);
        setSuccessMsg(`Department "${formData.name}" created successfully!`);
      }
      setShowModal(false);
      fetchDepartments();
      setTimeout(() => setSuccessMsg(''), 3500);
    } catch (err) {
      setError(err.message || 'Operation failed');
    } finally {
      setSubmitting(false);
    }
  };

  const handleToggleStatus = async (dept) => {
    const newStatus = dept.status === 'Active' ? 'Inactive' : 'Active';
    if (window.confirm(`Are you sure you want to mark department "${dept.name}" as ${newStatus}?`)) {
      try {
        if (newStatus === 'Inactive') {
          await api.delete(`/departments/${dept.id}`);
        } else {
          await api.put(`/departments/${dept.id}`, { status: 'Active' });
        }
        setSuccessMsg(`Department status updated to ${newStatus}`);
        fetchDepartments();
        setTimeout(() => setSuccessMsg(''), 3000);
      } catch (err) {
        setError(err.message || 'Failed to update status');
      }
    }
  };

  if (loading) {
    return (
      <div className="container mt-4 text-center py-5">
        <div className="spinner-border text-primary" role="status"></div>
        <div className="mt-2 text-muted">Loading departments...</div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2>Departments</h2>
          <p className="text-muted mb-0">Organize and manage organizational departments and teams.</p>
        </div>
        <button id="btn-add-department" className="btn btn-primary shadow-sm" onClick={handleOpenAdd}>
          + Add Department
        </button>
      </div>

      {successMsg && <div className="alert alert-success alert-dismissible fade show">{successMsg}</div>}
      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card shadow-sm border-0">
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-striped table-hover mb-0 align-middle">
              <thead className="table-dark">
                <tr>
                  <th>ID</th>
                  <th>Department Name</th>
                  <th>Description</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {departments.length > 0 ? (
                  departments.map(dept => (
                    <tr key={dept.id}>
                      <td>#{dept.id}</td>
                      <td><strong>{dept.name}</strong></td>
                      <td>{dept.description || <span className="text-muted fst-italic">No description</span>}</td>
                      <td>
                        <span className={`badge bg-${dept.status === 'Active' ? 'success' : 'secondary'}`}>
                          {dept.status}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-sm btn-outline-primary me-2"
                          onClick={() => handleOpenEdit(dept)}
                        >
                          ✏️ Edit
                        </button>
                        <button
                          className={`btn btn-sm ${dept.status === 'Active' ? 'btn-outline-danger' : 'btn-outline-success'}`}
                          onClick={() => handleToggleStatus(dept)}
                        >
                          {dept.status === 'Active' ? 'Deactivate' : 'Activate'}
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="text-center py-4 text-muted">
                      No departments found. Click "+ Add Department" to create one.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Add / Edit Modal */}
      {showModal && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }} tabIndex="-1">
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">{editingDept ? 'Edit Department' : 'Add New Department'}</h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Department Name *</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      placeholder="e.g. Engineering, Sales, Human Resources"
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Description</label>
                    <textarea
                      className="form-control"
                      rows="3"
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      placeholder="Brief overview of department functions..."
                    />
                  </div>
                  {editingDept && (
                    <div className="mb-3">
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
                  )}
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary" disabled={submitting}>
                    {submitting ? 'Saving...' : editingDept ? 'Save Changes' : 'Create Department'}
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

export default Departments;

