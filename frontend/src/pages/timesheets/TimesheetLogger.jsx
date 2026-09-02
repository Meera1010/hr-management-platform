import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Button, Spinner, Alert } from 'react-bootstrap';
import timesheetApi from '../../services/timesheetApi';

export default function TimesheetLogger() {
  const [timesheets, setTimesheets] = useState([]);
  const [rosters, setRosters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [tRes, rRes] = await Promise.all([
        timesheetApi.getTimesheets(),
        timesheetApi.getRosters()
      ]);
      setTimesheets(tRes?.timesheets || tRes?.data?.timesheets || []);
      setRosters(rRes?.rosters || rRes?.data?.rosters || []);
    } catch (err) {
      setError(err.message || err.response?.data?.message || 'Failed to fetch timesheets');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-5"><Spinner animation="border" variant="primary" /></div>;

  return (
    <Container fluid className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">Timesheets & Shift Roster Management</h2>
          <p className="text-muted">Track weekly billable work hours and scheduled employee shifts.</p>
        </div>
      </div>

      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

      <Row className="mb-4 g-3">
        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Weekly Timesheet Submissions</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Employee</th>
                    <th>Week Period</th>
                    <th>Total Hours</th>
                    <th>Billable Hours</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {timesheets.map(t => (
                    <tr key={t.id}>
                      <td className="fw-semibold">{t.employee_name}</td>
                      <td>{t.week_start_date} to {t.week_end_date}</td>
                      <td>{t.total_hours} hrs</td>
                      <td className="fw-bold text-success">{t.billable_hours} hrs</td>
                      <td><Badge bg={t.status === 'Approved' ? 'success' : 'info'}>{t.status}</Badge></td>
                    </tr>
                  ))}
                  {timesheets.length === 0 && <tr><td colSpan="5" className="text-center py-4">No weekly timesheets logged.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Shift Roster Schedule</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Employee</th>
                    <th>Shift</th>
                    <th>Timings</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {rosters.map(r => (
                    <tr key={r.id}>
                      <td className="fw-semibold">{r.employee_name}</td>
                      <td><Badge bg="primary">{r.shift_name}</Badge></td>
                      <td>{r.shift_start} - {r.shift_end}</td>
                      <td>{r.roster_date}</td>
                    </tr>
                  ))}
                  {rosters.length === 0 && <tr><td colSpan="4" className="text-center py-4">No shift rosters scheduled.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
