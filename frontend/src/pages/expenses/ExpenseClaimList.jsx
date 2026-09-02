import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Spinner, Alert } from 'react-bootstrap';
import expenseApi from '../../services/expenseApi';

export default function ExpenseClaimList() {
  const [claims, setClaims] = useState([]);
  const [travels, setTravels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [cRes, tRes] = await Promise.all([
        expenseApi.getClaims(),
        expenseApi.getTravelRequests()
      ]);
      setClaims(cRes?.claims || cRes?.data?.claims || []);
      setTravels(tRes?.requests || tRes?.data?.requests || []);
    } catch (err) {
      setError(err.message || err.response?.data?.message || 'Failed to fetch expense claims');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-5"><Spinner animation="border" variant="primary" /></div>;

  return (
    <Container fluid className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">Expenses & Travel Claims</h2>
          <p className="text-muted">Reimbursement claims, receipt audits, and business travel pre-approvals.</p>
        </div>
      </div>

      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

      <Row className="mb-4 g-3">
        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Reimbursement Claims</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Claim #</th>
                    <th>Employee</th>
                    <th>Title</th>
                    <th>Total Amount</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {claims.map(c => (
                    <tr key={c.id}>
                      <td className="fw-bold text-primary">{c.claim_number}</td>
                      <td>{c.employee_name}</td>
                      <td className="fw-semibold">{c.title}</td>
                      <td className="fw-bold">₹{c.total_amount?.toLocaleString()}</td>
                      <td><Badge bg={c.status === 'Paid' ? 'success' : 'info'}>{c.status}</Badge></td>
                    </tr>
                  ))}
                  {claims.length === 0 && <tr><td colSpan="5" className="text-center py-4">No expense claims submitted.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Travel Pre-Approvals</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Request #</th>
                    <th>Employee</th>
                    <th>Destination</th>
                    <th>Est. Cost</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {travels.map(t => (
                    <tr key={t.id}>
                      <td className="fw-bold text-dark">{t.request_number}</td>
                      <td>{t.employee_name}</td>
                      <td className="fw-semibold">{t.destination}</td>
                      <td>₹{t.estimated_cost?.toLocaleString()}</td>
                      <td><Badge bg={t.status === 'Approved' ? 'success' : 'warning'}>{t.status}</Badge></td>
                    </tr>
                  ))}
                  {travels.length === 0 && <tr><td colSpan="5" className="text-center py-4">No business travel requests logged.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
