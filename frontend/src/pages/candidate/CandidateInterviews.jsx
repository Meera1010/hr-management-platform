import React, { useState, useEffect } from 'react';
import { getInterviews } from '../../services/api';

const STATUS_COLORS = { Scheduled: 'primary', Completed: 'success', Cancelled: 'danger', Rescheduled: 'warning' };

const CandidateInterviews = () => {
  const [interviews, setInterviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getInterviews().then(data => {
      setInterviews(Array.isArray(data) ? data : []);
    }).catch(err => setError(err.message)).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-5"><div className="spinner-border text-primary"></div></div>;

  return (
    <div className="container py-4">
      <div className="d-flex align-items-center mb-4">
        <i className="bi bi-camera-video-fill text-primary me-2 fs-3"></i>
        <div>
          <h2 className="mb-0 fw-bold">My Interviews</h2>
          <p className="text-muted mb-0 small">View your upcoming and past interviews</p>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {interviews.length === 0 ? (
        <div className="text-center py-5">
          <i className="bi bi-camera-video text-muted" style={{fontSize:'4rem'}}></i>
          <p className="text-muted mt-3">No interviews scheduled yet.</p>
        </div>
      ) : (
        <div className="row g-4">
          {interviews.map(i => (
            <div key={i.id} className="col-md-6">
              <div className="card border-0 shadow-sm h-100">
                <div className={`card-header bg-${STATUS_COLORS[i.status] || 'secondary'} bg-opacity-15 border-0 py-3`}>
                  <div className="d-flex justify-content-between align-items-center">
                    <div>
                      <div className="fw-bold">{i.interview_type} Interview</div>
                      <code className="text-muted small">{i.interview_code}</code>
                    </div>
                    <span className={`badge bg-${STATUS_COLORS[i.status] || 'secondary'}`}>{i.status}</span>
                  </div>
                </div>
                <div className="card-body">
                  <div className="mb-3">
                    <div className="fw-semibold text-primary mb-1">{i.job_title}</div>
                    <div className="small text-muted">{i.job_code}</div>
                  </div>
                  <ul className="list-unstyled small mb-0">
                    <li className="mb-1"><i className="bi bi-calendar3 me-2 text-primary"></i><strong>Date:</strong> {i.scheduled_date}</li>
                    <li className="mb-1"><i className="bi bi-clock me-2 text-primary"></i><strong>Time:</strong> {i.scheduled_time}</li>
                    <li className="mb-1"><i className="bi bi-hourglass-split me-2 text-primary"></i><strong>Duration:</strong> {i.duration_minutes} minutes</li>
                    <li className="mb-1"><i className="bi bi-person-badge me-2 text-primary"></i><strong>Interviewer:</strong> {i.interviewer_name}</li>
                    {i.meeting_link && (
                      <li><i className="bi bi-link-45deg me-2 text-primary"></i>
                        <a href={i.meeting_link} target="_blank" rel="noreferrer" className="text-primary">Join Meeting</a>
                      </li>
                    )}
                  </ul>
                </div>
                {i.status === 'Scheduled' && (
                  <div className="card-footer border-0 bg-transparent">
                    <div className="alert alert-info py-2 mb-0 small"><i className="bi bi-bell me-2"></i>Please be ready 5 minutes before your scheduled time.</div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CandidateInterviews;
