import React, { useState, useEffect } from 'react';
import { getApplications } from '../../services/api';
import { createOffer, updateOffer } from '../../services/api';

const OfferForm = ({ editOffer, onSuccess, onCancel }) => {
  const [applications, setApplications] = useState([]);
  const [form, setForm] = useState({
    application_id: '',
    job_title: '',
    employment_type: 'Full Time',
    offered_salary: '',
    start_date: '',
    expiration_date: '',
    status: 'Draft',
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (editOffer) {
      setForm({
        application_id: editOffer.application_id || '',
        job_title: editOffer.job_title || '',
        employment_type: editOffer.employment_type || 'Full Time',
        offered_salary: editOffer.offered_salary || '',
        start_date: editOffer.start_date || '',
        expiration_date: editOffer.expiration_date || '',
        status: editOffer.status || 'Draft',
        notes: editOffer.notes || ''
      });
    }
    if (!editOffer) {
      getApplications().then(data => {
        const apps = Array.isArray(data) ? data : data.applications || [];
        setApplications(apps.filter(a => ['Shortlisted', 'Selected', 'Under Review'].includes(a.status)));
      }).catch(() => {});
    }
  }, [editOffer]);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      if (editOffer) {
        await updateOffer(editOffer.id, form);
      } else {
        await createOffer({ ...form, application_id: parseInt(form.application_id) });
      }
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.message || 'Failed to save offer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card border-0 shadow-sm">
      <div className="card-header bg-success text-white py-3">
        <h5 className="mb-0"><i className="bi bi-file-earmark-plus me-2"></i>{editOffer ? 'Edit Offer' : 'Create New Offer'}</h5>
      </div>
      <div className="card-body">
        {error && <div className="alert alert-danger"><i className="bi bi-exclamation-triangle me-2"></i>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="row g-3">
            {!editOffer && (
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
            <div className="col-md-8">
              <label className="form-label fw-semibold">Job Title <span className="text-danger">*</span></label>
              <input className="form-control" name="job_title" value={form.job_title} onChange={handleChange} placeholder="e.g. Senior Software Engineer" required />
            </div>
            <div className="col-md-4">
              <label className="form-label fw-semibold">Employment Type</label>
              <select className="form-select" name="employment_type" value={form.employment_type} onChange={handleChange}>
                {['Full Time', 'Part Time', 'Contract', 'Internship', 'Freelance'].map(t => <option key={t}>{t}</option>)}
              </select>
            </div>
            <div className="col-md-6">
              <label className="form-label fw-semibold">Offered Salary <span className="text-danger">*</span></label>
              <input className="form-control" name="offered_salary" value={form.offered_salary} onChange={handleChange} placeholder="e.g. $85,000 / year" required />
              <div className="form-text">Use fictional demo salary format</div>
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Start Date <span className="text-danger">*</span></label>
              <input type="date" className="form-control" name="start_date" value={form.start_date} onChange={handleChange} required />
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Expiration Date <span className="text-danger">*</span></label>
              <input type="date" className="form-control" name="expiration_date" value={form.expiration_date} onChange={handleChange} required />
            </div>
            {editOffer && (
              <div className="col-md-4">
                <label className="form-label fw-semibold">Status</label>
                <select className="form-select" name="status" value={form.status} onChange={handleChange}>
                  {['Draft', 'Sent', 'Accepted', 'Declined', 'Expired', 'Cancelled'].map(s => <option key={s}>{s}</option>)}
                </select>
              </div>
            )}
            <div className="col-12">
              <label className="form-label fw-semibold">Notes</label>
              <textarea className="form-control" name="notes" value={form.notes} onChange={handleChange} rows="3" placeholder="Additional offer details..."></textarea>
            </div>
          </div>
          <div className="d-flex gap-2 mt-4">
            <button type="submit" className="btn btn-success" disabled={loading}>
              {loading ? <><span className="spinner-border spinner-border-sm me-2"></span>Saving...</> : <><i className="bi bi-check-circle me-2"></i>{editOffer ? 'Update Offer' : 'Create Offer'}</>}
            </button>
            {onCancel && <button type="button" className="btn btn-outline-secondary" onClick={onCancel}>Cancel</button>}
          </div>
        </form>
      </div>
    </div>
  );
};

export default OfferForm;
