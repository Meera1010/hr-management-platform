import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Spinner, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { getDashboardStats } from '../../services/api';

const RecruiterDashboard = () => {
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
      setError(err.message || 'Failed to load recruiter stats');
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
          <h2>Recruiter Dashboard</h2>
          <p className="text-muted">Candidate pipeline tracking, AI ranking, interview scheduling & offer delivery.</p>
        </div>
        <div>
          <Button as={Link} to="/recruiter/rankings" variant="primary" className="me-2">AI Candidate Rankings</Button>
          <Button as={Link} to="/recruiter/interviews/schedule" variant="outline-success">Schedule Interview</Button>
        </div>
      </div>

      <Row className="g-3 mb-4">
        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-primary text-white">
            <Card.Body>
              <h3>{stats.active_jobs || 0}</h3>
              <div>Active Job Postings</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-info text-white">
            <Card.Body>
              <h3>{stats.total_candidates || 0}</h3>
              <div>Candidate Pool</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-warning text-dark">
            <Card.Body>
              <h3>{stats.total_applications || 0}</h3>
              <div>Total Applications</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-success text-white">
            <Card.Body>
              <h3>{stats.upcoming_interviews || 0}</h3>
              <div>Scheduled Interviews</div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="g-4">
        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">Recruitment Pipeline Shortcuts</Card.Header>
            <Card.Body className="d-grid gap-2">
              <Button as={Link} to="/jobs" variant="outline-primary">Manage Open Jobs</Button>
              <Button as={Link} to="/hr/candidates" variant="outline-secondary">Search Candidates</Button>
              <Button as={Link} to="/applications" variant="outline-warning">Review Applications</Button>
              <Button as={Link} to="/recruiter/resumes" variant="outline-info">Parse & View Resumes</Button>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">Interview & Offer Management</Card.Header>
            <Card.Body className="d-grid gap-2">
              <Button as={Link} to="/recruiter/interviews" variant="outline-success">View Scheduled Interviews</Button>
              <Button as={Link} to="/recruiter/rankings" variant="outline-dark">AI Candidate Matching & Ranking</Button>
              <Button as={Link} to="/hr/offers" variant="outline-primary">View Offer Packages</Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default RecruiterDashboard;
