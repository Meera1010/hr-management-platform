import React, { useState, useEffect } from 'react';
import {
  getAttendance, checkIn, checkOut, getAttendanceSummary
} from '../../services/api';

const STATUS_COLORS = {
  'Present': 'success',
  'Absent': 'danger',
  'Half Day': 'warning',
  'Work From Home': 'info',
  'On Leave': 'secondary'
};

const EmployeeAttendance = () => {
  const [records, setRecords] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState('');
  const [error, setError] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  const today = new Date().toLocaleDateString('en-GB', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  const todayISO = new Date().toISOString().split('T')[0];

  const todayRecord = records.find(r => r.attendance_date === todayISO);
  const canCheckIn = !todayRecord;
  const canCheckOut = todayRecord && !todayRecord.check_out;

  const load = async () => {
    setLoading(true);
    try {
      const data = await getAttendance();
      setRecords(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleCheckIn = async () => {
    setActionLoading(true);
    try {
      await checkIn();
      setMsg('✅ Check-in successful! Have a productive day.');
      load();
    } catch (err) {
      setMsg('❌ ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleCheckOut = async () => {
    setActionLoading(true);
    try {
      await checkOut();
      setMsg('✅ Check-out successful! See you tomorrow.');
      load();
    } catch (err) {
      setMsg('❌ ' + err.message);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) return <div className="text-center py-5"><div className="spinner-border text-primary"></div></div>;

  return (
    <div className="container py-4">
      {/* Header */}
      <div className="d-flex align-items-center mb-4">
        <i className="bi bi-calendar-check-fill text-primary me-2 fs-3"></i>
        <div>
          <h2 className="mb-0 fw-bold">My Attendance</h2>
          <p className="text-muted mb-0 small">{today}</p>
        </div>
      </div>

      {msg && <div className="alert alert-info alert-dismissible"><i className="bi bi-info-circle me-2"></i>{msg}<button className="btn-close" onClick={() => setMsg('')}></button></div>}
      {error && <div className="alert alert-danger">{error}</div>}

      {/* Today's Card + Actions */}
      <div className="row g-3 mb-4">
        <div className="col-md-4">
          <div className="card border-0 shadow-sm h-100" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
            <div className="card-body text-white p-4">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <div className="small opacity-75 mb-1">Today's Status</div>
                  <h4 className="fw-bold mb-0">
                    {todayRecord ? todayRecord.status : 'Not Marked'}
                  </h4>
                </div>
                <i className="bi bi-calendar-day fs-2 opacity-50"></i>
              </div>
              {todayRecord && (
                <div className="small">
                  {todayRecord.check_in && <div><i className="bi bi-box-arrow-in-right me-1"></i>In: {todayRecord.check_in}</div>}
                  {todayRecord.check_out && <div><i className="bi bi-box-arrow-right me-1"></i>Out: {todayRecord.check_out}</div>}
                  {todayRecord.work_hours && <div><i className="bi bi-clock me-1"></i>Hours: {todayRecord.work_hours}h</div>}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body p-4 d-flex flex-column justify-content-center align-items-center">
              <div className="small text-muted mb-2">Mark Attendance</div>
              <div className="d-grid gap-2 w-100">
                <button
                  className="btn btn-success"
                  onClick={handleCheckIn}
                  disabled={!canCheckIn || actionLoading}
                >
                  <i className="bi bi-box-arrow-in-right me-2"></i>
                  {actionLoading ? 'Processing...' : 'Check In'}
                </button>
                <button
                  className="btn btn-warning"
                  onClick={handleCheckOut}
                  disabled={!canCheckOut || actionLoading}
                >
                  <i className="bi bi-box-arrow-right me-2"></i>
                  {actionLoading ? 'Processing...' : 'Check Out'}
                </button>
              </div>
              {!canCheckIn && !canCheckOut && (
                <div className="text-success small mt-2"><i className="bi bi-check-circle-fill me-1"></i>Day completed</div>
              )}
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body p-4">
              <div className="small text-muted mb-3">This Month Summary</div>
              {records.length === 0 ? (
                <p className="text-muted small">No records yet.</p>
              ) : (
                <>
                  <div className="d-flex justify-content-between mb-1"><span className="small">Present</span><span className="badge bg-success">{records.filter(r => r.status === 'Present').length}</span></div>
                  <div className="d-flex justify-content-between mb-1"><span className="small">Absent</span><span className="badge bg-danger">{records.filter(r => r.status === 'Absent').length}</span></div>
                  <div className="d-flex justify-content-between mb-1"><span className="small">WFH</span><span className="badge bg-info">{records.filter(r => r.status === 'Work From Home').length}</span></div>
                  <div className="d-flex justify-content-between"><span className="small">Half Day</span><span className="badge bg-warning text-dark">{records.filter(r => r.status === 'Half Day').length}</span></div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Attendance Records Table */}
      <div className="card border-0 shadow-sm">
        <div className="card-header bg-white border-bottom py-3">
          <h5 className="mb-0 fw-semibold"><i className="bi bi-table me-2 text-primary"></i>Attendance Records</h5>
        </div>
        <div className="card-body p-0">
          {records.length === 0 ? (
            <div className="text-center py-5">
              <i className="bi bi-calendar-x text-muted" style={{ fontSize: '3rem' }}></i>
              <p className="text-muted mt-3">No attendance records found.</p>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Date</th>
                    <th>Check In</th>
                    <th>Check Out</th>
                    <th>Work Hours</th>
                    <th>Status</th>
                    <th>Remarks</th>
                  </tr>
                </thead>
                <tbody>
                  {records.map(r => (
                    <tr key={r.id}>
                      <td className="fw-semibold">{r.attendance_date}</td>
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

export default EmployeeAttendance;
