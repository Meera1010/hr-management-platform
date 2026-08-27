import React, { useState, useEffect } from 'react';
import { getOffers, acceptOffer, declineOffer } from '../../services/api';

const STATUS_COLORS = { Draft: 'secondary', Sent: 'primary', Accepted: 'success', Declined: 'danger', Expired: 'warning', Cancelled: 'dark' };

const CandidateOffers = () => {
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [msg, setMsg] = useState('');

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

  const handleAccept = async (id, jobTitle) => {
    if (!window.confirm(`Accept the offer for "${jobTitle}"?`)) return;
    try {
      await acceptOffer(id);
      setMsg(`Offer for "${jobTitle}" accepted! Congratulations!`);
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    }
  };

  const handleDecline = async (id, jobTitle) => {
    if (!window.confirm(`Decline the offer for "${jobTitle}"?`)) return;
    try {
      await declineOffer(id);
      setMsg(`Offer for "${jobTitle}" declined.`);
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    }
  };

  if (loading) return <div className="text-center py-5"><div className="spinner-border text-success"></div></div>;

  return (
    <div className="container py-4">
      <div className="d-flex align-items-center mb-4">
        <i className="bi bi-file-earmark-check-fill text-success me-2 fs-3"></i>
        <div>
          <h2 className="mb-0 fw-bold">My Offer Letters</h2>
          <p className="text-muted mb-0 small">Review and respond to your job offers</p>
        </div>
      </div>

      {msg && <div className={`alert ${msg.startsWith('Error') ? 'alert-danger' : 'alert-success'} alert-dismissible`}><i className={`bi ${msg.startsWith('Error') ? 'bi-exclamation-triangle' : 'bi-check-circle'} me-2`}></i>{msg}<button className="btn-close" onClick={() => setMsg('')}></button></div>}
      {error && <div className="alert alert-danger">{error}</div>}

      {offers.length === 0 ? (
        <div className="text-center py-5">
          <i className="bi bi-file-earmark-x text-muted" style={{fontSize:'4rem'}}></i>
          <p className="text-muted mt-3">No offers received yet. Keep applying!</p>
        </div>
      ) : (
        <div className="row g-4">
          {offers.map(o => (
            <div key={o.id} className="col-md-6 col-lg-4">
              <div className={`card border-0 shadow h-100 ${o.status === 'Accepted' ? 'border-success border' : ''}`}>
                <div className={`card-header bg-${STATUS_COLORS[o.status] || 'secondary'} text-white py-3`}>
                  <div className="d-flex justify-content-between align-items-start">
                    <div>
                      <div className="fw-bold">{o.offer_code}</div>
                      <small className="opacity-75">{o.employment_type}</small>
                    </div>
                    <span className="badge bg-white text-dark">{o.status}</span>
                  </div>
                </div>
                <div className="card-body">
                  <h5 className="fw-bold mb-3">{o.job_title}</h5>
                  
                  <div className="d-flex align-items-center mb-3 p-3 rounded" style={{background:'#f0fdf4'}}>
                    <i className="bi bi-currency-dollar text-success fs-4 me-2"></i>
                    <div>
                      <div className="small text-muted">Offered Salary</div>
                      <div className="fw-bold text-success fs-6">{o.offered_salary}</div>
                    </div>
                  </div>

                  <ul className="list-unstyled small mb-0">
                    <li className="mb-1"><i className="bi bi-calendar-check me-2 text-primary"></i><strong>Start Date:</strong> {o.start_date}</li>
                    <li className="mb-1"><i className="bi bi-calendar-x me-2 text-warning"></i><strong>Offer Expires:</strong> {o.expiration_date}</li>
                  </ul>

                  {o.notes && (
                    <div className="alert alert-light mt-3 mb-0 py-2 small"><i className="bi bi-sticky me-2"></i>{o.notes}</div>
                  )}
                </div>

                {o.status === 'Sent' && (
                  <div className="card-footer border-0 d-flex gap-2">
                    <button className="btn btn-success flex-grow-1" onClick={() => handleAccept(o.id, o.job_title)}>
                      <i className="bi bi-check-circle me-2"></i>Accept
                    </button>
                    <button className="btn btn-outline-danger flex-grow-1" onClick={() => handleDecline(o.id, o.job_title)}>
                      <i className="bi bi-x-circle me-2"></i>Decline
                    </button>
                  </div>
                )}
                {o.status === 'Accepted' && (
                  <div className="card-footer border-0 bg-success bg-opacity-10">
                    <div className="text-success fw-semibold text-center"><i className="bi bi-trophy-fill me-2"></i>Congratulations! Offer Accepted</div>
                  </div>
                )}
                {o.status === 'Declined' && (
                  <div className="card-footer border-0 bg-light">
                    <div className="text-muted text-center small">You declined this offer.</div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CandidateOffers;
