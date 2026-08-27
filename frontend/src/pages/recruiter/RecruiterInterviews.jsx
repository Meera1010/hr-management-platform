import React, { useState, useEffect } from 'react';
import { getInterviews, updateInterviewStatus, deleteInterview } from '../../services/api';

const STATUS_COLORS = { Scheduled: 'primary', Completed: 'success', Cancelled: 'danger', Rescheduled: 'warning' };

const RecruiterInterviews = () => {
  const [interviews, setInterviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [msg, setMsg] = useState('');
  const [filterStatus, setFilterStatus] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const data = await getInterviews();
      setInterviews(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleStatusChange = async (id, status) => {
    try {
      await updateInterviewStatus(id, status);
      setMsg(`Interview marked as ${status}.`);
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this interview?')) return;
    try {
      await deleteInterview(id);
      setMsg('Interview deleted.');
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    }
  };

  const filtered = filterStatus ? interviews.filter(i => i.status === filterStatus) : interviews;

  return (
    <div className="container-fluid py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div className="d-flex align-items-center">
          <i className="bi bi-camera-video-fill text-primary me-2 fs-3"></i>
          <div>
            <h2 className="mb-0 fw-bold">Interview Management</h2>
            <p className="text-muted mb-0 small">Schedule, track, and manage all candidate interviews</p>
          </div>
        </div>
        <a href="/recruiter/interviews/schedule" className="btn btn-primary">
          <i className="bi bi-plus-circle me-2"></i>Schedule Interview
        </a>
      </div>

      {msg && <div className="alert alert-info alert-dismissible"><i className="bi bi-info-circle me-2"></i>{msg}<button className="btn-close" onClick={() => setMsg('')}></button></div>}
      {error && <div className="alert alert-danger">{error}</div>}

      {/* Stats Row */}
      <div className="row g-3 mb-4">
        {['Scheduled', 'Completed', 'Rescheduled', 'Cancelled'].map(s => (
          <div key={s} className="col-md-3">
            <div className={`card border-0 shadow-sm text-center py-3 bg-${STATUS_COLORS[s]} bg-opacity-10`}>
              <div className={`fs-2 fw-bold text-${STATUS_COLORS[s]}`}>{interviews.filter(i => i.status === s).length}</div>
              <div className="small fw-semibold text-muted">{s}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Filter Bar */}
      <div className="card border-0 shadow-sm mb-4">
        <div className="card-body py-2">
          <div className="d-flex gap-2 flex-wrap">
            {['', 'Scheduled', 'Completed', 'Rescheduled', 'Cancelled'].map(s => (
              <button key={s} className={`btn btn-sm ${filterStatus === s ? 'btn-primary' : 'btn-outline-secondary'}`} onClick={() => setFilterStatus(s)}>
                {s || 'All'} {s && <span className="badge bg-white text-dark ms-1">{interviews.filter(i => i.status === s).length}</span>}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Table */}
      {loading ? (
        <div className="text-center py-5"><div className="spinner-border text-primary"></div></div>
      ) : (
        <div className="card border-0 shadow-sm">
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th className="ps-4">Code</th>
                    <th>Candidate</th>
                    <th>Job</th>
                    <th>Interviewer</th>
                    <th>Type</th>
                    <th>Date & Time</th>
                    <th>Status</th>
                    <th>Feedback</th>
                    <th className="text-center">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.length === 0 ? (
                    <tr><td colSpan="9" className="text-center py-4 text-muted">No interviews found.</td></tr>
                  ) : filtered.map(i => (
                    <tr key={i.id}>
                      <td className="ps-4"><code>{i.interview_code}</code></td>
                      <td>
                        <div className="fw-semibold">{i.candidate_name}</div>
                        <small className="text-muted">{i.candidate_email}</small>
                      </td>
                      <td className="small">{i.job_title}</td>
                      <td className="small">{i.interviewer_name}</td>
                      <td><span className="badge bg-info text-dark">{i.interview_type}</span></td>
                      <td className="small">
                        <div>{i.scheduled_date}</div>
                        <div className="text-muted">{i.scheduled_time} ({i.duration_minutes} min)</div>
                      </td>
                      <td><span className={`badge bg-${STATUS_COLORS[i.status] || 'secondary'}`}>{i.status}</span></td>
                      <td>
                        {i.feedback
                          ? <span className="badge bg-success"><i className="bi bi-check-circle me-1"></i>Submitted</span>
                          : <span className="badge bg-light text-muted">Pending</span>
                        }
                      </td>
                      <td className="text-center">
                        <div className="dropdown">
                          <button className="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">Actions</button>
                          <ul className="dropdown-menu dropdown-menu-end">
                            {i.status === 'Scheduled' && <>
                              <li><button className="dropdown-item" onClick={() => handleStatusChange(i.id, 'Completed')}><i className="bi bi-check-circle me-2 text-success"></i>Mark Completed</button></li>
                              <li><button className="dropdown-item" onClick={() => handleStatusChange(i.id, 'Cancelled')}><i className="bi bi-x-circle me-2 text-danger"></i>Cancel</button></li>
                            </>}
                            {i.status === 'Completed' && !i.feedback && (
                              <li><a className="dropdown-item" href={`/recruiter/interviews/${i.id}/feedback`}><i className="bi bi-star me-2 text-warning"></i>Submit Feedback</a></li>
                            )}
                            <li><button className="dropdown-item text-danger" onClick={() => handleDelete(i.id)}><i className="bi bi-trash me-2"></i>Delete</button></li>
                          </ul>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecruiterInterviews;
