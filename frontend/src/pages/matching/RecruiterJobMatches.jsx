import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getJobCandidateMatchesList, getJob } from '../../services/api';

const RecruiterJobMatches = () => {
  const { jobId } = useParams();
  const [jobInfo, setJobInfo] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const jobData = await getJob(jobId);
        setJobInfo(jobData);

        const matchData = await getJobCandidateMatchesList(jobId);
        setCandidates(matchData.candidates || []);
      } catch (err) {
        setError(err.message || 'Failed to load candidate match rankings');
      } finally {
        setLoading(false);
      }
    };

    if (jobId) {
      fetchData();
    }
  }, [jobId]);

  const getBadgeClass = (pct) => {
    if (pct >= 80) return 'bg-success';
    if (pct >= 50) return 'bg-primary';
    if (pct >= 30) return 'bg-warning text-dark';
    return 'bg-secondary';
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h2>Candidate Skill Match Rankings</h2>
          {jobInfo && (
            <p className="lead text-muted mb-0">
              Job: <strong>{jobInfo.title}</strong> ({jobInfo.job_code}) — Required Skills: <code>{jobInfo.required_skills || 'None'}</code>
            </p>
          )}
        </div>
        <Link to="/jobs" className="btn btn-outline-secondary">
          &larr; Back to Jobs
        </Link>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {loading ? (
        <div className="text-center py-4">
          <div className="spinner-border text-primary" role="status"></div>
          <p className="mt-2">Ranking candidates by skill match...</p>
        </div>
      ) : candidates.length === 0 ? (
        <div className="alert alert-info">No candidates found for matching.</div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover table-striped align-middle border">
            <thead className="table-dark">
              <tr>
                <th>Rank</th>
                <th>Candidate</th>
                <th>Experience</th>
                <th>Education</th>
                <th>Matched Skills</th>
                <th>Missing Skills</th>
                <th>Match %</th>
                <th>Application Status</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {candidates.map((c, idx) => (
                <tr key={c.candidate_id}>
                  <td><strong>#{idx + 1}</strong></td>
                  <td>
                    <strong>{c.candidate_name}</strong>
                    <br />
                    <small className="text-muted">{c.candidate_code}</small>
                  </td>
                  <td>{c.experience_years} years</td>
                  <td>{c.education}</td>
                  <td>
                    {c.matched_skills && c.matched_skills.length > 0 ? (
                      c.matched_skills.map((s, sIdx) => (
                        <span key={sIdx} className="badge bg-success me-1 mb-1">
                          {s}
                        </span>
                      ))
                    ) : (
                      <span className="text-muted small">None</span>
                    )}
                  </td>
                  <td>
                    {c.missing_skills && c.missing_skills.length > 0 ? (
                      c.missing_skills.map((s, mIdx) => (
                        <span key={mIdx} className="badge bg-light text-danger border me-1 mb-1">
                          {s}
                        </span>
                      ))
                    ) : (
                      <span className="badge bg-light text-success border">Full Match</span>
                    )}
                  </td>
                  <td>
                    <span className={`badge ${getBadgeClass(c.match_percentage)} fs-6`}>
                      {c.match_percentage}%
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${c.application_status === 'Not Applied' ? 'bg-secondary' : 'bg-info text-dark'}`}>
                      {c.application_status}
                    </span>
                  </td>
                  <td className="text-end">
                    <Link
                      to={`/hr/candidates/${c.candidate_id}`}
                      className="btn btn-outline-primary btn-sm"
                    >
                      View Candidate
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default RecruiterJobMatches;
