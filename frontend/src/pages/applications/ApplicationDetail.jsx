import React, { useState, useEffect } from 'react';
import { Container, Card, Badge, Form, Button, Spinner, Alert } from 'react-bootstrap';
import { useParams, useNavigate } from 'react-router-dom';
import { getApplication, updateApplicationStatus } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const ApplicationDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [app, setApp] = useState(null);
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState('');
  const [notes, setNotes] = useState('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    fetchApplication();
  }, [id]);

  const fetchApplication = async () => {
    try {
      const data = await getApplication(id);
      setApp(data.application);
      setStatus(data.application.status);
      setNotes(data.application.recruiter_notes || '');
    } catch (err) {
      setError(err.message || 'Error fetching application');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSuccess(false);
    setError(null);
    try {
      const data = await updateApplicationStatus(id, { status, recruiter_notes: notes });
      setApp(data.application);
      setSuccess(true);
    } catch (err) {
      setError(err.message || 'Error updating application');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Container className="mt-4"><Spinner animation="border" /></Container>;
  if (!app) return <Container className="mt-4"><Alert variant="danger">{error}</Alert></Container>;

  const isRecruiter = ['Admin', 'HR', 'Recruiter'].includes(user.role);

  return (
    <Container className="mt-4">
      <Button variant="outline-secondary" className="mb-3" onClick={() => navigate(-1)}>
        &larr; Back
      </Button>

      <h2>Application {app.application_code}</h2>
      
      <Card className="mb-4 shadow-sm">
        <Card.Body>
          <Card.Title>Details</Card.Title>
          <p><strong>Job:</strong> {app.job_title} ({app.department_name})</p>
          <p><strong>Candidate:</strong> {app.candidate_name}</p>
          <p><strong>Applied:</strong> {new Date(app.applied_date).toLocaleString()}</p>
          <p><strong>Current Status:</strong> <Badge bg="primary">{app.status}</Badge></p>
          
          <h5 className="mt-4">Cover Letter</h5>
          <div className="p-3 bg-light rounded" style={{ whiteSpace: 'pre-wrap' }}>
            {app.cover_letter || 'No cover letter provided.'}
          </div>
        </Card.Body>
      </Card>

      {isRecruiter && (
        <Card className="shadow-sm">
          <Card.Body>
            <Card.Title>Recruiter Actions</Card.Title>
            {error && <Alert variant="danger">{error}</Alert>}
            {success && <Alert variant="success">Application updated successfully.</Alert>}
            
            <Form onSubmit={handleUpdate}>
              <Form.Group className="mb-3">
                <Form.Label>Status</Form.Label>
                <Form.Select value={status} onChange={(e) => setStatus(e.target.value)}>
                  <option value="Submitted">Submitted</option>
                  <option value="Under Review">Under Review</option>
                  <option value="Shortlisted">Shortlisted</option>
                  <option value="Rejected">Rejected</option>
                  <option value="Withdrawn">Withdrawn</option>
                  <option value="Selected">Selected</option>
                </Form.Select>
              </Form.Group>
              
              <Form.Group className="mb-3">
                <Form.Label>Recruiter Notes (internal)</Form.Label>
                <Form.Control 
                  as="textarea" 
                  rows={3} 
                  value={notes} 
                  onChange={(e) => setNotes(e.target.value)} 
                  placeholder="Private notes for HR team..."
                />
              </Form.Group>
              
              <Button type="submit" variant="primary" disabled={saving}>
                {saving ? 'Saving...' : 'Update Application'}
              </Button>
            </Form>
          </Card.Body>
        </Card>
      )}

    </Container>
  );
};

export default ApplicationDetail;
