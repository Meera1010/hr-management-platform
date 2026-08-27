import React, { useState, useEffect } from 'react';
import { getPerformanceReviews } from '../../services/api';

const SCORE_COLOR = (score) => {
  if (score >= 4.5) return 'success';
  if (score >= 3.5) return 'primary';
  if (score >= 2.5) return 'warning';
  return 'danger';
};

const ScoreBadge = ({ score }) => (
  <span className={`badge bg-${SCORE_COLOR(score)} rounded-pill`}>{score}</span>
);

const EmployeePerformance = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const data = await getPerformanceReviews();
        setReviews(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <div className="text-center py-5"><div className="spinner-border text-success"></div></div>;

  const avgScore = reviews.length > 0
    ? (reviews.reduce((s, r) => s + r.overall_score, 0) / reviews.length).toFixed(2)
    : null;

  return (
    <div className="container py-4">
      <div className="d-flex align-items-center mb-4">
        <i className="bi bi-graph-up-arrow text-success me-2 fs-3"></i>
        <div>
          <h2 className="mb-0 fw-bold">My Performance Reviews</h2>
          <p className="text-muted mb-0 small">View your completed performance assessments</p>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {/* Summary */}
      <div className="row g-3 mb-4">
        <div className="col-md-4">
          <div className="card border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)' }}>
            <div className="card-body text-white p-4">
              <div className="small opacity-75">Average Score</div>
              <div className="display-5 fw-bold">{avgScore || '—'}</div>
              <div className="small opacity-75">out of 5.0</div>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card border-0 shadow-sm">
            <div className="card-body p-4">
              <div className="small text-muted">Total Reviews</div>
              <div className="display-6 fw-bold text-primary">{reviews.length}</div>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card border-0 shadow-sm">
            <div className="card-body p-4">
              <div className="small text-muted">Latest Period</div>
              <div className="fw-bold fs-5 text-success">{reviews[0]?.review_period || '—'}</div>
            </div>
          </div>
        </div>
      </div>

      {reviews.length === 0 ? (
        <div className="text-center py-5">
          <i className="bi bi-clipboard-x text-muted" style={{ fontSize: '4rem' }}></i>
          <p className="text-muted mt-3">No completed performance reviews yet.</p>
        </div>
      ) : (
        <div className="row g-4">
          {reviews.map(r => (
            <div key={r.id} className="col-md-6">
              <div className="card border-0 shadow h-100">
                <div className="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
                  <div>
                    <span className="badge bg-light text-dark border me-2">{r.review_code}</span>
                    <strong>{r.review_period}</strong>
                  </div>
                  <ScoreBadge score={r.overall_score} />
                </div>
                <div className="card-body">
                  <div className="row g-2 mb-3">
                    {[
                      { label: 'Productivity', val: r.productivity_score },
                      { label: 'Quality',      val: r.quality_score },
                      { label: 'Teamwork',     val: r.teamwork_score },
                      { label: 'Goals',        val: r.goal_score },
                    ].map(dim => (
                      <div key={dim.label} className="col-6">
                        <div className="d-flex justify-content-between small mb-1">
                          <span>{dim.label}</span><span className="fw-bold">{dim.val}/5</span>
                        </div>
                        <div className="progress" style={{ height: 6 }}>
                          <div
                            className={`progress-bar bg-${SCORE_COLOR(dim.val)}`}
                            style={{ width: `${(dim.val / 5) * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="mb-2">
                    <div className="d-flex justify-content-between mb-1">
                      <span className="small fw-semibold">Overall Score</span>
                      <span className="fw-bold">{r.overall_score}/5.0</span>
                    </div>
                    <div className="progress" style={{ height: 10 }}>
                      <div className={`progress-bar bg-${SCORE_COLOR(r.overall_score)}`} style={{ width: `${(r.overall_score / 5) * 100}%` }}></div>
                    </div>
                  </div>
                  {r.comments && (
                    <div className="alert alert-light mt-3 mb-0 py-2">
                      <div className="small text-muted mb-1"><i className="bi bi-quote me-1"></i>Reviewer: {r.reviewer_name}</div>
                      <div className="small">{r.comments}</div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EmployeePerformance;
