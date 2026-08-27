import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../services/api';

const JobProfile = () => {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchJob();
  }, [id]);

  const fetchJob = async () => {
    try {
      setLoading(true);
      const data = await api.getJob(id);
      setJob(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
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
        <div className="spinner-border" role="status"></div>
        <p className="mt-3">Loading job details...</p>
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
        <Link to="/jobs" className="btn btn-outline-secondary mb-3">
          &larr; Back to Jobs
        </Link>
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
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Job Description</h5>
              <p style={{ whiteSpace: 'pre-wrap' }}>{job.description}</p>
              
              {job.responsibilities && (
                <>
                  <h5 className="card-title mt-4">Responsibilities</h5>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{job.responsibilities}</p>
                </>
              )}
              
              {job.required_skills && (
                <>
                  <h5 className="card-title mt-4">Required Skills</h5>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{job.required_skills}</p>
                </>
              )}
              
              {job.preferred_skills && (
                <>
                  <h5 className="card-title mt-4">Preferred Skills</h5>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{job.preferred_skills}</p>
                </>
              )}
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card mb-4">
            <div className="card-header bg-light">
              <h5 className="mb-0">Key Details</h5>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <strong>Location:</strong>
                <div>{job.location || 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>Employment Type:</strong>
                <div>{job.employment_type || 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>Experience Required:</strong>
                <div>{job.experience_required || 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>Education Required:</strong>
                <div>{job.education_required || 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>Salary Range:</strong>
                <div>{job.salary_range || 'Not specified'}</div>
              </div>
              {job.application_deadline && (
                <div className="mb-3">
                  <strong>Application Deadline:</strong>
                  <div>{new Date(job.application_deadline).toLocaleDateString()}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobProfile;
