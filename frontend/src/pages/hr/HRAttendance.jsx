import React, { useState, useEffect } from 'react';
import { getAttendance, createAttendance, updateAttendance } from '../../services/api';

const STATUS_COLORS = { Present: 'success', Absent: 'danger', 'Half Day': 'warning', 'Work From Home': 'info', 'On Leave': 'secondary' };
const STATUSES = ['Present', 'Absent', 'Half Day', 'Work From Home', 'On Leave'];

const HRAttendance = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ employee_id: '', date: '', status: '' });
  const [msg, setMsg] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ employee_id: '', attendance_date: '', status: 'Present', check_in: '', check_out: '', remarks: '' });

  const load = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.employee_id) params.set('employee_id', filters.employee_id);
      if (filters.date) params.set('date', filters.date);
      if (filters.status) params.set('status', filters.status);
      const data = await getAttendance(params.toString());
      setRecords(Array.isArray(data) ? data : []);
    } catch {
      setRecords([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleFilter = (e) => { e.preventDefault(); load(); };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await createAttendance(form);
      setMsg('Attendance record created.');
      setShowForm(false);
      setForm({ employee_id: '', attendance_date: '', status: 'Present', check_in: '', check_out: '', remarks: '' });
      load();
    } catch (err) {
      setMsg('Error: ' + err.message);
    }
  };

  const todayPresent = records.filter(r => r.status === 'Present').length;
  const todayAbsent = records.filter(r => r.status === 'Absent').length;
  const todayWFH = records.filter(r => r.status === 'Work From Home').length;

  return (
    <div className="container py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div className="d-flex align-items-center">
          <i className="bi bi-people-fill text-primary me-2 fs-3"></i>
          <div>
            <h2 className="mb-0 fw-bold">HR — Attendance Management</h2>
            <p className="text-muted mb-0 small">View and manage all employee attendance records</p>
          </div>
        </div>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          <i className={`bi bi-${showForm ? 'x-lg' : 'plus-lg'} me-2`}></i>
          {showForm ? 'Close' : 'Add Record'}
        </button>
      </div>

      {/* Stats */}
      <div className="row g-3 mb-4">
        {[
          { label: 'Total Records', val: records.length, color: 'primary', icon: 'bi-calendar2-check' },
          { label: 'Present', val: todayPresent, color: 'success', icon: 'bi-person-check' },
          { label: 'Absent', val: todayAbsent, color: 'danger', icon: 'bi-person-x' },
          { label: 'WFH', val: todayWFH, color: 'info', icon: 'bi-house-check' },
        ].map((s, i) => (
          <div key={i} className="col-md-3">
            <div className={`card border-0 shadow-sm border-top border-${s.color} border-3`}>
              <div className="card-body py-3">
                <div className="d-flex align-items-center">
                  <i className={`bi ${s.icon} text-${s.color} fs-3 me-3`}></i>
                  <div><div className="small text-muted">{s.label}</div><div className="fw-bold fs-5">{s.val}</div></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {msg && <div className="alert alert-info alert-dismissible">{msg}<button className="btn-close" onClick={() => setMsg('')}></button></div>}

      {/* Manual Create Form */}
      {showForm && (
        <div className="card border-0 shadow-sm mb-4">
          <div className="card-header"><h6 className="mb-0"><i className="bi bi-plus-circle me-2"></i>Add Attendance Record</h6></div>
          <div className="card-body">
            <form onSubmit={handleCreate}>
              <div className="row g-3">
                <div className="col-md-3"><label className="form-label">Employee ID *</label><input className="form-control" value={form.employee_id} onChange={e => setForm({...form, employee_id: e.target.value})} required /></div>
                <div className="col-md-3"><label className="form-label">Date *</label><input type="date" className="form-control" value={form.attendance_date} onChange={e => setForm({...form, attendance_date: e.target.value})} required /></div>
                <div className="col-md-2"><label className="form-label">Status *</label>
                  <select className="form-select" value={form.status} onChange={e => setForm({...form, status: e.target.value})}>
                    {STATUSES.map(s => <option key={s}>{s}</option>)}
                  </select>
                </div>
                <div className="col-md-2"><label className="form-label">Check In</label><input type="time" className="form-control" value={form.check_in} onChange={e => setForm({...form, check_in: e.target.value + ':00'})} /></div>
                <div className="col-md-2"><label className="form-label">Check Out</label><input type="time" className="form-control" value={form.check_out} onChange={e => setForm({...form, check_out: e.target.value + ':00'})} /></div>
                <div className="col-md-6"><label className="form-label">Remarks</label><input className="form-control" value={form.remarks} onChange={e => setForm({...form, remarks: e.target.value})} /></div>
                <div className="col-12"><button type="submit" className="btn btn-primary"><i className="bi bi-save me-2"></i>Save</button></div>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="card border-0 shadow-sm mb-4">
        <div className="card-body py-3">
          <form className="row g-2 align-items-end" onSubmit={handleFilter}>
            <div className="col-md-3"><label className="form-label small">Employee ID</label><input className="form-control form-control-sm" value={filters.employee_id} onChange={e => setFilters({...filters, employee_id: e.target.value})} /></div>
            <div className="col-md-3"><label className="form-label small">Date</label><input type="date" className="form-control form-control-sm" value={filters.date} onChange={e => setFilters({...filters, date: e.target.value})} /></div>
            <div className="col-md-3"><label className="form-label small">Status</label>
              <select className="form-select form-select-sm" value={filters.status} onChange={e => setFilters({...filters, status: e.target.value})}>
                <option value="">All Statuses</option>
                {STATUSES.map(s => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div className="col-md-3 d-flex gap-2">
              <button type="submit" className="btn btn-primary btn-sm">Filter</button>
              <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => { setFilters({ employee_id: '', date: '', status: '' }); setTimeout(load, 100); }}>Clear</button>
            </div>
          </form>
        </div>
      </div>

      {/* Records Table */}
      <div className="card border-0 shadow-sm">
        <div className="card-body p-0">
          {loading ? <div className="text-center py-4"><div className="spinner-border text-primary"></div></div> : records.length === 0 ? (
            <div className="text-center py-5"><i className="bi bi-calendar-x text-muted fs-1"></i><p className="text-muted mt-2">No records found.</p></div>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead className="table-light">
                  <tr><th>Employee</th><th>Dept</th><th>Date</th><th>Check In</th><th>Check Out</th><th>Hours</th><th>Status</th><th>Remarks</th></tr>
                </thead>
                <tbody>
                  {records.map(r => (
                    <tr key={r.id}>
                      <td><div className="fw-semibold">{r.employee_name}</div><small className="text-muted">{r.employee_code}</small></td>
                      <td><span className="text-muted small">{r.department_name}</span></td>
                      <td>{r.attendance_date}</td>
                      <td>{r.check_in || '—'}</td>
                      <td>{r.check_out || '—'}</td>
                      <td>{r.work_hours ? `${r.work_hours}h` : '—'}</td>
                      <td><span className={`badge bg-${STATUS_COLORS[r.status] || 'secondary'}`}>{r.status}</span></td>
                      <td><span className="text-muted small">{r.remarks || '—'}</span></td>
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

export default HRAttendance;
