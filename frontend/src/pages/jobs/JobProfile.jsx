import React, { useState, useEffect } from 'react';
import { Container, Card, Row, Col, Badge, Button, Spinner } from 'react-bootstrap';
import { useParams, Link } from 'react-router-dom';
import { getJob } from '../../services/api';

const JobProfile = () => {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchJob();
  }, [id]);

  const fetchJob = async () => {
    try {
      setLoading(true);
      const data = await getJob(id);
      setJob(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Open': return 'success';
      case 'Closed': return 'secondary';
      case 'Draft': return 'warning';
      case 'Archived': return 'dark';
      default: return 'primary';
    }
  };

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <Spinner animation="border" />
        <p className="mt-3">Loading job details...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="py-5 text-center">
        <div className="alert alert-danger">{error}</div>
        <Button as={Link} to="/jobs" variant="primary">Back to Jobs</Button>
      </Container>
    );
  }

  if (!job) return null;

  return (
    <Container className="py-4">
      <div className="mb-4">
        <Button as={Link} to="/jobs" variant="outline-secondary" className="mb-3">
          &larr; Back to Jobs
        </Button>
        <div className="d-flex justify-content-between align-items-start">
          <div>
            <h2>{job.title}</h2>
            <h5 className="text-muted mb-3">{job.job_code} • {job.department_name}</h5>
          </div>
          <Badge bg={getStatusBadge(job.status)} className="fs-6 p-2">
            {job.status}
          </Badge>
        </div>
      </div>

      <Row>
        <Col md={8}>
          <Card className="mb-4">
            <Card.Body>
              <h5 className="card-title">Job Description</h5>
              <p style={{ whiteSpace: 'pre-wrap' }}>{job.description}</p>
              
              {job.responsibilities && (
                <>
                  <h5 className="card-title mt-4">Responsibilities</h5>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{job.responsibilities}</p>
                </>
              )}
              
              {job.required_skills && (
                <>
                  <h5 className="card-title mt-4">Required Skills</h5>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{job.required_skills}</p>
                </>
              )}
              
              {job.preferred_skills && (
                <>
                  <h5 className="card-title mt-4">Preferred Skills</h5>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{job.preferred_skills}</p>
                </>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="mb-4">
            <Card.Header className="bg-light">
              <h5 className="mb-0">Key Details</h5>
            </Card.Header>
            <Card.Body>
              <div className="mb-3">
                <strong>Location:</strong>
                <div>{job.location || 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>Employment Type:</strong>
                <div>{job.employment_type || 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>Experience Required:</strong>
                <div>{job.experience_required || 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>Education Required:</strong>
                <div>{job.education_required || 'Not specified'}</div>
              </div>
              <div className="mb-3">
                <strong>Salary Range:</strong>
                <div>{job.salary_range || 'Not specified'}</div>
              </div>
              {job.application_deadline && (
                <div className="mb-3">
                  <strong>Application Deadline:</strong>
                  <div>{new Date(job.application_deadline).toLocaleDateString()}</div>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default JobProfile;
