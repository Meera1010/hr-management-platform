import React, { useState, useEffect } from 'react';

const SCORE_COLOR = (s) => s >= 4.5 ? 'success' : s >= 3.5 ? 'primary' : s >= 2.5 ? 'warning' : 'danger';

const defaultForm = { employee_id: '', review_period: '', productivity_score: 3, quality_score: 3, teamwork_score: 3, goal_score: 3, reviewer_name: '', comments: '', status: 'Draft' };

const PerformanceForm = ({ initial = defaultForm, onSave, onCancel }) => {
  const [form, setForm] = useState(initial);

  const overall = (
    (parseInt(form.productivity_score) || 0) +
    (parseInt(form.quality_score) || 0) +
    (parseInt(form.teamwork_score) || 0) +
    (parseInt(form.goal_score) || 0)
  ) / 4;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ ...form, productivity_score: parseInt(form.productivity_score), quality_score: parseInt(form.quality_score), teamwork_score: parseInt(form.teamwork_score), goal_score: parseInt(form.goal_score) });
  };

  const scoreField = (label, key) => (
    <div className="mb-3">
      <div className="d-flex justify-content-between">
        <label className="form-label fw-semibold">{label}</label>
        <span className={`badge bg-${SCORE_COLOR(parseInt(form[key]) || 0)}`}>{form[key]}/5</span>
      </div>
      <input type="range" className="form-range" min="1" max="5" step="1" value={form[key]} onChange={e => setForm({...form, [key]: e.target.value})} />
      <div className="d-flex justify-content-between small text-muted">
        <span>1 - Poor</span><span>3 - Average</span><span>5 - Excellent</span>
      </div>
    </div>
  );

  return (
    <form onSubmit={handleSubmit}>
      <div className="row g-3">
        <div className="col-md-4">
          <label className="form-label fw-semibold">Employee ID *</label>
          <input className="form-control" value={form.employee_id} onChange={e => setForm({...form, employee_id: e.target.value})} required />
        </div>
        <div className="col-md-4">
          <label className="form-label fw-semibold">Review Period *</label>
          <input className="form-control" value={form.review_period} onChange={e => setForm({...form, review_period: e.target.value})} placeholder="e.g. Q1 2026" required />
        </div>
        <div className="col-md-4">
          <label className="form-label fw-semibold">Reviewer Name *</label>
          <input className="form-control" value={form.reviewer_name} onChange={e => setForm({...form, reviewer_name: e.target.value})} required />
        </div>
        <div className="col-md-6">
          {scoreField('Productivity Score', 'productivity_score')}
          {scoreField('Quality Score', 'quality_score')}
        </div>
        <div className="col-md-6">
          {scoreField('Teamwork Score', 'teamwork_score')}
          {scoreField('Goal Achievement Score', 'goal_score')}
        </div>
        <div className="col-12">
          <div className={`alert alert-${SCORE_COLOR(overall)} py-2`}>
            <strong>Calculated Overall Score: {overall.toFixed(2)} / 5.0</strong>
            <span className="ms-2 small text-muted">(auto-calculated by server)</span>
          </div>
        </div>
        <div className="col-md-8">
          <label className="form-label fw-semibold">Comments</label>
          <textarea className="form-control" rows={3} value={form.comments} onChange={e => setForm({...form, comments: e.target.value})} />
        </div>
        <div className="col-md-4">
          <label className="form-label fw-semibold">Status</label>
          <select className="form-select" value={form.status} onChange={e => setForm({...form, status: e.target.value})}>
            <option value="Draft">Draft</option>
            <option value="Completed">Completed</option>
          </select>
        </div>
        <div className="col-12 d-flex gap-2">
          <button type="submit" className="btn btn-success"><i className="bi bi-save me-2"></i>Save Review</button>
          <button type="button" className="btn btn-outline-secondary" onClick={onCancel}>Cancel</button>
        </div>
      </div>
    </form>
  );
};

export default PerformanceForm;
