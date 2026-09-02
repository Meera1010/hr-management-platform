import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const JobProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Application Modal state
  const [showApplyModal, setShowApplyModal] = useState(false);
  const [coverLetter, setCoverLetter] = useState('');
  const [applying, setApplying] = useState(false);
  const [applySuccess, setApplySuccess] = useState('');
  const [applyError, setApplyError] = useState('');

  const canManage = ['Admin', 'HR', 'Recruiter'].includes(user?.role);
  const canApply = ['Candidate', 'Employee'].includes(user?.role);

  useEffect(() => {
    fetchJob();
  }, [id]);

  const fetchJob = async () => {
    try {
      setLoading(true);
      const res = await api.getJob(id);
      const jobData = res.data || res;
      setJob(jobData);
    } catch (err) {
      setError(err.message || 'Failed to load job details');
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async (e) => {
    e.preventDefault();
    setApplying(true);
    setApplyError('');
    setApplySuccess('');
    try {
      await api.createApplication({ job_id: parseInt(id), cover_letter: coverLetter });
      setApplySuccess('Your application was submitted successfully!');
      setTimeout(() => {
        setShowApplyModal(false);
        setApplySuccess('');
        setCoverLetter('');
      }, 2500);
    } catch (err) {
      setApplyError(err.message || 'Failed to submit application');
    } finally {
      setApplying(false);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Open': return 'bg-success';
      case 'Closed': return 'bg-secondary';
      case 'Draft': return 'bg-warning text-dark';
      case 'Archived': return 'bg-dark';
      default: return 'bg-primary';
    }
  };

  if (loading) {
    return (
      <div className="container py-5 text-center">
        <div className="spinner-border text-primary" role="status"></div>
        <p className="mt-3 text-muted">Loading job details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-5 text-center">
        <div className="alert alert-danger">{error}</div>
        <Link to="/jobs" className="btn btn-primary">Back to Jobs</Link>
      </div>
    );
  }

  if (!job) return null;

  return (
    <div className="container py-4">
      <div className="mb-4">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <button className="btn btn-outline-secondary btn-sm" onClick={() => navigate(-1)}>
            &larr; Back
          </button>
          
          <div className="d-flex gap-2">
            {canManage && (
              <>
                <button
                  className="btn btn-outline-info btn-sm"
                  onClick={() => navigate(`/recruiter/jobs/${job.id}/matches`)}
                >
                  🎯 AI Matches
                </button>
                <button
                  className="btn btn-outline-primary btn-sm"
                  onClick={() => navigate(`/jobs/${job.id}/edit`)}
                >
                  ✏️ Edit Job
                </button>
              </>
            )}
            {canApply && job.status === 'Open' && (
              <button
                className="btn btn-primary btn-sm px-3"
                onClick={() => setShowApplyModal(true)}
              >
                🚀 Apply Now
              </button>
            )}
          </div>
        </div>

        <div className="d-flex justify-content-between align-items-start">
          <div>
            <h2>{job.title}</h2>
            <h5 className="text-muted mb-3">{job.job_code} • {job.department_name}</h5>
          </div>
          <span className={`badge ${getStatusBadge(job.status)} fs-6 p-2`}>
            {job.status}
          </span>
        </div>
      </div>

      <div className="row">
        <div className="col-md-8">
          <div className="card shadow-sm border-0 mb-4">
            <div className="card-body p-4">
              <h5 className="card-title fw-bold">Job Description</h5>
              <p style={{ whiteSpace: 'pre-wrap' }}>{job.description}</p>
              
              {job.responsibilities && (
                <>
                  <h5 className="card-title fw-bold mt-4">Key Responsibilities</h5>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{job.responsibilities}</p>
                </>
              )}
              
              {job.required_skills && (
                <>
                  <h5 className="card-title fw-bold mt-4">Required Skills</h5>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{job.required_skills}</p>
                </>
              )}
              
              {job.preferred_skills && (
                <>
                  <h5 className="card-title fw-bold mt-4">Preferred Skills</h5>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{job.preferred_skills}</p>
                </>
              )}
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow-sm border-0 mb-4">
            <div className="card-header bg-dark text-white">
              <h5 className="mb-0">Key Information</h5>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <strong>📍 Location:</strong>
                <div>{job.location || 'Remote / Flexible'}</div>
              </div>
              <div className="mb-3">
                <strong>💼 Employment Type:</strong>
                <div>{job.employment_type || 'Full Time'}</div>
              </div>
              <div className="mb-3">
                <strong>⏳ Experience Required:</strong>
                <div>{job.experience_required ? `${job.experience_required} years` : 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>🎓 Education:</strong>
                <div>{job.education_required || 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>💰 Salary Range:</strong>
                <div>{job.salary_range || 'Competitive'}</div>
              </div>
              {job.application_deadline && (
                <div className="mb-3">
                  <strong>📅 Application Deadline:</strong>
                  <div>{new Date(job.application_deadline).toLocaleDateString()}</div>
                </div>
              )}
              {canApply && job.status === 'Open' && (
                <button
                  className="btn btn-primary w-100 mt-3"
                  onClick={() => setShowApplyModal(true)}
                >
                  Apply for this Position
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Apply Modal */}
      {showApplyModal && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }} tabIndex="-1">
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Apply for {job.title}</h5>
                <button type="button" className="btn-close" onClick={() => setShowApplyModal(false)}></button>
              </div>
              <form onSubmit={handleApply}>
                <div className="modal-body">
                  {applySuccess && <div className="alert alert-success">{applySuccess}</div>}
                  {applyError && <div className="alert alert-danger">{applyError}</div>}

                  {!applySuccess && (
                    <div className="mb-3">
                      <label className="form-label fw-semibold">Cover Letter / Note</label>
                      <textarea
                        className="form-control"
                        rows="5"
                        placeholder="Highlight your key qualifications, relevant experience, and why you're a great fit for this role..."
                        value={coverLetter}
                        onChange={(e) => setCoverLetter(e.target.value)}
                        required
                      />
                    </div>
                  )}
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowApplyModal(false)}>
                    Close
                  </button>
                  {!applySuccess && (
                    <button type="submit" className="btn btn-primary" disabled={applying}>
                      {applying ? 'Submitting...' : 'Submit Application'}
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JobProfile;
