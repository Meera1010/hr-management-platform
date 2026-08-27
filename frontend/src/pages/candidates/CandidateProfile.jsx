import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../services/api';

function CandidateProfile() {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCandidate = async () => {
      try {
        const res = await api.getCandidate(id);
        setCandidate(res.data.candidate);
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to load candidate');
      } finally {
        setLoading(false);
      }
    };
    fetchCandidate();
  }, [id]);

  if (loading) return <div className="text-center mt-5"><div className="spinner-border text-primary" /></div>;
  if (error) return <div className="container mt-5 alert alert-danger">{error}</div>;
  if (!candidate) return <div className="container mt-5 alert alert-warning">Candidate not found</div>;

  const getStatusBadge = (status) => {
    const colors = {
      'Available': 'bg-primary',
      'Hired': 'bg-success',
      'Rejected': 'bg-danger',
      'Active': 'bg-info',
      'Inactive': 'bg-secondary'
    };
    return <span className={`badge ${colors[status] || 'bg-secondary'}`}>{status}</span>;
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Candidate Profile</h2>
        <div>
          <Link to={`/hr/candidates/${candidate.id}/edit`} className="btn btn-primary me-2">Edit Candidate</Link>
          <Link to="/hr/candidates" className="btn btn-secondary">Back to List</Link>
        </div>
      </div>

      <div className="row">
        <div className="col-md-4">
          <div className="card shadow-sm mb-4">
            <div className="card-body text-center">
              <div className="display-1 text-primary mb-3">
                <i className="bi bi-person-circle"></i>
              </div>
              <h4 className="card-title">{candidate.first_name} {candidate.last_name}</h4>
              <p className="text-muted mb-2">{candidate.current_role || 'No role specified'}</p>
              <div className="mb-3">
                {getStatusBadge(candidate.status)}
              </div>
              <ul className="list-group list-group-flush text-start mt-4">
                <li className="list-group-item"><strong>Code:</strong> {candidate.candidate_code}</li>
                <li className="list-group-item"><strong>Email:</strong> {candidate.email}</li>
                <li className="list-group-item"><strong>Phone:</strong> {candidate.phone || '-'}</li>
                <li className="list-group-item"><strong>Location:</strong> {candidate.location || '-'}</li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="col-md-8">
          <div className="card shadow-sm mb-4">
            <div className="card-header bg-white">
              <h5 className="mb-0">Professional Summary</h5>
            </div>
            <div className="card-body">
              <div className="row mb-3">
                <div className="col-sm-3 text-muted">Experience</div>
                <div className="col-sm-9">{candidate.experience_years} Years</div>
              </div>
              <div className="row mb-3">
                <div className="col-sm-3 text-muted">Education</div>
                <div className="col-sm-9">{candidate.education || '-'}</div>
              </div>
              <div className="row mb-3">
                <div className="col-sm-3 text-muted">Skills</div>
                <div className="col-sm-9">
                  {candidate.skills ? (
                    candidate.skills.split(',').map((skill, index) => (
                      <span key={index} className="badge bg-light text-dark me-1 border">{skill.trim()}</span>
                    ))
                  ) : '-'}
                </div>
              </div>
              <div className="row mb-3">
                <div className="col-sm-3 text-muted">Certifications</div>
                <div className="col-sm-9">{candidate.certifications || '-'}</div>
              </div>
              <div className="row mb-3">
                <div className="col-sm-3 text-muted">Added On</div>
                <div className="col-sm-9">{new Date(candidate.created_at).toLocaleDateString()}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CandidateProfile;
