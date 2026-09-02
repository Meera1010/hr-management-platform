import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, ProgressBar, Spinner, Alert } from 'react-bootstrap';
import okrApi from '../../services/okrApi';

export default function OkrDashboard() {
  const [objectives, setObjectives] = useState([]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [oRes, fRes] = await Promise.all([
        okrApi.getObjectives(),
        okrApi.get360Feedback()
      ]);
      setObjectives(oRes?.objectives || oRes?.data?.objectives || []);
      setFeedbacks(fRes?.feedbacks || fRes?.data?.feedbacks || []);
    } catch (err) {
      setError(err.message || err.response?.data?.message || 'Failed to fetch OKR data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-5"><Spinner animation="border" variant="primary" /></div>;

  return (
    <Container fluid className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">OKRs & 360-Degree Performance</h2>
          <p className="text-muted">Align team objectives, key results, and multi-evaluator feedback.</p>
        </div>
      </div>

      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

      <Row className="mb-4 g-3">
        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Quarterly OKR Objectives</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Objective</th>
                    <th>Level</th>
                    <th>Quarter</th>
                    <th>Progress</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {objectives.map(o => (
                    <tr key={o.id}>
                      <td className="fw-semibold">{o.title}</td>
                      <td><Badge bg="secondary">{o.level}</Badge></td>
                      <td>{o.period_quarter}</td>
                      <td style={{ width: '150px' }}>
                        <div className="d-flex align-items-center gap-2">
                          <ProgressBar now={o.progress_pct} variant="info" className="flex-grow-1" style={{ height: '6px' }} />
                          <small className="fw-bold">{o.progress_pct}%</small>
                        </div>
                      </td>
                      <td><Badge bg={o.status === 'Completed' ? 'success' : (o.status === 'On Track' ? 'info' : 'warning')}>{o.status}</Badge></td>
                    </tr>
                  ))}
                  {objectives.length === 0 && <tr><td colSpan="5" className="text-center py-4">No OKR objectives created.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">360-Degree Feedback Submissions</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Evaluatee</th>
                    <th>Evaluator</th>
                    <th>Relation</th>
                    <th>Overall Rating</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {feedbacks.map(f => (
                    <tr key={f.id}>
                      <td className="fw-semibold">{f.evaluatee_name}</td>
                      <td>{f.evaluator_name}</td>
                      <td><Badge bg="outline-secondary">{f.relationship}</Badge></td>
                      <td className="fw-bold text-primary">{f.overall_rating} / 5.0</td>
                      <td><Badge bg={f.status === 'Submitted' ? 'success' : 'secondary'}>{f.status}</Badge></td>
                    </tr>
                  ))}
                  {feedbacks.length === 0 && <tr><td colSpan="5" className="text-center py-4">No 360 feedback reviews logged.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
