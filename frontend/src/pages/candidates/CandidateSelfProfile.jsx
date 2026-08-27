import React, { useState, useEffect } from 'react';
import api from '../../services/api';

function CandidateSelfProfile() {
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  
  const [formData, setFormData] = useState({});

  useEffect(() => {
    fetchMyProfile();
  }, []);

  const fetchMyProfile = async () => {
    try {
      setLoading(true);
      const res = await api.getMyCandidateProfile();
      setCandidate(res.data.candidate);
      setFormData(res.data.candidate);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load your profile');
    } finally {
      setLoading(false);
    }
  };

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
    setSuccessMsg(null);
    try {
      const res = await api.updateMyCandidateProfile(formData);
      setCandidate(res.data.candidate);
      setSuccessMsg('Profile updated successfully!');
      setIsEditing(false);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update profile');
    }
  };

  if (loading) return <div className="text-center mt-5"><div className="spinner-border text-primary" /></div>;
  
  if (error && !candidate) return (
    <div className="container mt-5">
      <div className="alert alert-danger">{error}</div>
      <p>If you recently registered, your profile might not be fully set up yet. Please contact support.</p>
    </div>
  );

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>My Profile</h2>
        {!isEditing && (
          <button className="btn btn-primary" onClick={() => setIsEditing(true)}>Edit Profile</button>
        )}
      </div>

      {successMsg && <div className="alert alert-success">{successMsg}</div>}
      {error && isEditing && <div className="alert alert-danger">{error}</div>}

      <div className="card shadow-sm mb-4">
        <div className="card-body">
          {isEditing ? (
            <form onSubmit={handleSubmit}>
              <div className="row g-3 mb-4">
                <div className="col-md-6">
                  <label className="form-label">First Name</label>
                  <input type="text" className="form-control" name="first_name" value={formData.first_name || ''} onChange={handleChange} required />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Last Name</label>
                  <input type="text" className="form-control" name="last_name" value={formData.last_name || ''} onChange={handleChange} required />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Phone</label>
                  <input type="text" className="form-control" name="phone" value={formData.phone || ''} onChange={handleChange} />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Location</label>
                  <input type="text" className="form-control" name="location" value={formData.location || ''} onChange={handleChange} />
                </div>
                
                <div className="col-md-4">
                  <label className="form-label">Current Role</label>
                  <input type="text" className="form-control" name="current_role" value={formData.current_role || ''} onChange={handleChange} />
                </div>
                <div className="col-md-4">
                  <label className="form-label">Experience (Years)</label>
                  <input type="number" className="form-control" name="experience_years" value={formData.experience_years || 0} onChange={handleChange} min="0" required />
                </div>
                <div className="col-md-4">
                  <label className="form-label">Education</label>
                  <input type="text" className="form-control" name="education" value={formData.education || ''} onChange={handleChange} />
                </div>
                <div className="col-md-12">
                  <label className="form-label">Skills (comma separated)</label>
                  <textarea className="form-control" name="skills" value={formData.skills || ''} onChange={handleChange} rows="2"></textarea>
                </div>
                <div className="col-md-12">
                  <label className="form-label">Certifications</label>
                  <input type="text" className="form-control" name="certifications" value={formData.certifications || ''} onChange={handleChange} />
                </div>
              </div>
              <div className="d-flex justify-content-end gap-2">
                <button type="button" className="btn btn-secondary" onClick={() => { setIsEditing(false); setFormData(candidate); }}>Cancel</button>
                <button type="submit" className="btn btn-success">Save Changes</button>
              </div>
            </form>
          ) : (
            <div className="row">
              <div className="col-md-6 mb-3">
                <h6 className="text-muted">Full Name</h6>
                <p className="fs-5">{candidate.first_name} {candidate.last_name}</p>
              </div>
              <div className="col-md-6 mb-3">
                <h6 className="text-muted">Email</h6>
                <p className="fs-5">{candidate.email} <span className="badge bg-secondary ms-2" title="Contact HR to change email">Read-only</span></p>
              </div>
              <div className="col-md-6 mb-3">
                <h6 className="text-muted">Phone</h6>
                <p className="fs-5">{candidate.phone || 'Not provided'}</p>
              </div>
              <div className="col-md-6 mb-3">
                <h6 className="text-muted">Location</h6>
                <p className="fs-5">{candidate.location || 'Not provided'}</p>
              </div>
              <div className="col-md-6 mb-3">
                <h6 className="text-muted">Current Role</h6>
                <p className="fs-5">{candidate.current_role || 'Not provided'}</p>
              </div>
              <div className="col-md-6 mb-3">
                <h6 className="text-muted">Experience</h6>
                <p className="fs-5">{candidate.experience_years} Years</p>
              </div>
              <div className="col-md-6 mb-3">
                <h6 className="text-muted">Education</h6>
                <p className="fs-5">{candidate.education || 'Not provided'}</p>
              </div>
              <div className="col-md-6 mb-3">
                <h6 className="text-muted">Skills</h6>
                <p className="fs-5">
                  {candidate.skills ? candidate.skills.split(',').map((s, i) => (
                    <span key={i} className="badge bg-light text-dark border me-1">{s.trim()}</span>
                  )) : 'Not provided'}
                </p>
              </div>
              <div className="col-md-12 mb-3">
                <h6 className="text-muted">Certifications</h6>
                <p className="fs-5">{candidate.certifications || 'Not provided'}</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      <div className="card shadow-sm border-info">
        <div className="card-body">
          <h5 className="card-title text-info">Recruitment Status</h5>
          <p className="card-text mb-0">Your current status in our system is: <strong>{candidate.status}</strong></p>
        </div>
      </div>
    </div>
  );
}

export default CandidateSelfProfile;
