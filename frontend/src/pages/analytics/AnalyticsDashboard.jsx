import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, ProgressBar, Table, Spinner, Alert } from 'react-bootstrap';
import { getAnalyticsOverview } from '../../services/api';

const AnalyticsDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const res = await getAnalyticsOverview();
      setData(res.analytics || {});
    } catch (err) {
      setError(err.message || 'Error loading analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Container className="py-5 text-center"><Spinner animation="border" /></Container>;
  if (error) return <Container className="py-5"><Alert variant="danger">{error}</Alert></Container>;

  const funnel = data.funnel || {};
  const depts = data.departments || [];
  const empTypes = data.employment_types || {};
  const leaves = data.leaves || {};

  return (
    <Container className="py-4">
      <h2>HR & Recruitment Analytics</h2>
      <p className="text-muted">High-level workforce metrics, recruitment funnel progression, and department breakdown.</p>

      {/* Recruitment Funnel */}
      <Card className="shadow-sm mb-4">
        <Card.Header className="bg-white fw-bold">Recruitment Pipeline Funnel</Card.Header>
        <Card.Body>
          <Row className="g-3 align-items-center mb-3 text-center">
            <Col>
              <div className="fw-bold fs-4">{funnel.total_applications || 0}</div>
              <div className="small text-muted">Applications</div>
            </Col>
            <Col>➔</Col>
            <Col>
              <div className="fw-bold fs-4">{funnel.shortlisted || 0}</div>
              <div className="small text-muted">Shortlisted</div>
            </Col>
            <Col>➔</Col>
            <Col>
              <div className="fw-bold fs-4">{funnel.interviewed || 0}</div>
              <div className="small text-muted">Interviewed</div>
            </Col>
            <Col>➔</Col>
            <Col>
              <div className="fw-bold fs-4 text-success">{funnel.hired || 0}</div>
              <div className="small text-muted fw-bold">Hired</div>
            </Col>
          </Row>

          <ProgressBar className="mt-3" style={{ height: '20px' }}>
            <ProgressBar striped variant="primary" now={100} label={`Apps (${funnel.total_applications})`} key={1} />
            <ProgressBar striped variant="info" now={funnel.total_applications ? (funnel.shortlisted/funnel.total_applications)*100 : 0} label={`Shortlisted (${funnel.shortlisted})`} key={2} />
            <ProgressBar striped variant="warning" now={funnel.total_applications ? (funnel.interviewed/funnel.total_applications)*100 : 0} label={`Interviewed (${funnel.interviewed})`} key={3} />
            <ProgressBar striped variant="success" now={funnel.total_applications ? (funnel.hired/funnel.total_applications)*100 : 0} label={`Hired (${funnel.hired})`} key={4} />
          </ProgressBar>
        </Card.Body>
      </Card>

      <Row className="g-4 mb-4">
        {/* Department Headcount */}
        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">Department Headcount & Openings</Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="mb-0">
                <thead className="bg-light">
                  <tr>
                    <th>Department</th>
                    <th>Active Employees</th>
                    <th>Open Jobs</th>
                  </tr>
                </thead>
                <tbody>
                  {depts.map(d => (
                    <tr key={d.department_id}>
                      <td>{d.name}</td>
                      <td>{d.employee_count}</td>
                      <td>{d.open_jobs}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        {/* Workforce Overview */}
        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">Workforce Composition & Performance</Card.Header>
            <Card.Body>
              <h6 className="mb-3">Employment Type Distribution</h6>
              <div className="mb-2">Full Time: <strong>{empTypes.full_time || 0}</strong></div>
              <div className="mb-2">Part Time: <strong>{empTypes.part_time || 0}</strong></div>
              <div className="mb-2">Contract: <strong>{empTypes.contract || 0}</strong></div>
              <div className="mb-4">Intern: <strong>{empTypes.intern || 0}</strong></div>

              <hr />

              <h6 className="mb-2">Average Performance Review Score</h6>
              <div className="display-6 text-primary fw-bold mb-3">{data.average_performance_score || 0.0} / 5.0</div>

              <h6>Leave Utilization Summary</h6>
              <div className="small text-muted">
                Total Requests: {leaves.total || 0} | Approved: {leaves.approved || 0} | Pending: {leaves.pending || 0}
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default AnalyticsDashboard;
