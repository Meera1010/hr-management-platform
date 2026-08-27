import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, InputGroup, Badge, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { getJobs, searchJobs } from '../../services/api';

const CandidateJobs = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const res = await getJobs(); // the backend filters out non-Open jobs for candidates
      setJobs(res.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchTerm.trim()) {
      fetchJobs();
      return;
    }
    try {
      setLoading(true);
      const data = await searchJobs(searchTerm);
      setJobs(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="py-4">
      <div className="text-center mb-5">
        <h2 className="display-5 fw-bold">Open Opportunities</h2>
        <p className="lead text-muted">Find your next career move with us</p>
      </div>

      <Row className="justify-content-center mb-5">
        <Col md={8}>
          <Form onSubmit={handleSearch}>
            <InputGroup size="lg">
              <Form.Control
                type="text"
                placeholder="Search by title, location, or keyword..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <Button type="submit" variant="primary">Search</Button>
            </InputGroup>
          </Form>
        </Col>
      </Row>

      {error && <div className="alert alert-danger">{error}</div>}

      {loading ? (
        <div className="text-center py-5">
          <Spinner animation="border" variant="primary" />
        </div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-5">
          <h4 className="text-muted">No open jobs found at the moment.</h4>
        </div>
      ) : (
        <Row className="g-4">
          {jobs.map(job => (
            <Col md={6} lg={4} key={job.id}>
              <Card className="h-100 shadow-sm border-0 job-card">
                <Card.Body className="d-flex flex-column">
                  <div className="mb-2">
                    <Badge bg="light" text="dark" className="me-2 mb-2 border">
                      {job.department_name}
                    </Badge>
                    <Badge bg="light" text="dark" className="mb-2 border">
                      {job.employment_type || 'Full Time'}
                    </Badge>
                  </div>
                  <Card.Title className="fw-bold mb-1">{job.title}</Card.Title>
                  <Card.Subtitle className="mb-3 text-muted">
                    <i className="bi bi-geo-alt-fill me-1"></i> {job.location || 'Remote'}
                  </Card.Subtitle>
                  
                  <Card.Text className="text-secondary flex-grow-1" style={{ display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {job.description}
                  </Card.Text>
                  
                  <div className="mt-3 pt-3 border-top d-flex justify-content-between align-items-center">
                    <small className="text-muted">
                      {job.application_deadline ? `Apply by ${new Date(job.application_deadline).toLocaleDateString()}` : 'No deadline'}
                    </small>
                    <Button variant="outline-primary" size="sm" onClick={() => navigate(`/jobs/${job.id}`)}>
                      View Details
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </Container>
  );
};

export default CandidateJobs;
