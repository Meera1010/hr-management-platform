import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getCandidateMatches } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const CandidateMatches = () => {
  const { currentUser } = useAuth();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMatches = async () => {
      if (!currentUser || !currentUser.candidate_id) {
        // Fallback fetch: try getting candidate profile ID if missing
        setLoading(false);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const data = await getCandidateMatches(currentUser.candidate_id);
        setMatches(data);
      } catch (err) {
        setError(err.message || 'Failed to fetch job matches');
      } finally {
        setLoading(false);
      }
    };

    fetchMatches();
  }, [currentUser]);

  const getMatchBadgeClass = (pct) => {
    if (pct >= 80) return 'bg-success';
    if (pct >= 50) return 'bg-primary';
    if (pct >= 30) return 'bg-warning text-dark';
    return 'bg-secondary';
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>AI-Assisted Job Matches</h2>
        <span className="badge bg-info text-dark">Rule-Based Skill Scoring</span>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="alert alert-light border mb-4">
        <strong>How it works:</strong> Our AI-assisted matching engine compares your parsed resume skills and profile skills against open job requirements to calculate your match score.
      </div>

      {loading ? (
        <div className="text-center py-4">
          <div className="spinner-border text-primary" role="status"></div>
          <p className="mt-2">Calculating job matches...</p>
        </div>
      ) : matches.length === 0 ? (
        <div className="alert alert-info">
          No open job matches found. Make sure you have uploaded a resume in <Link to="/candidate/resumes">My Resumes</Link> to extract your skills!
        </div>
      ) : (
        <div className="row row-cols-1 row-cols-md-2 g-4">
          {matches.map((job) => (
            <div className="col" key={job.job_id}>
              <div className="card h-100 shadow-sm border-0">
                <div className="card-header bg-white d-flex justify-content-between align-items-center py-3">
                  <h5 className="card-title mb-0 text-primary">{job.job_title}</h5>
                  <span className={`badge ${getMatchBadgeClass(job.match_percentage)} fs-6`}>
                    {job.match_percentage}% Match
                  </span>
                </div>
                <div className="card-body">
                  <p className="card-text text-muted mb-2">
                    <strong>Department:</strong> {job.department} | <strong>Location:</strong> {job.location}
                  </p>

                  {/* Progress Bar */}
                  <div className="progress mb-3" style={{ height: '8px' }}>
                    <div
                      className={`progress-bar ${getMatchBadgeClass(job.match_percentage)}`}
                      role="progressbar"
                      style={{ width: `${job.match_percentage}%` }}
                      aria-valuenow={job.match_percentage}
                      aria-valuemin="0"
                      aria-valuemax="100"
                    ></div>
                  </div>

                  <div className="mb-3">
                    <strong>Required Skills:</strong>
                    <div className="mt-1">
                      {job.required_skills ? (
                        job.required_skills.split(',').map((skill, sIdx) => {
                          const sTrim = skill.trim();
                          const isMatched = job.matched_skills.includes(sTrim.toLowerCase());
                          return (
                            <span
                              key={sIdx}
                              className={`badge me-1 mb-1 ${isMatched ? 'bg-success' : 'bg-outline-secondary border text-muted'}`}
                            >
                              {sTrim} {isMatched ? '✓' : ''}
                            </span>
                          );
                        })
                      ) : (
                        <span className="text-muted small">No specific skills listed</span>
                      )}
                    </div>
                  </div>

                  {job.missing_skills.length > 0 && (
                    <div className="mb-2">
                      <small className="text-muted">Skills to acquire: </small>
                      {job.missing_skills.map((ms, mIdx) => (
                        <span key={mIdx} className="badge bg-light text-danger border me-1">
                          {ms}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <div className="card-footer bg-white border-top-0 d-flex justify-content-between align-items-center">
                  <small className="text-muted">Code: {job.job_code}</small>
                  <Link to={`/jobs/${job.job_id}`} className="btn btn-outline-primary btn-sm">
                    View Job
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CandidateMatches;
