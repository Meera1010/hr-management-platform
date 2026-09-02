import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, ProgressBar, Spinner, Alert } from 'react-bootstrap';
import onboardingApi from '../../services/onboardingApi';

export default function OnboardingDashboard() {
  const [checklists, setChecklists] = useState([]);
  const [resignations, setResignations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [cRes, rRes] = await Promise.all([
        onboardingApi.getChecklists(),
        onboardingApi.getResignations()
      ]);
      setChecklists(cRes?.checklists || cRes?.data?.checklists || []);
      setResignations(rRes?.resignations || rRes?.data?.resignations || []);
    } catch (err) {
      setError(err.message || err.response?.data?.message || 'Failed to fetch lifecycle data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-5"><Spinner animation="border" variant="primary" /></div>;

  return (
    <Container fluid className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">Employee Onboarding & Exit Lifecycle</h2>
          <p className="text-muted">Monitor new hire orientation plans and exit clearance workflows.</p>
        </div>
      </div>

      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

      <Row className="mb-4 g-3">
        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Active Onboarding Plans</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Employee</th>
                    <th>Buddy</th>
                    <th>Completion</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {checklists.map(c => (
                    <tr key={c.id}>
                      <td className="fw-semibold">{c.employee_name}</td>
                      <td>{c.buddy_name || '-'}</td>
                      <td style={{ width: '180px' }}>
                        <div className="d-flex align-items-center gap-2">
                          <ProgressBar now={c.completion_percentage} variant="success" className="flex-grow-1" style={{ height: '6px' }} />
                          <small className="fw-bold">{c.completion_percentage}%</small>
                        </div>
                      </td>
                      <td><Badge bg={c.overall_status === 'Completed' ? 'success' : 'info'}>{c.overall_status}</Badge></td>
                    </tr>
                  ))}
                  {checklists.length === 0 && <tr><td colSpan="4" className="text-center py-4">No onboarding checklists found.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Resignations & Exit Clearances</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Employee</th>
                    <th>Submission Date</th>
                    <th>Last Working Day</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {resignations.map(r => (
                    <tr key={r.id}>
                      <td className="fw-semibold">{r.employee_name}</td>
                      <td>{r.submission_date}</td>
                      <td>{r.requested_last_working_day}</td>
                      <td><Badge bg={r.status === 'Approved' ? 'success' : 'warning'}>{r.status}</Badge></td>
                    </tr>
                  ))}
                  {resignations.length === 0 && <tr><td colSpan="4" className="text-center py-4">No resignation requests logged.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
