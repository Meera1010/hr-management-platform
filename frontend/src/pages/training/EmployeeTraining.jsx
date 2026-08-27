import React, { useState, useEffect } from 'react';
import { Container, Table, Card, Button, Badge, Spinner, Alert, Modal, Form } from 'react-bootstrap';
import { getMyTrainings, updateTrainingAssignment } from '../../services/api';

const EmployeeTraining = () => {
  const [trainings, setTrainings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Completion modal
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [feedback, setFeedback] = useState('');

  useEffect(() => {
    fetchMyTrainings();
  }, []);

  const fetchMyTrainings = async () => {
    try {
      setLoading(true);
      const res = await getMyTrainings();
      setTrainings(res.data || []);
    } catch (err) {
      setError(err.message || 'Error loading assigned trainings');
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = async (e) => {
    e.preventDefault();
    try {
      await updateTrainingAssignment(selectedAssignment.id, {
        status: 'Completed',
        feedback: feedback,
        score: 100.0
      });
      setShowModal(false);
      fetchMyTrainings();
    } catch (err) {
      alert(`Error updating training: ${err.message}`);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Completed': return 'success';
      case 'In Progress': return 'info';
      case 'Assigned': return 'warning';
      default: return 'danger';
    }
  };

  return (
    <Container className="py-4">
      <h2>My Training & Development</h2>
      <p className="text-muted">View your assigned corporate learning courses and complete requirements.</p>

      {error && <Alert variant="danger">{error}</Alert>}

      <Card className="shadow-sm">
        <Card.Body className="p-0">
          <Table responsive hover className="mb-0">
            <thead className="bg-light">
              <tr>
                <th>Assignment Code</th>
                <th>Course Title</th>
                <th>Category</th>
                <th>Assigned Date</th>
                <th>Due Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="7" className="text-center py-4"><Spinner animation="border" /></td></tr>
              ) : trainings.length === 0 ? (
                <tr><td colSpan="7" className="text-center py-4 text-muted">You have no training assignments.</td></tr>
              ) : (
                trainings.map(t => (
                  <tr key={t.id}>
                    <td><Badge bg="secondary">{t.assignment_code}</Badge></td>
                    <td className="fw-bold">{t.course_title}</td>
                    <td><Badge bg="info">{t.course_category}</Badge></td>
                    <td>{t.assigned_date}</td>
                    <td>{t.due_date || 'N/A'}</td>
                    <td><Badge bg={getStatusBadge(t.status)}>{t.status}</Badge></td>
                    <td>
                      {t.status !== 'Completed' && (
                        <Button
                          size="sm"
                          variant="success"
                          onClick={() => {
                            setSelectedAssignment(t);
                            setShowModal(true);
                          }}
                        >
                          Mark Completed
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

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Form onSubmit={handleComplete}>
          <Modal.Header closeButton>
            <Modal.Title>Complete Training: {selectedAssignment?.course_title}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Course Completion Feedback / Notes</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                placeholder="Share your learning experience..."
                value={feedback}
                onChange={e => setFeedback(e.target.value)}
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
            <Button type="submit" variant="success">Submit Completion</Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </Container>
  );
};

export default EmployeeTraining;
