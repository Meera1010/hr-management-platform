import React, { useState, useEffect } from 'react';
import { getResumes, uploadResume, deleteResume, downloadResume, extractSkills } from '../../services/api';

const CandidateResumes = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState(null);

  // Modal for Viewing Extracted Text
  const [viewResumeText, setViewResumeText] = useState(null);

  const fetchResumes = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getResumes();
      setResumes(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch resumes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, []);

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setUploading(true);
    setMessage(null);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await uploadResume(formData);
      setMessage('Resume uploaded and processed successfully!');
      setSelectedFile(null);
      fetchResumes();
    } catch (err) {
      setError(err.message || 'Failed to upload resume');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this resume?')) return;
    try {
      await deleteResume(id);
      setMessage('Resume deleted successfully.');
      fetchResumes();
    } catch (err) {
      setError(err.message || 'Failed to delete resume');
    }
  };

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

  const formatBytes = (bytes) => {
    if (!bytes) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>My Resumes</h2>
        <span className="badge bg-info text-dark">AI-Assisted Skill Extraction Enabled</span>
      </div>

      {message && <div className="alert alert-success alert-dismissible fade show">{message}</div>}
      {error && <div className="alert alert-danger alert-dismissible fade show">{error}</div>}

      {/* Upload Card */}
      <div className="card mb-4 shadow-sm">
        <div className="card-header bg-primary text-white">
          <h5 className="mb-0">Upload New Resume</h5>
        </div>
        <div className="card-body">
          <form onSubmit={handleUpload} className="row g-3 align-items-center">
            <div className="col-md-8">
              <input
                type="file"
                className="form-control"
                accept=".pdf,.txt,.docx"
                onChange={handleFileChange}
                required
              />
              <small className="text-muted">Allowed formats: PDF, TXT, DOCX (Max 5 MB)</small>
            </div>
            <div className="col-md-4">
              <button type="submit" className="btn btn-success w-100" disabled={uploading || !selectedFile}>
                {uploading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Uploading & Parsing...
                  </>
                ) : (
                  'Upload Resume'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Resumes List Table */}
      {loading ? (
        <div className="text-center py-4">
          <div className="spinner-border text-primary" role="status"></div>
          <p className="mt-2">Loading resumes...</p>
        </div>
      ) : resumes.length === 0 ? (
        <div className="alert alert-info">You haven't uploaded any resumes yet. Use the upload box above to add your demo resume.</div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover table-striped align-middle border">
            <thead className="table-dark">
              <tr>
                <th>Code</th>
                <th>Filename</th>
                <th>Type</th>
                <th>Size</th>
                <th>Upload Date</th>
                <th>Status</th>
                <th>Extracted Skills</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {resumes.map((r) => (
                <tr key={r.id}>
                  <td><strong>{r.resume_code}</strong></td>
                  <td>{r.filename}</td>
                  <td><span className="badge bg-secondary">{r.file_type}</span></td>
                  <td>{formatBytes(r.file_size)}</td>
                  <td>{new Date(r.uploaded_at).toLocaleDateString()}</td>
                  <td>
                    <span className={`badge ${r.status === 'Parsed' ? 'bg-success' : 'bg-warning text-dark'}`}>
                      {r.status}
                    </span>
                  </td>
                  <td>
                    {r.extracted_skills && r.extracted_skills.length > 0 ? (
                      r.extracted_skills.map((skill, sIdx) => (
                        <span key={sIdx} className="badge bg-light text-dark border me-1 mb-1">
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="text-muted small">No skills extracted</span>
                    )}
                  </td>
                  <td className="text-end">
                    <div className="btn-group btn-group-sm" role="group">
                      {r.extracted_text && (
                        <button
                          className="btn btn-outline-info"
                          title="View Extracted Text"
                          onClick={() => setViewResumeText(r)}
                        >
                          View
                        </button>
                      )}
                      <button
                        className="btn btn-outline-primary"
                        title="Download"
                        onClick={() => handleDownload(r.id, r.filename)}
                      >
                        Download
                      </button>
                      <button
                        className="btn btn-outline-success"
                        title="Extract Skills"
                        onClick={() => handleExtractSkills(r.id)}
                      >
                        Extract Skills
                      </button>
                      <button
                        className="btn btn-outline-danger"
                        title="Delete"
                        onClick={() => handleDelete(r.id)}
                      >
                        Delete
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
                <h5 className="modal-title">Extracted Text - {viewResumeText.resume_code}</h5>
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

export default CandidateResumes;
