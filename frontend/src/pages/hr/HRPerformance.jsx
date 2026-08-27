import React, { useState, useEffect } from 'react';
import { getPerformanceReviews, createPerformanceReview, updatePerformanceReview, deletePerformanceReview } from '../../services/api';
import PerformanceForm from './PerformanceForm';

const SCORE_COLOR = (s) => s >= 4.5 ? 'success' : s >= 3.5 ? 'primary' : s >= 2.5 ? 'warning' : 'danger';

const HRPerformance = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [mode, setMode] = useState('list'); // 'list' | 'create' | 'edit'
  const [editItem, setEditItem] = useState(null);
  const [msg, setMsg] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const data = await getPerformanceReviews();
      setReviews(Array.isArray(data) ? data : []);
    } catch { setReviews([]); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async (form) => {
    try {
      await createPerformanceReview(form);
      setMsg('Performance review created.');
      setMode('list');
      load();
    } catch (err) { setMsg('Error: ' + err.message); }
  };

  const handleUpdate = async (form) => {
    try {
      await updatePerformanceReview(editItem.id, form);
      setMsg('Performance review updated.');
      setMode('list');
      setEditItem(null);
      load();
    } catch (err) { setMsg('Error: ' + err.message); }
  };

  const handleDelete = async (id, code) => {
    if (!window.confirm(`Delete review ${code}?`)) return;
    try {
      await deletePerformanceReview(id);
      setMsg('Review deleted.');
      load();
    } catch (err) { setMsg('Error: ' + err.message); }
  };

  const completedCount = reviews.filter(r => r.status === 'Completed').length;
  const avgScore = reviews.filter(r => r.status === 'Completed').length > 0
    ? (reviews.filter(r => r.status === 'Completed').reduce((s, r) => s + r.overall_score, 0) / completedCount).toFixed(2)
    : '—';

  return (
    <div className="container py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div className="d-flex align-items-center">
          <i className="bi bi-graph-up-arrow text-success me-2 fs-3"></i>
          <div>
            <h2 className="mb-0 fw-bold">Performance Management</h2>
            <p className="text-muted mb-0 small">Create and manage employee performance reviews</p>
          </div>
        </div>
        {mode === 'list' && (
          <button className="btn btn-success" onClick={() => setMode('create')}>
            <i className="bi bi-plus-lg me-2"></i>New Review
          </button>
        )}
      </div>

      {/* Stats */}
      <div className="row g-3 mb-4">
        {[
          { label: 'Total Reviews', val: reviews.length, color: 'primary', icon: 'bi-clipboard-data' },
          { label: 'Completed', val: completedCount, color: 'success', icon: 'bi-check2-square' },
          { label: 'Avg Score', val: avgScore, color: 'info', icon: 'bi-star-half' },
        ].map((s, i) => (
          <div key={i} className="col-md-4">
            <div className={`card border-0 shadow-sm border-start border-${s.color} border-4`}>
              <div className="card-body py-3 d-flex align-items-center">
                <i className={`bi ${s.icon} text-${s.color} fs-3 me-3`}></i>
                <div><div className="small text-muted">{s.label}</div><div className="fw-bold fs-5">{s.val}</div></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {msg && <div className="alert alert-info alert-dismissible">{msg}<button className="btn-close" onClick={() => setMsg('')}></button></div>}

      {/* Create/Edit Form */}
      {(mode === 'create' || mode === 'edit') && (
        <div className="card border-0 shadow-sm mb-4">
          <div className="card-header">
            <h5 className="mb-0"><i className="bi bi-clipboard-plus me-2"></i>{mode === 'create' ? 'New Performance Review' : 'Edit Review'}</h5>
          </div>
          <div className="card-body">
            <PerformanceForm
              initial={mode === 'edit' ? editItem : undefined}
              onSave={mode === 'create' ? handleCreate : handleUpdate}
              onCancel={() => { setMode('list'); setEditItem(null); }}
            />
          </div>
        </div>
      )}

      {/* Reviews Table */}
      {mode === 'list' && (
        <div className="card border-0 shadow-sm">
          <div className="card-body p-0">
            {loading ? <div className="text-center py-4"><div className="spinner-border text-success"></div></div> :
            reviews.length === 0 ? (
              <div className="text-center py-5"><i className="bi bi-clipboard-x text-muted fs-1"></i><p className="text-muted mt-2">No reviews found.</p></div>
            ) : (
              <div className="table-responsive">
                <table className="table table-hover mb-0">
                  <thead className="table-light">
                    <tr><th>Code</th><th>Employee</th><th>Period</th><th>Prod</th><th>Quality</th><th>Teamwork</th><th>Goals</th><th>Overall</th><th>Status</th><th>Actions</th></tr>
                  </thead>
                  <tbody>
                    {reviews.map(r => (
                      <tr key={r.id}>
                        <td><span className="badge bg-light text-dark border">{r.review_code}</span></td>
                        <td><div className="fw-semibold">{r.employee_name}</div><small className="text-muted">{r.department_name}</small></td>
                        <td>{r.review_period}</td>
                        <td><span className={`badge bg-${SCORE_COLOR(r.productivity_score)}`}>{r.productivity_score}</span></td>
                        <td><span className={`badge bg-${SCORE_COLOR(r.quality_score)}`}>{r.quality_score}</span></td>
                        <td><span className={`badge bg-${SCORE_COLOR(r.teamwork_score)}`}>{r.teamwork_score}</span></td>
                        <td><span className={`badge bg-${SCORE_COLOR(r.goal_score)}`}>{r.goal_score}</span></td>
                        <td>
                          <div className={`fw-bold text-${SCORE_COLOR(r.overall_score)}`}>{r.overall_score}</div>
                          <div className="progress" style={{ height: 4 }}>
                            <div className={`progress-bar bg-${SCORE_COLOR(r.overall_score)}`} style={{ width: `${(r.overall_score/5)*100}%` }}></div>
                          </div>
                        </td>
                        <td><span className={`badge bg-${r.status === 'Completed' ? 'success' : 'secondary'}`}>{r.status}</span></td>
                        <td>
                          <div className="d-flex gap-1">
                            <button className="btn btn-outline-primary btn-sm" onClick={() => { setEditItem(r); setMode('edit'); }} title="Edit"><i className="bi bi-pencil"></i></button>
                            <button className="btn btn-outline-danger btn-sm" onClick={() => handleDelete(r.id, r.review_code)} title="Delete"><i className="bi bi-trash"></i></button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default HRPerformance;
