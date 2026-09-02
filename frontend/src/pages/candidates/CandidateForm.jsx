import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

function CandidateForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id);

  const [formData, setFormData] = useState({
    candidate_code: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    education: '',
    experience_years: 0,
    current_role: '',
    skills: '',
    certifications: '',
    location: '',
    status: 'Available'
  });
  const [loading, setLoading] = useState(isEdit);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isEdit) {
      const fetchCandidate = async () => {
        try {
          const res = await api.getCandidate(id);
          const c = res?.candidate || res?.data?.candidate || res?.data || res || {};
          setFormData({
            candidate_code: c.candidate_code || '',
            first_name: c.first_name || '',
            last_name: c.last_name || '',
            email: c.email || '',
            phone: c.phone || '',
            education: c.education || '',
            experience_years: c.experience_years || 0,
            current_role: c.current_role || '',
            skills: c.skills || '',
            certifications: c.certifications || '',
            location: c.location || '',
            status: c.status || 'Available'
          });
        } catch (err) {
          setError(err.message || err.response?.data?.message || 'Failed to fetch candidate');
        } finally {
          setLoading(false);
        }
      };
      fetchCandidate();
    }
  }, [id, isEdit]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'experience_years' ? Number(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      if (isEdit) {
        await api.updateCandidate(id, formData);
      } else {
        await api.createCandidate(formData);
      }
      navigate('/hr/candidates');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to save candidate');
    }
  };

  if (loading) return <div className="text-center mt-5"><div className="spinner-border text-primary" /></div>;

  return (
    <div className="container mt-4">
      <h2>{isEdit ? 'Edit Candidate' : 'Add Candidate'}</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      
      <div className="card shadow-sm mt-4">
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <h5 className="mb-3">Basic Information</h5>
            <div className="row g-3 mb-4">
              <div className="col-md-4">
                <label className="form-label">Candidate Code</label>
                <input type="text" className="form-control" name="candidate_code" value={formData.candidate_code} onChange={handleChange} required />
              </div>
              <div className="col-md-4">
                <label className="form-label">First Name</label>
                <input type="text" className="form-control" name="first_name" value={formData.first_name} onChange={handleChange} required />
              </div>
              <div className="col-md-4">
                <label className="form-label">Last Name</label>
                <input type="text" className="form-control" name="last_name" value={formData.last_name} onChange={handleChange} required />
              </div>
              <div className="col-md-6">
                <label className="form-label">Email</label>
                <input type="email" className="form-control" name="email" value={formData.email} onChange={handleChange} required />
              </div>
              <div className="col-md-6">
                <label className="form-label">Phone</label>
                <input type="text" className="form-control" name="phone" value={formData.phone} onChange={handleChange} />
              </div>
              <div className="col-md-6">
                <label className="form-label">Location</label>
                <input type="text" className="form-control" name="location" value={formData.location} onChange={handleChange} />
              </div>
            </div>

            <h5 className="mb-3">Professional Details</h5>
            <div className="row g-3 mb-4">
              <div className="col-md-4">
                <label className="form-label">Current Role</label>
                <input type="text" className="form-control" name="current_role" value={formData.current_role} onChange={handleChange} />
              </div>
              <div className="col-md-4">
                <label className="form-label">Experience (Years)</label>
                <input type="number" className="form-control" name="experience_years" value={formData.experience_years} onChange={handleChange} min="0" required />
              </div>
              <div className="col-md-4">
                <label className="form-label">Education</label>
                <input type="text" className="form-control" name="education" value={formData.education} onChange={handleChange} />
              </div>
              <div className="col-md-12">
                <label className="form-label">Skills (comma separated)</label>
                <textarea className="form-control" name="skills" value={formData.skills} onChange={handleChange} rows="2" placeholder="e.g., Python, React, SQL"></textarea>
              </div>
              <div className="col-md-12">
                <label className="form-label">Certifications</label>
                <input type="text" className="form-control" name="certifications" value={formData.certifications} onChange={handleChange} />
              </div>
            </div>

            <h5 className="mb-3">Status</h5>
            <div className="row g-3 mb-4">
              <div className="col-md-4">
                <label className="form-label">Current Status</label>
                <select className="form-select" name="status" value={formData.status} onChange={handleChange}>
                  <option value="Available">Available</option>
                  <option value="Active">Active</option>
                  <option value="Hired">Hired</option>
                  <option value="Rejected">Rejected</option>
                  <option value="Inactive">Inactive</option>
                </select>
              </div>
            </div>

            <div className="d-flex justify-content-end gap-2">
              <button type="button" className="btn btn-secondary" onClick={() => navigate('/hr/candidates')}>Cancel</button>
              <button type="submit" className="btn btn-primary">Save Candidate</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default CandidateForm;
