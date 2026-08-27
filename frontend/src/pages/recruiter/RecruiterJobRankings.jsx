import React, { useState, useEffect } from 'react';
import { getCandidateRankings, shortlistApplication } from '../../services/api';
import { getJobs } from '../../services/api';

const RecruiterJobRankings = () => {
  const [jobs, setJobs] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState('');
  const [rankings, setRankings] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingJobs, setLoadingJobs] = useState(true);
  const [error, setError] = useState('');
  const [actionMsg, setActionMsg] = useState('');

  useEffect(() => {
    getJobs().then(data => {
      const openJobs = (Array.isArray(data) ? data : data.jobs || []).filter(j => j.status === 'Open');
      setJobs(openJobs);
    }).catch(() => setError('Failed to load jobs.')).finally(() => setLoadingJobs(false));
  }, []);

  const loadRankings = async () => {
    if (!selectedJobId) return;
    setLoading(true);
    setError('');
    setActionMsg('');
    try {
      const data = await getCandidateRankings(selectedJobId);
      setRankings(data);
    } catch (err) {
      setError(err.message || 'Failed to load rankings');
    } finally {
      setLoading(false);
    }
  };

  const handleShortlist = async (appId, candidateName) => {
    if (!appId) { setActionMsg('Candidate has not applied for this job yet.'); return; }
    if (!window.confirm(`Shortlist ${candidateName}?`)) return;
    try {
      await shortlistApplication(appId);
      setActionMsg(`${candidateName} shortlisted successfully.`);
      loadRankings();
    } catch (err) {
      setActionMsg('Error: ' + err.message);
    }
  };

  const scoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 50) return 'warning';
    return 'danger';
  };

  return (
    <div className="container-fluid py-4">
      <div className="d-flex align-items-center mb-4">
        <i className="bi bi-bar-chart-fill text-primary me-2 fs-3"></i>
        <div>
          <h2 className="mb-0 fw-bold">AI Candidate Rankings</h2>
          <p className="text-muted mb-0 small">Transparent scoring: Skills 60% · Experience 25% · Education 15%</p>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="alert alert-info border-0 mb-4" style={{background:'linear-gradient(135deg,#dbeafe,#e0f2fe)'}}>
        <i className="bi bi-info-circle-fill me-2"></i>
        <strong>Decision Support Only.</strong> Rankings are a guide. Final hiring decisions must be made by qualified HR professionals considering all relevant factors. Rankings are based solely on job-related criteria.
      </div>

      {/* Job Selection */}
      <div className="card border-0 shadow-sm mb-4">
        <div className="card-body">
          <div className="row g-3 align-items-end">
            <div className="col-md-8">
              <label className="form-label fw-semibold">Select a Job to Rank Candidates</label>
              <select className="form-select form-select-lg" value={selectedJobId} onChange={e => setSelectedJobId(e.target.value)} disabled={loadingJobs}>
                <option value="">-- Choose a Job --</option>
                {jobs.map(j => (
                  <option key={j.id} value={j.id}>{j.job_code} – {j.title}</option>
                ))}
              </select>
            </div>
            <div className="col-md-4">
              <button className="btn btn-primary btn-lg w-100" onClick={loadRankings} disabled={!selectedJobId || loading}>
                {loading ? <><span className="spinner-border spinner-border-sm me-2"></span>Ranking...</> : <><i className="bi bi-cpu-fill me-2"></i>Run AI Ranking</>}
              </button>
            </div>
          </div>
        </div>
      </div>

      {error && <div className="alert alert-danger"><i className="bi bi-exclamation-triangle me-2"></i>{error}</div>}
      {actionMsg && <div className="alert alert-success"><i className="bi bi-check-circle me-2"></i>{actionMsg}</div>}

      {/* Rankings Table */}
      {rankings && (
        <>
          <div className="card border-0 shadow-sm mb-3">
            <div className="card-header bg-white d-flex justify-content-between align-items-center py-3">
              <div>
                <h5 className="mb-0 fw-bold">{rankings.job_title}</h5>
                <small className="text-muted">{rankings.job_code} · {rankings.candidates.length} candidates ranked</small>
              </div>
              <span className="badge bg-primary fs-6">{rankings.candidates.length} Candidates</span>
            </div>
            <div className="card-body p-0">
              <div className="table-responsive">
                <table className="table table-hover align-middle mb-0">
                  <thead className="table-light">
                    <tr>
                      <th className="ps-4">#</th>
                      <th>Candidate</th>
                      <th>AI Score</th>
                      <th>Skills</th>
                      <th>Experience</th>
                      <th>Education</th>
                      <th>Status</th>
                      <th>Matched Skills</th>
                      <th className="text-center">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rankings.candidates.map((c, idx) => (
                      <tr key={c.candidate_id}>
                        <td className="ps-4">
                          <span className={`badge ${idx < 3 ? 'bg-warning text-dark' : 'bg-light text-dark'} rounded-pill`}>
                            {idx + 1}
                          </span>
                        </td>
                        <td>
                          <div className="fw-semibold">{c.candidate_name}</div>
                          <small className="text-muted">{c.email}</small>
                        </td>
                        <td>
                          <div className="d-flex align-items-center gap-2">
                            <div className="progress flex-grow-1" style={{height:'8px', minWidth:'80px'}}>
                              <div className={`progress-bar bg-${scoreColor(c.score)}`} style={{width:`${c.score}%`}}></div>
                            </div>
                            <span className={`badge bg-${scoreColor(c.score)} fw-bold`}>{c.score}%</span>
                          </div>
                          <small className="text-muted fst-italic">{c.explanation}</small>
                        </td>
                        <td><span className={`badge bg-${scoreColor(c.skill_score)}`}>{c.skill_score}%</span></td>
                        <td>
                          <span className={`badge bg-${scoreColor(c.experience_score)}`}>{c.experience_score}%</span>
                          <div><small className="text-muted">{c.experience_years} yrs</small></div>
                        </td>
                        <td>
                          <span className={`badge bg-${scoreColor(c.education_score)}`}>{c.education_score}%</span>
                          <div><small className="text-muted">{c.education}</small></div>
                        </td>
                        <td>
                          <span className={`badge ${c.application_status === 'Shortlisted' ? 'bg-success' : c.application_status === 'Not Applied' ? 'bg-secondary' : 'bg-info text-dark'}`}>
                            {c.application_status}
                          </span>
                        </td>
                        <td>
                          {c.matched_skills && c.matched_skills.length > 0
                            ? c.matched_skills.slice(0, 3).map((s, i) => <span key={i} className="badge bg-light text-dark me-1 mb-1">{s}</span>)
                            : <span className="text-muted small">None</span>
                          }
                          {c.matched_skills && c.matched_skills.length > 3 && <span className="badge bg-light text-muted">+{c.matched_skills.length - 3}</span>}
                        </td>
                        <td className="text-center">
                          {c.application_status !== 'Shortlisted' && c.application_status !== 'Not Applied' && (
                            <button className="btn btn-sm btn-outline-success" onClick={() => handleShortlist(c.application_id, c.candidate_name)}>
                              <i className="bi bi-person-check me-1"></i>Shortlist
                            </button>
                          )}
                          {c.application_status === 'Shortlisted' && <span className="text-success"><i className="bi bi-check-circle-fill me-1"></i>Shortlisted</span>}
                          {c.application_status === 'Not Applied' && <span className="text-muted small">Not Applied</span>}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default RecruiterJobRankings;
