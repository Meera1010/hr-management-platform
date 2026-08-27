import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Spinner, Alert, ProgressBar } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { getDashboardStats } from '../../services/api';

const HRDashboard = () => {
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
      setError(err.message || 'Failed to load HR dashboard metrics');
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
          <h2>HR & Executive Dashboard</h2>
          <p className="text-muted">Workforce analytics, department management, and quick operational controls.</p>
        </div>
        <div>
          <Button as={Link} to="/analytics" variant="primary" className="me-2">Analytics Overview</Button>
          <Button as={Link} to="/reports" variant="outline-secondary">Reports Generator</Button>
        </div>
      </div>

      <Row className="g-3 mb-4">
        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-primary text-white">
            <Card.Body>
              <h3>{stats.total_employees || 0}</h3>
              <div>Total Employees</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-success text-white">
            <Card.Body>
              <h3>{stats.active_employees || 0}</h3>
              <div>Active Staff</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-warning text-dark">
            <Card.Body>
              <h3>{stats.pending_leaves || 0}</h3>
              <div>Pending Leaves</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-info text-white">
            <Card.Body>
              <h3>{stats.open_jobs || 0}</h3>
              <div>Open Positions</div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="g-4">
        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">Quick Management Actions</Card.Header>
            <Card.Body className="d-grid gap-2">
              <Button as={Link} to="/hr/employees/new" variant="outline-primary">Add New Employee</Button>
              <Button as={Link} to="/jobs/new" variant="outline-success">Create Job Opening</Button>
              <Button as={Link} to="/hr/leaves" variant="outline-warning">Review Pending Leaves</Button>
              <Button as={Link} to="/training" variant="outline-info">Manage Training Courses</Button>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">HR System Modules</Card.Header>
            <Card.Body>
              <Row className="g-2 text-center">
                <Col sm={6}>
                  <Card className="p-3 border">
                    <h6>Departments</h6>
                    <Button as={Link} to="/hr/departments" size="sm" variant="secondary">View ({stats.departments_count || 0})</Button>
                  </Card>
                </Col>
                <Col sm={6}>
                  <Card className="p-3 border">
                    <h6>Applications</h6>
                    <Button as={Link} to="/applications" size="sm" variant="secondary">Review ({stats.total_applications || 0})</Button>
                  </Card>
                </Col>
                <Col sm={6} className="mt-3">
                  <Card className="p-3 border">
                    <h6>Offers Package</h6>
                    <Button as={Link} to="/hr/offers" size="sm" variant="secondary">Manage Offers</Button>
                  </Card>
                </Col>
                <Col sm={6} className="mt-3">
                  <Card className="p-3 border">
                    <h6>Performance</h6>
                    <Button as={Link} to="/hr/performance" size="sm" variant="secondary">Reviews</Button>
                  </Card>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default HRDashboard;
