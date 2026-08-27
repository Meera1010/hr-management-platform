import React, { useState, useEffect } from 'react';
import { getLeaves, createLeave, cancelLeave } from '../../services/api';

const STATUS_COLORS = { Pending: 'warning', Approved: 'success', Rejected: 'danger', Cancelled: 'secondary' };
const LEAVE_TYPES = ['Casual', 'Annual', 'Unpaid', 'Personal'];

const EmployeeLeaves = () => {
  const [leaves, setLeaves] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [msg, setMsg] = useState('');
  const [error, setError] = useState('');
  const [form, setForm] = useState({ leave_type: 'Casual', start_date: '', end_date: '', reason: '' });
  const [submitting, setSubmitting] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const data = await getLeaves();
      setLeaves(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.start_date || !form.end_date) { setMsg('Please fill all required fields.'); return; }
    if (form.end_date < form.start_date) { setMsg('End date cannot be before start date.'); return; }
    setSubmitting(true);
    try {
      await createLeave(form);
      setMsg('Leave request submitted successfully!');
      setShowForm(false);
      setForm({ leave_type: 'Casual', start_date: '', end_date: '', reason: '' });
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancel = async (id, code) => {
    if (!window.confirm(`Cancel leave ${code}?`)) return;
    try {
      await cancelLeave(id);
      setMsg('Leave cancelled.');
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    }
  };

  if (loading) return <div className="text-center py-5"><div className="spinner-border text-warning"></div></div>;

  const pending = leaves.filter(l => l.status === 'Pending').length;
  const approved = leaves.filter(l => l.status === 'Approved').length;

  return (
    <div className="container py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div className="d-flex align-items-center">
          <i className="bi bi-calendar2-week-fill text-warning me-2 fs-3"></i>
          <div>
            <h2 className="mb-0 fw-bold">My Leave Requests</h2>
            <p className="text-muted mb-0 small">Manage your time-off requests</p>
          </div>
        </div>
        <button className="btn btn-warning text-white" onClick={() => setShowForm(!showForm)}>
          <i className={`bi bi-${showForm ? 'x-lg' : 'plus-lg'} me-2`}></i>
          {showForm ? 'Cancel' : 'Request Leave'}
        </button>
      </div>

      {/* Stats */}
      <div className="row g-3 mb-4">
        {[{ label: 'Total Requests', val: leaves.length, icon: 'bi-list-ul', color: 'primary' },
          { label: 'Pending', val: pending, icon: 'bi-hourglass-split', color: 'warning' },
          { label: 'Approved', val: approved, icon: 'bi-check-circle-fill', color: 'success' }].map((s, i) => (
          <div key={i} className="col-md-4">
            <div className={`card border-0 shadow-sm border-start border-${s.color} border-4`}>
              <div className="card-body py-3">
                <div className="d-flex align-items-center">
                  <i className={`bi ${s.icon} text-${s.color} fs-3 me-3`}></i>
                  <div>
                    <div className="small text-muted">{s.label}</div>
                    <div className="fw-bold fs-4">{s.val}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {msg && <div className="alert alert-info alert-dismissible"><i className="bi bi-info-circle me-2"></i>{msg}<button className="btn-close" onClick={() => setMsg('')}></button></div>}

      {/* Request Form */}
      {showForm && (
        <div className="card border-0 shadow-sm mb-4">
          <div className="card-header bg-warning bg-opacity-10">
            <h5 className="mb-0 fw-semibold"><i className="bi bi-calendar-plus me-2"></i>New Leave Request</h5>
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="row g-3">
                <div className="col-md-3">
                  <label className="form-label fw-semibold">Leave Type *</label>
                  <select className="form-select" value={form.leave_type} onChange={e => setForm({...form, leave_type: e.target.value})}>
                    {LEAVE_TYPES.map(t => <option key={t}>{t}</option>)}
                  </select>
                </div>
                <div className="col-md-3">
                  <label className="form-label fw-semibold">Start Date *</label>
                  <input type="date" className="form-control" value={form.start_date} onChange={e => setForm({...form, start_date: e.target.value})} required />
                </div>
                <div className="col-md-3">
                  <label className="form-label fw-semibold">End Date *</label>
                  <input type="date" className="form-control" value={form.end_date} onChange={e => setForm({...form, end_date: e.target.value})} required />
                </div>
                <div className="col-md-12">
                  <label className="form-label fw-semibold">Reason *</label>
                  <textarea className="form-control" rows={3} value={form.reason} onChange={e => setForm({...form, reason: e.target.value})} required placeholder="Please provide a reason for your leave request..." />
                </div>
                <div className="col-12">
                  <button type="submit" className="btn btn-warning text-white" disabled={submitting}>
                    <i className="bi bi-send me-2"></i>{submitting ? 'Submitting...' : 'Submit Request'}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Leave List */}
      <div className="card border-0 shadow-sm">
        <div className="card-header bg-white border-bottom py-3">
          <h5 className="mb-0 fw-semibold"><i className="bi bi-table me-2 text-warning"></i>Leave History</h5>
        </div>
        <div className="card-body p-0">
          {leaves.length === 0 ? (
            <div className="text-center py-5">
              <i className="bi bi-calendar-x text-muted" style={{ fontSize: '3rem' }}></i>
              <p className="text-muted mt-3">No leave requests found.</p>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Code</th>
                    <th>Type</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Days</th>
                    <th>Status</th>
                    <th>Reason</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {leaves.map(l => (
                    <tr key={l.id}>
                      <td><span className="badge bg-light text-dark border">{l.leave_code}</span></td>
                      <td>{l.leave_type}</td>
                      <td>{l.start_date}</td>
                      <td>{l.end_date}</td>
                      <td><span className="badge bg-light text-dark">{l.days_count}d</span></td>
                      <td><span className={`badge bg-${STATUS_COLORS[l.status] || 'secondary'} ${l.status === 'Pending' ? 'text-dark' : ''}`}>{l.status}</span></td>
                      <td><span className="text-muted small" title={l.reason}>{l.reason?.length > 40 ? l.reason.substring(0, 40) + '…' : l.reason}</span></td>
                      <td>
                        {l.status === 'Pending' && (
                          <button className="btn btn-outline-danger btn-sm" onClick={() => handleCancel(l.id, l.leave_code)}>
                            <i className="bi bi-x-circle me-1"></i>Cancel
                          </button>
                        )}
                        {l.manager_comment && (
                          <span className="text-muted small ms-2" title={l.manager_comment}>
                            <i className="bi bi-chat-quote"></i>
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EmployeeLeaves;
