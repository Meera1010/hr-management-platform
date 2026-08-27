import React, { useState, useEffect } from 'react';
import { Table, Container, Badge, Button, Spinner } from 'react-bootstrap';
import { getApplications, withdrawApplication } from '../../services/api';

const CandidateApplications = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const data = await getApplications({});
      setApplications(data.applications);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleWithdraw = async (id) => {
    if (window.confirm("Are you sure you want to withdraw this application?")) {
      try {
        await withdrawApplication(id);
        fetchApplications();
      } catch (err) {
        alert(err.message || 'Error withdrawing application');
      }
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

  if (loading) return <Container className="mt-4"><Spinner animation="border" /></Container>;

  return (
    <Container className="mt-4">
      <h2>My Applications</h2>
      {applications.length === 0 ? (
        <p>You have not applied to any jobs yet.</p>
      ) : (
        <Table striped bordered hover className="mt-3">
          <thead>
            <tr>
              <th>Application Code</th>
              <th>Job Title</th>
              <th>Department</th>
              <th>Applied Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {applications.map(app => (
              <tr key={app.id}>
                <td>{app.application_code}</td>
                <td>{app.job_title}</td>
                <td>{app.department_name}</td>
                <td>{new Date(app.applied_date).toLocaleDateString()}</td>
                <td>{getStatusBadge(app.status)}</td>
                <td>
                  {!['Rejected', 'Withdrawn', 'Selected'].includes(app.status) && (
                    <Button variant="danger" size="sm" onClick={() => handleWithdraw(app.id)}>
                      Withdraw
                    </Button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  );
};

export default CandidateApplications;
