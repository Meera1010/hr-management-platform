import React, { useState, useEffect } from 'react';
import { getLeaves, approveLeave, rejectLeave } from '../../services/api';

const STATUS_COLORS = { Pending: 'warning', Approved: 'success', Rejected: 'danger', Cancelled: 'secondary' };

const HRLeaves = () => {
  const [leaves, setLeaves] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ status: '', employee_id: '' });
  const [msg, setMsg] = useState('');
  const [commentModal, setCommentModal] = useState(null); // {id, action}
  const [comment, setComment] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.status) params.set('status', filters.status);
      if (filters.employee_id) params.set('employee_id', filters.employee_id);
      const data = await getLeaves(params.toString());
      setLeaves(Array.isArray(data) ? data : []);
    } catch {
      setLeaves([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleAction = async () => {
    if (!commentModal) return;
    try {
      if (commentModal.action === 'approve') {
        await approveLeave(commentModal.id, comment || 'Approved.');
        setMsg('Leave approved successfully.');
      } else {
        await rejectLeave(commentModal.id, comment || 'Rejected.');
        setMsg('Leave rejected.');
      }
      setCommentModal(null);
      setComment('');
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    }
  };

  const pending = leaves.filter(l => l.status === 'Pending').length;
  const approved = leaves.filter(l => l.status === 'Approved').length;

  return (
    <div className="container py-4">
      <div className="d-flex align-items-center mb-4">
        <i className="bi bi-calendar2-week-fill text-warning me-2 fs-3"></i>
        <div>
          <h2 className="mb-0 fw-bold">Leave Management</h2>
          <p className="text-muted mb-0 small">Review and manage employee leave requests</p>
        </div>
      </div>

      {/* Stats */}
      <div className="row g-3 mb-4">
        {[
          { label: 'Total Requests', val: leaves.length, color: 'primary', icon: 'bi-list-ul' },
          { label: 'Pending Review', val: pending, color: 'warning', icon: 'bi-hourglass-split' },
          { label: 'Approved', val: approved, color: 'success', icon: 'bi-check-circle' },
        ].map((s, i) => (
          <div key={i} className="col-md-4">
            <div className={`card border-0 shadow-sm border-start border-${s.color} border-4`}>
              <div className="card-body py-3 d-flex align-items-center">
                <i className={`bi ${s.icon} text-${s.color} fs-3 me-3`}></i>
                <div><div className="small text-muted">{s.label}</div><div className="fw-bold fs-4">{s.val}</div></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {msg && <div className="alert alert-info alert-dismissible">{msg}<button className="btn-close" onClick={() => setMsg('')}></button></div>}

      {/* Filters */}
      <div className="card border-0 shadow-sm mb-4">
        <div className="card-body py-3">
          <div className="row g-2 align-items-end">
            <div className="col-md-3">
              <label className="form-label small">Status</label>
              <select className="form-select form-select-sm" value={filters.status} onChange={e => setFilters({...filters, status: e.target.value})}>
                <option value="">All Statuses</option>
                {['Pending','Approved','Rejected','Cancelled'].map(s => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div className="col-md-3">
              <label className="form-label small">Employee ID</label>
              <input className="form-control form-control-sm" value={filters.employee_id} onChange={e => setFilters({...filters, employee_id: e.target.value})} />
            </div>
            <div className="col-md-3 d-flex gap-2">
              <button className="btn btn-primary btn-sm" onClick={load}>Filter</button>
              <button className="btn btn-outline-secondary btn-sm" onClick={() => { setFilters({ status: '', employee_id: '' }); setTimeout(load, 100); }}>Clear</button>
            </div>
          </div>
        </div>
      </div>

      {/* Approve/Reject Comment Modal */}
      {commentModal && (
        <div className="modal show d-block" style={{ background: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className={`modal-header bg-${commentModal.action === 'approve' ? 'success' : 'danger'} text-white`}>
                <h5 className="modal-title">{commentModal.action === 'approve' ? 'Approve Leave' : 'Reject Leave'}</h5>
                <button className="btn-close btn-close-white" onClick={() => setCommentModal(null)}></button>
              </div>
              <div className="modal-body">
                <label className="form-label">Manager Comment (optional)</label>
                <textarea className="form-control" rows={3} value={comment} onChange={e => setComment(e.target.value)} placeholder="Add a comment..." />
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={() => setCommentModal(null)}>Cancel</button>
                <button className={`btn btn-${commentModal.action === 'approve' ? 'success' : 'danger'}`} onClick={handleAction}>
                  {commentModal.action === 'approve' ? 'Approve' : 'Reject'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Leave Table */}
      <div className="card border-0 shadow-sm">
        <div className="card-body p-0">
          {loading ? <div className="text-center py-4"><div className="spinner-border text-warning"></div></div> :
          leaves.length === 0 ? (
            <div className="text-center py-5"><i className="bi bi-calendar-x text-muted fs-1"></i><p className="text-muted mt-2">No leave requests found.</p></div>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead className="table-light">
                  <tr><th>Code</th><th>Employee</th><th>Type</th><th>Start</th><th>End</th><th>Days</th><th>Status</th><th>Reason</th><th>Actions</th></tr>
                </thead>
                <tbody>
                  {leaves.map(l => (
                    <tr key={l.id}>
                      <td><span className="badge bg-light text-dark border">{l.leave_code}</span></td>
                      <td><div className="fw-semibold">{l.employee_name}</div><small className="text-muted">{l.department_name}</small></td>
                      <td>{l.leave_type}</td>
                      <td>{l.start_date}</td>
                      <td>{l.end_date}</td>
                      <td><span className="badge bg-light text-dark">{l.days_count}d</span></td>
                      <td><span className={`badge bg-${STATUS_COLORS[l.status]} ${l.status === 'Pending' ? 'text-dark' : ''}`}>{l.status}</span></td>
                      <td><span className="text-muted small">{l.reason?.substring(0, 35)}{l.reason?.length > 35 ? '…' : ''}</span></td>
                      <td>
                        {l.status === 'Pending' && (
                          <div className="d-flex gap-1">
                            <button className="btn btn-success btn-sm" onClick={() => setCommentModal({id: l.id, action: 'approve'})}>
                              <i className="bi bi-check2"></i>
                            </button>
                            <button className="btn btn-danger btn-sm" onClick={() => setCommentModal({id: l.id, action: 'reject'})}>
                              <i className="bi bi-x-lg"></i>
                            </button>
                          </div>
                        )}
                        {l.manager_comment && l.status !== 'Pending' && (
                          <span className="text-muted small" title={l.manager_comment}><i className="bi bi-chat-text me-1"></i>{l.manager_comment?.substring(0, 20)}</span>
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

export default HRLeaves;
