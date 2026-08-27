import React, { useState, useEffect } from 'react';
import { getApplications } from '../../services/api';
import { createInterview } from '../../services/api';

const InterviewForm = ({ preselectedAppId, onSuccess, onCancel }) => {
  const [applications, setApplications] = useState([]);
  const [form, setForm] = useState({
    application_id: preselectedAppId || '',
    interviewer_name: '',
    interview_type: 'Technical',
    scheduled_date: '',
    scheduled_time: '',
    duration_minutes: 45,
    meeting_link: 'https://example.com/demo-interview',
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!preselectedAppId) {
      getApplications().then(data => {
        const apps = Array.isArray(data) ? data : data.applications || [];
        setApplications(apps.filter(a => ['Shortlisted', 'Under Review'].includes(a.status)));
      }).catch(() => {});
    }
  }, [preselectedAppId]);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await createInterview({
        ...form,
        application_id: parseInt(form.application_id),
        duration_minutes: parseInt(form.duration_minutes)
      });
      if (onSuccess) onSuccess(result);
      else window.location.href = '/recruiter/interviews';
    } catch (err) {
      setError(err.message || 'Failed to schedule interview');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card border-0 shadow-sm">
      <div className="card-header bg-primary text-white py-3">
        <h5 className="mb-0"><i className="bi bi-calendar-plus me-2"></i>Schedule Interview</h5>
      </div>
      <div className="card-body">
        {error && <div className="alert alert-danger"><i className="bi bi-exclamation-triangle me-2"></i>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="row g-3">
            {!preselectedAppId && (
              <div className="col-12">
                <label className="form-label fw-semibold">Application <span className="text-danger">*</span></label>
                <select className="form-select" name="application_id" value={form.application_id} onChange={handleChange} required>
                  <option value="">-- Select Application --</option>
                  {applications.map(a => (
                    <option key={a.id} value={a.id}>{a.application_code} – {a.candidate_name} → {a.job_title}</option>
                  ))}
                </select>
              </div>
            )}
            <div className="col-md-6">
              <label className="form-label fw-semibold">Interviewer Name <span className="text-danger">*</span></label>
              <input className="form-control" name="interviewer_name" value={form.interviewer_name} onChange={handleChange} placeholder="e.g. Sarah TechLead" required />
            </div>
            <div className="col-md-6">
              <label className="form-label fw-semibold">Interview Type</label>
              <select className="form-select" name="interview_type" value={form.interview_type} onChange={handleChange}>
                {['Technical', 'HR', 'Managerial', 'General', 'Panel'].map(t => <option key={t}>{t}</option>)}
              </select>
            </div>
            <div className="col-md-4">
              <label className="form-label fw-semibold">Date <span className="text-danger">*</span></label>
              <input type="date" className="form-control" name="scheduled_date" value={form.scheduled_date} onChange={handleChange} required />
            </div>
            <div className="col-md-4">
              <label className="form-label fw-semibold">Time <span className="text-danger">*</span></label>
              <input type="time" className="form-control" name="scheduled_time" value={form.scheduled_time} onChange={handleChange} required />
            </div>
            <div className="col-md-4">
              <label className="form-label fw-semibold">Duration (minutes)</label>
              <input type="number" className="form-control" name="duration_minutes" value={form.duration_minutes} onChange={handleChange} min="15" max="180" />
            </div>
            <div className="col-12">
              <label className="form-label fw-semibold">Meeting Link</label>
              <input className="form-control" name="meeting_link" value={form.meeting_link} onChange={handleChange} placeholder="https://example.com/meeting" />
            </div>
            <div className="col-12">
              <label className="form-label fw-semibold">Internal Notes</label>
              <textarea className="form-control" name="notes" value={form.notes} onChange={handleChange} rows="3" placeholder="Internal notes about the interview..."></textarea>
            </div>
          </div>
          <div className="d-flex gap-2 mt-4">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <><span className="spinner-border spinner-border-sm me-2"></span>Scheduling...</> : <><i className="bi bi-calendar-check me-2"></i>Schedule Interview</>}
            </button>
            {onCancel && <button type="button" className="btn btn-outline-secondary" onClick={onCancel}>Cancel</button>}
            {!onCancel && <a href="/recruiter/interviews" className="btn btn-outline-secondary">Cancel</a>}
          </div>
        </form>
      </div>
    </div>
  );
};

const InterviewFormPage = () => (
  <div className="container py-4">
    <div className="mb-3">
      <a href="/recruiter/interviews" className="btn btn-outline-secondary btn-sm"><i className="bi bi-arrow-left me-2"></i>Back to Interviews</a>
    </div>
    <InterviewForm />
  </div>
);

export default InterviewFormPage;
export { InterviewForm };
