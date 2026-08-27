import React, { useState, useEffect } from 'react';
import { getResumes, downloadResume, extractSkills } from '../../services/api';

const HRResumes = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [viewResumeText, setViewResumeText] = useState(null);
  const [message, setMessage] = useState(null);

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

  const handleExtractSkills = async (id) => {
    try {
      setMessage('Extracting skills from resume...');
      const res = await extractSkills(id);
      setMessage(`Skills extracted successfully! Found: ${res.skills.join(', ')}`);
      fetchResumes();
    } catch (err) {
      setError(err.message || 'Failed to extract skills');
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
        <h2>HR Resume Management</h2>
        <span className="badge bg-secondary">Total Resumes: {resumes.length}</span>
      </div>

      {message && <div className="alert alert-success alert-dismissible fade show">{message}</div>}
      {error && <div className="alert alert-danger alert-dismissible fade show">{error}</div>}

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
          <p className="mt-2">Loading resumes...</p>
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
                <th>Type</th>
                <th>Upload Date</th>
                <th>Status</th>
                <th>Extracted Skills</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredResumes.map((r) => (
                <tr key={r.id}>
                  <td><strong>{r.candidate_name || `Candidate #${r.candidate_id}`}</strong></td>
                  <td><code>{r.resume_code}</code></td>
                  <td><span className="badge bg-info text-dark">{r.file_type}</span></td>
                  <td>{new Date(r.uploaded_at).toLocaleDateString()}</td>
                  <td>
                    <span className={`badge ${r.status === 'Parsed' ? 'bg-success' : 'bg-warning text-dark'}`}>
                      {r.status}
                    </span>
                  </td>
                  <td>
                    {r.extracted_skills && r.extracted_skills.length > 0 ? (
                      r.extracted_skills.map((skill, sIdx) => (
                        <span key={sIdx} className="badge bg-primary me-1 mb-1">
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="text-muted small">No skills parsed</span>
                    )}
                  </td>
                  <td className="text-end">
                    <div className="btn-group btn-group-sm" role="group">
                      {r.extracted_text && (
                        <button
                          className="btn btn-outline-info"
                          onClick={() => setViewResumeText(r)}
                        >
                          View Text
                        </button>
                      )}
                      <button
                        className="btn btn-outline-primary"
                        onClick={() => handleDownload(r.id, r.filename)}
                      >
                        Download
                      </button>
                      <button
                        className="btn btn-outline-success"
                        onClick={() => handleExtractSkills(r.id)}
                      >
                        Extract Skills
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
                <h5 className="modal-title">{viewResumeText.candidate_name} - Extracted Text ({viewResumeText.resume_code})</h5>
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

export default HRResumes;
