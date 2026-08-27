import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, Table, Badge, InputGroup } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { getJobs, searchJobs, changeJobStatus, archiveJob } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const Jobs = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  
  const canManageJobs = ['Admin', 'HR', 'Recruiter'].includes(user?.role);
  const canArchiveJobs = ['Admin', 'HR'].includes(user?.role);

  useEffect(() => {
    fetchJobs();
  }, [statusFilter, typeFilter]);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const params = {};
      if (statusFilter) params.status = statusFilter;
      if (typeFilter) params.employment_type = typeFilter;
      
      const res = await getJobs(params);
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

  const handleStatusChange = async (id, newStatus) => {
    try {
      await changeJobStatus(id, newStatus);
      fetchJobs();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleArchive = async (id) => {
    if (window.confirm('Are you sure you want to archive this job?')) {
      try {
        await archiveJob(id);
        fetchJobs();
      } catch (err) {
        alert(`Error: ${err.message}`);
      }
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

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Jobs</h2>
        {canManageJobs && (
          <Button as={Link} to="/jobs/new" variant="primary">
            Create Job
          </Button>
        )}
      </div>

      <Card className="mb-4">
        <Card.Body>
          <Form onSubmit={handleSearch}>
            <Row className="g-3">
              <Col md={5}>
                <InputGroup>
                  <Form.Control
                    type="text"
                    placeholder="Search by title, code, or location..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                  <Button type="submit" variant="outline-secondary">Search</Button>
                </InputGroup>
              </Col>
              
              {canManageJobs && (
                <Col md={3}>
                  <Form.Select 
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                  >
                    <option value="">All Statuses</option>
                    <option value="Open">Open</option>
                    <option value="Closed">Closed</option>
                    <option value="Draft">Draft</option>
                    <option value="Archived">Archived</option>
                  </Form.Select>
                </Col>
              )}

              <Col md={canManageJobs ? 4 : 7}>
                <Form.Select
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                >
                  <option value="">All Types</option>
                  <option value="Full Time">Full Time</option>
                  <option value="Part Time">Part Time</option>
                  <option value="Contract">Contract</option>
                  <option value="Internship">Internship</option>
                </Form.Select>
              </Col>
            </Row>
          </Form>
        </Card.Body>
      </Card>

      {error && <div className="alert alert-danger">{error}</div>}

      <Card>
        <Card.Body className="p-0">
          <Table responsive hover className="mb-0">
            <thead className="bg-light">
              <tr>
                <th>Job Code</th>
                <th>Title</th>
                <th>Department</th>
                <th>Location</th>
                <th>Type</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="7" className="text-center py-4">Loading...</td>
                </tr>
              ) : jobs.length === 0 ? (
                <tr>
                  <td colSpan="7" className="text-center py-4">No jobs found.</td>
                </tr>
              ) : (
                jobs.map(job => (
                  <tr key={job.id}>
                    <td>{job.job_code}</td>
                    <td>{job.title}</td>
                    <td>{job.department_name}</td>
                    <td>{job.location || '-'}</td>
                    <td>{job.employment_type || '-'}</td>
                    <td>
                      <Badge bg={getStatusBadge(job.status)}>{job.status}</Badge>
                    </td>
                    <td>
                      <Button 
                        variant="info" 
                        size="sm" 
                        className="me-2"
                        onClick={() => navigate(`/jobs/${job.id}`)}
                      >
                        View
                      </Button>

                      {canManageJobs && (
                        <Button 
                          variant="outline-info" 
                          size="sm" 
                          className="me-2"
                          onClick={() => navigate(`/recruiter/jobs/${job.id}/matches`)}
                        >
                          Matches
                        </Button>
                      )}
                      
                      {canManageJobs && job.status !== 'Archived' && (
                        <>
                          <Button 
                            variant="outline-primary" 
                            size="sm" 
                            className="me-2"
                            onClick={() => navigate(`/jobs/${job.id}/edit`)}
                          >
                            Edit
                          </Button>
                          
                          {job.status === 'Draft' && (
                            <Button 
                              variant="outline-success" 
                              size="sm" 
                              className="me-2"
                              onClick={() => handleStatusChange(job.id, 'Open')}
                            >
                              Publish
                            </Button>
                          )}
                          
                          {job.status === 'Open' && (
                            <Button 
                              variant="outline-secondary" 
                              size="sm" 
                              className="me-2"
                              onClick={() => handleStatusChange(job.id, 'Closed')}
                            >
                              Close
                            </Button>
                          )}
                        </>
                      )}

                      {canArchiveJobs && job.status !== 'Archived' && (
                        <Button 
                          variant="outline-danger" 
                          size="sm"
                          onClick={() => handleArchive(job.id)}
                        >
                          Archive
                        </Button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Jobs;
