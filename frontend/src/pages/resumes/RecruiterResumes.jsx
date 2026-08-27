import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getResumes, downloadResume } from '../../services/api';

const RecruiterResumes = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [viewResumeText, setViewResumeText] = useState(null);

  const fetchResumes = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getResumes();
      setResumes(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch candidate resumes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, []);

  const handleDownload = async (id, filename) => {
    try {
      const blob = await downloadResume(id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      alert('Failed to download resume file.');
    }
  };

  const filteredResumes = resumes.filter((r) => {
    const candidateName = r.candidate_name ? r.candidate_name.toLowerCase() : '';
    const code = r.resume_code ? r.resume_code.toLowerCase() : '';
    const term = searchTerm.toLowerCase();
    return candidateName.includes(term) || code.includes(term);
  });

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Recruiter Resume Directory</h2>
        <span className="badge bg-primary">Candidate Pool: {resumes.length}</span>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card mb-4 shadow-sm">
        <div className="card-body">
          <input
            type="text"
            className="form-control"
            placeholder="Search by candidate name or resume code..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <div className="text-center py-4">
          <div className="spinner-border text-primary" role="status"></div>
          <p className="mt-2">Loading candidate resumes...</p>
        </div>
      ) : filteredResumes.length === 0 ? (
        <div className="alert alert-info">No candidate resumes found.</div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover table-striped align-middle border">
            <thead className="table-dark">
              <tr>
                <th>Candidate</th>
                <th>Resume Code</th>
                <th>Upload Date</th>
                <th>Match Status</th>
                <th>Parsed Skills</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredResumes.map((r) => (
                <tr key={r.id}>
                  <td>
                    <strong>{r.candidate_name || `Candidate #${r.candidate_id}`}</strong>
                  </td>
                  <td><code>{r.resume_code}</code></td>
                  <td>{new Date(r.uploaded_at).toLocaleDateString()}</td>
                  <td>
                    <span className={`badge ${r.status === 'Parsed' ? 'bg-success' : 'bg-secondary'}`}>
                      {r.status}
                    </span>
                  </td>
                  <td>
                    {r.extracted_skills && r.extracted_skills.length > 0 ? (
                      r.extracted_skills.map((skill, sIdx) => (
                        <span key={sIdx} className="badge bg-info text-dark me-1 mb-1">
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="text-muted small">No skills parsed</span>
                    )}
                  </td>
                  <td className="text-end">
                    <div className="btn-group btn-group-sm" role="group">
                      <Link
                        to={`/hr/candidates/${r.candidate_id}`}
                        className="btn btn-outline-primary"
                      >
                        View Candidate
                      </Link>
                      {r.extracted_text && (
                        <button
                          className="btn btn-outline-info"
                          onClick={() => setViewResumeText(r)}
                        >
                          View Resume
                        </button>
                      )}
                      <button
                        className="btn btn-outline-secondary"
                        onClick={() => handleDownload(r.id, r.filename)}
                      >
                        Download
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Extracted Text Modal */}
      {viewResumeText && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-lg modal-dialog-scrollable">
            <div className="modal-content">
              <div className="modal-header bg-dark text-white">
                <h5 className="modal-title">Candidate Resume Text - {viewResumeText.candidate_name} ({viewResumeText.resume_code})</h5>
                <button type="button" className="btn-close btn-close-white" onClick={() => setViewResumeText(null)}></button>
              </div>
              <div className="modal-body bg-light">
                <pre style={{ whitespace: 'pre-wrap', fontFamily: 'monospace' }}>
                  {viewResumeText.extracted_text}
                </pre>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setViewResumeText(null)}>
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecruiterResumes;
