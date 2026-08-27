import React, { useState, useEffect } from 'react';
import { getRoles } from '../services/api';

const UserForm = ({ initialData, onSubmit, onCancel, roles }) => {
  const [formData, setFormData] = useState(
    initialData || {
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      password: '',
      role_id: '',
      is_active: true
    }
  );

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label className="form-label">First Name *</label>
        <input type="text" className="form-control" name="first_name" value={formData.first_name} onChange={handleChange} required />
      </div>
      <div className="mb-3">
        <label className="form-label">Last Name *</label>
        <input type="text" className="form-control" name="last_name" value={formData.last_name} onChange={handleChange} required />
      </div>
      <div className="mb-3">
        <label className="form-label">Email *</label>
        <input type="email" className="form-control" name="email" value={formData.email} onChange={handleChange} required />
      </div>
      <div className="mb-3">
        <label className="form-label">Phone</label>
        <input type="text" className="form-control" name="phone" value={formData.phone || ''} onChange={handleChange} />
      </div>
      <div className="mb-3">
        <label className="form-label">Password {initialData ? '(Leave blank to keep unchanged)' : '*'}</label>
        <input type="password" className="form-control" name="password" value={formData.password || ''} onChange={handleChange} required={!initialData} minLength={6} />
      </div>
      <div className="mb-3">
        <label className="form-label">Role *</label>
        <select className="form-select" name="role_id" value={formData.role_id} onChange={handleChange} required>
          <option value="">Select a role</option>
          {roles.map(role => (
            <option key={role.id} value={role.id}>{role.name}</option>
          ))}
        </select>
      </div>
      <div className="mb-3 form-check">
        <input type="checkbox" className="form-check-input" name="is_active" id="isActive" checked={formData.is_active} onChange={handleChange} />
        <label className="form-check-label" htmlFor="isActive">Is Active</label>
      </div>
      
      <div className="d-flex justify-content-end gap-2">
        <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
        <button type="submit" className="btn btn-primary">Save User</button>
      </div>
    </form>
  );
};

export default UserForm;
