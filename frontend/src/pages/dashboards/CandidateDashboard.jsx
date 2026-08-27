import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Spinner, Alert, Badge } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { getDashboardStats } from '../../services/api';

const CandidateDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const res = await getDashboardStats();
      setStats(res.metrics || {});
    } catch (err) {
      setError(err.message || 'Failed to load candidate portal');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Container className="py-5 text-center"><Spinner animation="border" /></Container>;

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2>Candidate Portal</h2>
          <p className="text-muted">Track your job applications, interview schedules, offers, and AI job recommendations.</p>
        </div>
        <div>
          <Button as={Link} to="/candidate/jobs" variant="primary" className="me-2">Browse Jobs</Button>
          <Button as={Link} to="/career-recommendations" variant="outline-success">AI Job Recommendations</Button>
        </div>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      <Row className="g-3 mb-4">
        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-primary text-white">
            <Card.Body>
              <h3>{stats.total || 0}</h3>
              <div>Total Applications</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-info text-white">
            <Card.Body>
              <h3>{stats.under_review || 0}</h3>
              <div>Under Review</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-success text-white">
            <Card.Body>
              <h3>{stats.shortlisted || 0}</h3>
              <div>Shortlisted</div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="text-center shadow-sm border-0 bg-warning text-dark">
            <Card.Body>
              <h3>{stats.rejected || 0}</h3>
              <div>Archived / Rejected</div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="g-4">
        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">My Career Dashboard</Card.Header>
            <Card.Body className="d-grid gap-2">
              <Button as={Link} to="/candidate/applications" variant="outline-primary">View My Applications</Button>
              <Button as={Link} to="/candidate/resumes" variant="outline-info">Manage My Resumes</Button>
              <Button as={Link} to="/candidate/interviews" variant="outline-success">My Scheduled Interviews</Button>
              <Button as={Link} to="/candidate/offers" variant="outline-warning">My Job Offer Letters</Button>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="shadow-sm border-0 h-100">
            <Card.Header className="bg-white fw-bold">AI Skill Matching & Profile</Card.Header>
            <Card.Body>
              <p>Let AI evaluate your resume skills against active job requirements to highlight top matching positions.</p>
              <div className="d-grid gap-2">
                <Button as={Link} to="/career-recommendations" variant="success">View Top AI Job Recommendations</Button>
                <Button as={Link} to="/candidate/matches" variant="outline-secondary">Job Matching Analysis</Button>
                <Button as={Link} to="/candidate/profile" variant="outline-primary">Update Profile & Skills</Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default CandidateDashboard;
