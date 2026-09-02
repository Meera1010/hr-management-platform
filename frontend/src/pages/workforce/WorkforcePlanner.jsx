import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Spinner, Alert } from 'react-bootstrap';
import workforceApi from '../../services/workforceApi';

export default function WorkforcePlanner() {
  const [plans, setPlans] = useState([]);
  const [risks, setRisks] = useState([]);
  const [benchmarks, setBenchmarks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [pRes, rRes, bRes] = await Promise.all([
        workforceApi.getPlans(),
        workforceApi.getAttritionRisks(),
        workforceApi.getBenchmarks()
      ]);
      setPlans(pRes?.plans || pRes?.data?.plans || []);
      setRisks(rRes?.attrition_risks || rRes?.data?.attrition_risks || []);
      setBenchmarks(bRes?.benchmarks || bRes?.data?.benchmarks || []);
    } catch (err) {
      setError(err.message || err.response?.data?.message || 'Failed to fetch workforce analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-5"><Spinner animation="border" variant="primary" /></div>;

  return (
    <Container fluid className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">Workforce Planning & Predictive Analytics</h2>
          <p className="text-muted">Headcount forecasting, attrition flight-risk prediction, and salary competitiveness benchmarks.</p>
        </div>
      </div>

      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

      <Row className="mb-4 g-3">
        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Attrition Flight-Risk Analysis</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Employee</th>
                    <th>Department</th>
                    <th>Risk Score</th>
                    <th>Level</th>
                    <th>Primary Drivers</th>
                  </tr>
                </thead>
                <tbody>
                  {risks.map(r => (
                    <tr key={r.id}>
                      <td className="fw-semibold">{r.employee_name}</td>
                      <td>{r.department}</td>
                      <td className="fw-bold">{r.risk_score_pct}%</td>
                      <td><Badge bg={r.risk_level === 'Critical' ? 'danger' : (r.risk_level === 'High' ? 'warning' : 'info')}>{r.risk_level}</Badge></td>
                      <td><small className="text-muted">{r.primary_drivers}</small></td>
                    </tr>
                  ))}
                  {risks.length === 0 && <tr><td colSpan="5" className="text-center py-4">No risk evaluation data.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Industry Salary Benchmarks</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Job Title</th>
                    <th>Level</th>
                    <th>Company Avg</th>
                    <th>Industry Median</th>
                    <th>Competitiveness</th>
                  </tr>
                </thead>
                <tbody>
                  {benchmarks.map(b => (
                    <tr key={b.id}>
                      <td className="fw-semibold">{b.job_title}</td>
                      <td><Badge bg="secondary">{b.experience_level}</Badge></td>
                      <td className="fw-bold">₹{(b.company_avg_ctc / 100000).toFixed(1)}L</td>
                      <td>₹{(b.industry_median_ctc / 100000).toFixed(1)}L</td>
                      <td>
                        <Badge bg={b.competitive_index_pct >= 0 ? 'success' : 'danger'}>
                          {b.competitive_index_pct >= 0 ? `+${b.competitive_index_pct}%` : `${b.competitive_index_pct}%`}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                  {benchmarks.length === 0 && <tr><td colSpan="5" className="text-center py-4">No salary benchmarks configured.</td></tr>}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
