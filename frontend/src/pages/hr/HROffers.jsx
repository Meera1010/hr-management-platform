import React, { useState, useEffect } from 'react';
import { getOffers, updateOfferStatus, deleteOffer } from '../../services/api';
import OfferForm from './OfferForm';

const STATUS_COLORS = { Draft: 'secondary', Sent: 'primary', Accepted: 'success', Declined: 'danger', Expired: 'warning', Cancelled: 'dark' };

const HROffers = () => {
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [msg, setMsg] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editOffer, setEditOffer] = useState(null);
  const [filterStatus, setFilterStatus] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const data = await getOffers();
      setOffers(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleStatusChange = async (id, status) => {
    try {
      await updateOfferStatus(id, status);
      setMsg(`Offer status updated to ${status}.`);
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this offer?')) return;
    try {
      await deleteOffer(id);
      setMsg('Offer deleted.');
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    }
  };

  const filtered = filterStatus ? offers.filter(o => o.status === filterStatus) : offers;

  return (
    <div className="container-fluid py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div className="d-flex align-items-center">
          <i className="bi bi-file-earmark-check-fill text-success me-2 fs-3"></i>
          <div>
            <h2 className="mb-0 fw-bold">Offer Management</h2>
            <p className="text-muted mb-0 small">Create and manage job offers for selected candidates</p>
          </div>
        </div>
        <button className="btn btn-success" onClick={() => { setEditOffer(null); setShowForm(true); }}>
          <i className="bi bi-plus-circle me-2"></i>Create Offer
        </button>
      </div>

      {msg && <div className="alert alert-info alert-dismissible"><i className="bi bi-info-circle me-2"></i>{msg}<button className="btn-close" onClick={() => setMsg('')}></button></div>}
      {error && <div className="alert alert-danger">{error}</div>}

      {showForm && (
        <div className="mb-4">
          <OfferForm
            editOffer={editOffer}
            onSuccess={() => { setShowForm(false); setMsg('Offer saved successfully!'); load(); }}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}

      {/* Stats */}
      <div className="row g-3 mb-4">
        {['Draft', 'Sent', 'Accepted', 'Declined'].map(s => (
          <div key={s} className="col-md-3">
            <div className={`card border-0 shadow-sm text-center py-3 bg-${STATUS_COLORS[s]} bg-opacity-10`}>
              <div className={`fs-2 fw-bold text-${STATUS_COLORS[s]}`}>{offers.filter(o => o.status === s).length}</div>
              <div className="small fw-semibold text-muted">{s}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Filter */}
      <div className="card border-0 shadow-sm mb-4">
        <div className="card-body py-2">
          <div className="d-flex gap-2 flex-wrap">
            {['', 'Draft', 'Sent', 'Accepted', 'Declined', 'Expired', 'Cancelled'].map(s => (
              <button key={s} className={`btn btn-sm ${filterStatus === s ? 'btn-success' : 'btn-outline-secondary'}`} onClick={() => setFilterStatus(s)}>
                {s || 'All'}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Table */}
      {loading ? (
        <div className="text-center py-5"><div className="spinner-border text-success"></div></div>
      ) : (
        <div className="card border-0 shadow-sm">
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th className="ps-4">Offer Code</th>
                    <th>Candidate</th>
                    <th>Job Title</th>
                    <th>Salary</th>
                    <th>Start Date</th>
                    <th>Expires</th>
                    <th>Status</th>
                    <th className="text-center">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.length === 0 ? (
                    <tr><td colSpan="8" className="text-center py-4 text-muted">No offers found.</td></tr>
                  ) : filtered.map(o => (
                    <tr key={o.id}>
                      <td className="ps-4"><code>{o.offer_code}</code></td>
                      <td>
                        <div className="fw-semibold">{o.candidate_name}</div>
                        <small className="text-muted">{o.candidate_email}</small>
                      </td>
                      <td>{o.job_title}</td>
                      <td className="fw-semibold text-success">{o.offered_salary}</td>
                      <td className="small">{o.start_date}</td>
                      <td className="small text-muted">{o.expiration_date}</td>
                      <td><span className={`badge bg-${STATUS_COLORS[o.status] || 'secondary'}`}>{o.status}</span></td>
                      <td className="text-center">
                        <div className="dropdown">
                          <button className="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">Actions</button>
                          <ul className="dropdown-menu dropdown-menu-end">
                            {o.status === 'Draft' && (
                              <li><button className="dropdown-item" onClick={() => handleStatusChange(o.id, 'Sent')}><i className="bi bi-send me-2 text-primary"></i>Send to Candidate</button></li>
                            )}
                            {o.status === 'Sent' && (
                              <li><button className="dropdown-item" onClick={() => handleStatusChange(o.id, 'Expired')}><i className="bi bi-hourglass-bottom me-2 text-warning"></i>Mark Expired</button></li>
                            )}
                            <li><button className="dropdown-item" onClick={() => { setEditOffer(o); setShowForm(true); }}><i className="bi bi-pencil me-2"></i>Edit</button></li>
                            <li><button className="dropdown-item text-danger" onClick={() => handleDelete(o.id)}><i className="bi bi-trash me-2"></i>Delete</button></li>
                          </ul>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HROffers;
