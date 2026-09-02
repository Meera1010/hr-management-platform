import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Spinner, Alert } from 'react-bootstrap';
import complianceApi from '../../services/complianceApi';

export default function GrievanceCenter() {
  const [grievances, setGrievances] = useState([]);
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [gRes, pRes] = await Promise.all([
        complianceApi.getGrievances(),
        complianceApi.getPolicies()
      ]);
      setGrievances(gRes?.tickets || gRes?.data?.tickets || []);
      setPolicies(pRes?.policies || pRes?.data?.policies || []);
    } catch (err) {
      setError(err.message || err.response?.data?.message || 'Failed to fetch compliance data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-5"><Spinner animation="border" variant="primary" /></div>;

  return (
    <Container fluid className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">Grievance & HR Policy Compliance</h2>
          <p className="text-muted">Confidential case reporting, policy library, and mandatory policy acknowledgments.</p>
        </div>
      </div>

      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

      <Row className="mb-4 g-3">
        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Grievance Case Tickets</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Ticket #</th>
                    <th>Category</th>
                    <th>Subject</th>
                    <th>Severity</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {grievances.map(g => (
                    <tr key={g.id}>
                      <td className="fw-bold text-danger">{g.ticket_number}</td>
                      <td>{g.category}</td>
                      <td className="fw-semibold">{g.subject}</td>
                      <td><Badge bg={g.severity === 'Critical' ? 'danger' : 'warning'}>{g.severity}</Badge></td>
                      <td><Badge bg={g.status === 'Resolved' ? 'success' : 'secondary'}>{g.status}</Badge></td>
                    </tr>
                  ))}
                  {grievances.length === 0 && <tr><td colSpan="5" className="text-center py-4">No grievance cases reported.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Company Policy Documents</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Code</th>
                    <th>Policy Title</th>
                    <th>Category</th>
                    <th>Version</th>
                  </tr>
                </thead>
                <tbody>
                  {policies.map(p => (
                    <tr key={p.id}>
                      <td className="fw-bold text-primary">{p.code}</td>
                      <td className="fw-semibold">{p.title}</td>
                      <td><Badge bg="info">{p.category}</Badge></td>
                      <td><code>v{p.version}</code></td>
                    </tr>
                  ))}
                  {policies.length === 0 && <tr><td colSpan="4" className="text-center py-4">No policy documents published.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
