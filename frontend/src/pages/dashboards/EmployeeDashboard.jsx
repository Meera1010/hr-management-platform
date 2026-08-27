import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Spinner, Alert, Badge } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { getDashboardStats } from '../../services/api';

const EmployeeDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const res = await getDashboardStats();
      setStats(res.metrics || {});
    } catch (err) {
      setError(err.message || 'Failed to load employee portal');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Container className="py-5 text-center"><Spinner animation="border" /></Container>;
  if (error) return <Container className="py-5"><Alert variant="danger">{error}</Alert></Container>;

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2>Employee Self-Service Portal</h2>
          <p className="text-muted">Manage your leaves, attendance, training courses, and internal career growth.</p>
        </div>
        <div>
          <Button as={Link} to="/my-training" variant="primary" className="me-2">My Trainings</Button>
          <Button as={Link} to="/career-recommendations" variant="outline-success">Career Growth AI</Button>
        </div>
      </div>

      <Row className="g-3 mb-4">
        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-light">
            <Card.Body>
              <h6 className="text-muted">Employee Code</h6>
              <h5><Badge bg="secondary">{stats.employee_code || 'EMP'}</Badge></h5>
              <div className="small text-muted">{stats.designation || 'Staff'}</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-info text-white">
            <Card.Body>
              <h3>{stats.pending_leaves || 0}</h3>
              <div>Pending Leave Requests</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-success text-white">
            <Card.Body>
              <h3>{stats.approved_leaves || 0}</h3>
              <div>Approved Leaves</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-primary text-white">
            <Card.Body>
              <h3>{stats.completed_trainings || 0} / {stats.assigned_trainings || 0}</h3>
              <div>Trainings Completed</div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="g-4">
        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">Self-Service Actions</Card.Header>
            <Card.Body className="d-grid gap-2">
              <Button as={Link} to="/employee/attendance" variant="outline-primary">Check In / Out Attendance</Button>
              <Button as={Link} to="/employee/leaves" variant="outline-success">Apply for Leave</Button>
              <Button as={Link} to="/my-training" variant="outline-info">View Assigned Trainings</Button>
              <Button as={Link} to="/employee/performance" variant="outline-warning">My Performance Reviews</Button>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">Internal Career & Learning Opportunities</Card.Header>
            <Card.Body>
              <p>Explore open positions across departments and discover AI skill match recommendations.</p>
              <div className="d-grid gap-2">
                <Button as={Link} to="/careers" variant="primary">Internal Job Openings</Button>
                <Button as={Link} to="/career-recommendations" variant="outline-secondary">Explore Skill Match Recommendations</Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default EmployeeDashboard;
