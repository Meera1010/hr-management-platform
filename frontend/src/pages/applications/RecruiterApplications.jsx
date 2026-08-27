import React, { useState, useEffect } from 'react';
import { Table, Container, Badge, Button, Form, Row, Col, Spinner } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { getApplications } from '../../services/api';

const RecruiterApplications = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    fetchApplications();
  }, [search, statusFilter]);

  const fetchApplications = async () => {
    try {
      const data = await getApplications({ search, status: statusFilter });
      setApplications(data.applications);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const map = {
      'Submitted': 'primary',
      'Under Review': 'info',
      'Shortlisted': 'success',
      'Rejected': 'danger',
      'Withdrawn': 'secondary',
      'Selected': 'success'
    };
    return <Badge bg={map[status] || 'secondary'}>{status}</Badge>;
  };

  return (
    <Container className="mt-4">
      <h2>Manage Applications</h2>
      
      <Row className="mb-3">
        <Col md={6}>
          <Form.Control 
            type="text" 
            placeholder="Search by candidate, job, or code..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </Col>
        <Col md={6}>
          <Form.Select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="">All Statuses</option>
            <option value="Submitted">Submitted</option>
            <option value="Under Review">Under Review</option>
            <option value="Shortlisted">Shortlisted</option>
            <option value="Rejected">Rejected</option>
            <option value="Withdrawn">Withdrawn</option>
            <option value="Selected">Selected</option>
          </Form.Select>
        </Col>
      </Row>

      {loading ? (
        <Spinner animation="border" />
      ) : (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>App Code</th>
              <th>Candidate</th>
              <th>Job Title</th>
              <th>Applied Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {applications.length === 0 ? (
              <tr><td colSpan="6" className="text-center">No applications found.</td></tr>
            ) : (
              applications.map(app => (
                <tr key={app.id}>
                  <td>{app.application_code}</td>
                  <td>{app.candidate_name}</td>
                  <td>{app.job_title}</td>
                  <td>{new Date(app.applied_date).toLocaleDateString()}</td>
                  <td>{getStatusBadge(app.status)}</td>
                  <td>
                    <Button variant="info" size="sm" as={Link} to={`/applications/${app.id}`}>
                      View/Update
                    </Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </Table>
      )}
    </Container>
  );
};

export default RecruiterApplications;
