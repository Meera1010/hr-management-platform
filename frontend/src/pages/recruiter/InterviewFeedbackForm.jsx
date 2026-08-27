import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getInterview, submitInterviewFeedback, getInterviewFeedback } from '../../services/api';

const RECOMMENDATIONS = ['Strongly Recommend', 'Recommend', 'Neutral', 'Do Not Recommend'];

const InterviewFeedbackForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [interview, setInterview] = useState(null);
  const [existingFeedback, setExistingFeedback] = useState(null);
  const [form, setForm] = useState({
    technical_score: 3,
    communication_score: 3,
    problem_solving_score: 3,
    recommendation: 'Recommend',
    comments: ''
  });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const intData = await getInterview(id);
        setInterview(intData);
        try {
          const fb = await getInterviewFeedback(id);
          setExistingFeedback(fb);
          setForm({
            technical_score: fb.technical_score,
            communication_score: fb.communication_score,
            problem_solving_score: fb.problem_solving_score,
            recommendation: fb.recommendation,
            comments: fb.comments || ''
          });
        } catch (_) {}
      } catch (err) {
        setError('Failed to load interview details.');
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [id]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.type === 'range' ? parseInt(e.target.value) : e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      await submitInterviewFeedback(id, form);
      setSuccess('Feedback submitted successfully!');
      setTimeout(() => navigate('/recruiter/interviews'), 2000);
    } catch (err) {
      setError(err.message || 'Failed to submit feedback');
    } finally {
      setSubmitting(false);
    }
  };

  const ScoreSlider = ({ name, label, icon }) => (
    <div className="mb-4">
      <label className="form-label fw-semibold">{icon} {label}</label>
      <div className="d-flex align-items-center gap-3">
        <input type="range" className="form-range flex-grow-1" name={name} min="1" max="5" value={form[name]} onChange={handleChange} />
        <div className={`badge fs-5 fw-bold rounded-pill px-3 ${form[name] >= 4 ? 'bg-success' : form[name] >= 3 ? 'bg-warning text-dark' : 'bg-danger'}`}>{form[name]}/5</div>
      </div>
      <div className="d-flex justify-content-between text-muted small">
        <span>Poor</span><span>Average</span><span>Excellent</span>
      </div>
    </div>
  );

  if (loading) return <div className="text-center py-5"><div className="spinner-border text-primary"></div></div>;

  const overallScore = ((form.technical_score + form.communication_score + form.problem_solving_score) / 3).toFixed(1);

  return (
    <div className="container py-4" style={{maxWidth:'700px'}}>
      <div className="mb-3">
        <a href="/recruiter/interviews" className="btn btn-outline-secondary btn-sm"><i className="bi bi-arrow-left me-2"></i>Back</a>
      </div>

      {interview && (
        <div className="card border-0 shadow-sm mb-4">
          <div className="card-body">
            <div className="row">
              <div className="col-md-8">
                <h5 className="fw-bold mb-1">{interview.candidate_name}</h5>
                <div className="text-muted small">{interview.job_title} · {interview.interview_type} Interview</div>
                <div className="text-muted small">{interview.scheduled_date} at {interview.scheduled_time}</div>
              </div>
              <div className="col-md-4 text-end">
                <div className="fw-semibold">Interviewer</div>
                <div className="text-muted small">{interview.interviewer_name}</div>
                <span className={`badge ${interview.status === 'Completed' ? 'bg-success' : 'bg-primary'}`}>{interview.status}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {existingFeedback ? (
        <div className="alert alert-success">
          <i className="bi bi-check-circle-fill me-2"></i>
          Feedback already submitted. Overall Score: <strong>{existingFeedback.overall_score}/5</strong> · {existingFeedback.recommendation}
        </div>
      ) : (
        <div className="card border-0 shadow-sm">
          <div className="card-header bg-warning text-dark py-3">
            <h5 className="mb-0"><i className="bi bi-star-fill me-2"></i>Submit Interview Feedback</h5>
          </div>
          <div className="card-body">
            {error && <div className="alert alert-danger"><i className="bi bi-exclamation-triangle me-2"></i>{error}</div>}
            {success && <div className="alert alert-success"><i className="bi bi-check-circle me-2"></i>{success}</div>}

            {/* Preview Score */}
            <div className="text-center mb-4 p-3 rounded" style={{background:'linear-gradient(135deg,#f0f4ff,#e8f5e9)'}}>
              <div className={`display-4 fw-bold ${overallScore >= 4 ? 'text-success' : overallScore >= 3 ? 'text-warning' : 'text-danger'}`}>{overallScore}</div>
              <div className="text-muted">Overall Score (Live Preview)</div>
            </div>

            <form onSubmit={handleSubmit}>
              <ScoreSlider name="technical_score" label="Technical Skills" icon="🔧" />
              <ScoreSlider name="communication_score" label="Communication" icon="💬" />
              <ScoreSlider name="problem_solving_score" label="Problem Solving" icon="🧩" />

              <div className="mb-4">
                <label className="form-label fw-semibold">Recommendation <span className="text-danger">*</span></label>
                <div className="d-flex gap-2 flex-wrap">
                  {RECOMMENDATIONS.map(r => (
                    <label key={r} className={`btn ${form.recommendation === r ? 'btn-primary' : 'btn-outline-secondary'} d-flex align-items-center gap-1`}>
                      <input type="radio" name="recommendation" value={r} checked={form.recommendation === r} onChange={handleChange} className="d-none" />
                      {r}
                    </label>
                  ))}
                </div>
              </div>

              <div className="mb-4">
                <label className="form-label fw-semibold">Comments</label>
                <textarea className="form-control" name="comments" value={form.comments} onChange={handleChange} rows="4" placeholder="Detailed observations about the candidate's performance..."></textarea>
              </div>

              <button type="submit" className="btn btn-warning fw-bold w-100" disabled={submitting}>
                {submitting ? <><span className="spinner-border spinner-border-sm me-2"></span>Submitting...</> : <><i className="bi bi-send me-2"></i>Submit Feedback</>}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default InterviewFeedbackForm;
