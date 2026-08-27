import React, { useState, useEffect } from 'react';
import { Container, Table, Card, Button, Modal, Form, Badge, Spinner, Alert, Row, Col } from 'react-bootstrap';
import { getTrainingCourses, createTrainingCourse, assignTraining, getEmployees } from '../../services/api';

const TrainingCourses = () => {
  const [courses, setCourses] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // New Course Modal
  const [showCourseModal, setShowCourseModal] = useState(false);
  const [newCourse, setNewCourse] = useState({ title: '', category: 'Technical', description: '', duration_hours: 2, instructor: '' });

  // Assign Modal
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [assignForm, setAssignForm] = useState({ employee_id: '', due_date: '' });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const coursesRes = await getTrainingCourses();
      setCourses(coursesRes.data || []);
      
      const empRes = await getEmployees();
      setEmployees(empRes.data || []);
    } catch (err) {
      setError(err.message || 'Error loading courses');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCourse = async (e) => {
    e.preventDefault();
    try {
      await createTrainingCourse(newCourse);
      setShowCourseModal(false);
      setNewCourse({ title: '', category: 'Technical', description: '', duration_hours: 2, instructor: '' });
      fetchData();
    } catch (err) {
      alert(`Error creating course: ${err.message}`);
    }
  };

  const handleAssignSubmit = async (e) => {
    e.preventDefault();
    try {
      await assignTraining({
        course_id: selectedCourse.id,
        employee_id: assignForm.employee_id,
        due_date: assignForm.due_date
      });
      setShowAssignModal(false);
      alert('Training course assigned successfully!');
    } catch (err) {
      alert(`Error assigning training: ${err.message}`);
    }
  };

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2>Training & Development Management</h2>
          <p className="text-muted">Manage employee training courses, skill development, and learning assignments.</p>
        </div>
        <Button variant="primary" onClick={() => setShowCourseModal(true)}>
          + Create New Course
        </Button>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      <Card className="shadow-sm">
        <Card.Body className="p-0">
          <Table responsive hover className="mb-0">
            <thead className="bg-light">
              <tr>
                <th>Code</th>
                <th>Title</th>
                <th>Category</th>
                <th>Duration</th>
                <th>Instructor</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="7" className="text-center py-4"><Spinner animation="border" /></td></tr>
              ) : courses.length === 0 ? (
                <tr><td colSpan="7" className="text-center py-4 text-muted">No training courses found.</td></tr>
              ) : (
                courses.map(c => (
                  <tr key={c.id}>
                    <td><Badge bg="secondary">{c.course_code}</Badge></td>
                    <td className="fw-bold">{c.title}</td>
                    <td><Badge bg="info">{c.category}</Badge></td>
                    <td>{c.duration_hours} Hours</td>
                    <td>{c.instructor || 'N/A'}</td>
                    <td><Badge bg={c.status === 'Active' ? 'success' : 'secondary'}>{c.status}</Badge></td>
                    <td>
                      <Button
                        size="sm"
                        variant="outline-primary"
                        onClick={() => {
                          setSelectedCourse(c);
                          setShowAssignModal(true);
                        }}
                      >
                        Assign to Staff
                      </Button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      {/* Create Course Modal */}
      <Modal show={showCourseModal} onHide={() => setShowCourseModal(false)}>
        <Form onSubmit={handleCreateCourse}>
          <Modal.Header closeButton>
            <Modal.Title>Create Training Course</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Course Title</Form.Label>
              <Form.Control required value={newCourse.title} onChange={e => setNewCourse({ ...newCourse, title: e.target.value })} />
            </Form.Group>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Category</Form.Label>
                  <Form.Select value={newCourse.category} onChange={e => setNewCourse({ ...newCourse, category: e.target.value })}>
                    <option value="Technical">Technical</option>
                    <option value="Compliance">Compliance</option>
                    <option value="Soft Skills">Soft Skills</option>
                    <option value="Management">Management</option>
                    <option value="Safety">Safety</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Duration (Hours)</Form.Label>
                  <Form.Control type="number" min="1" value={newCourse.duration_hours} onChange={e => setNewCourse({ ...newCourse, duration_hours: e.target.value })} />
                </Form.Group>
              </Col>
            </Row>
            <Form.Group className="mb-3">
              <Form.Label>Instructor / Trainer</Form.Label>
              <Form.Control value={newCourse.instructor} onChange={e => setNewCourse({ ...newCourse, instructor: e.target.value })} />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control as="textarea" rows={3} value={newCourse.description} onChange={e => setNewCourse({ ...newCourse, description: e.target.value })} />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowCourseModal(false)}>Cancel</Button>
            <Button type="submit" variant="primary">Create Course</Button>
          </Modal.Footer>
        </Form>
      </Modal>

      {/* Assign Training Modal */}
      <Modal show={showAssignModal} onHide={() => setShowAssignModal(false)}>
        <Form onSubmit={handleAssignSubmit}>
          <Modal.Header closeButton>
            <Modal.Title>Assign Training: {selectedCourse?.title}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Select Employee</Form.Label>
              <Form.Select required value={assignForm.employee_id} onChange={e => setAssignForm({ ...assignForm, employee_id: e.target.value })}>
                <option value="">-- Choose Employee --</option>
                {employees.map(emp => (
                  <option key={emp.id} value={emp.id}>
                    {emp.first_name} {emp.last_name} ({emp.employee_code} - {emp.department_name})
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Due Date</Form.Label>
              <Form.Control type="date" required value={assignForm.due_date} onChange={e => setAssignForm({ ...assignForm, due_date: e.target.value })} />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowAssignModal(false)}>Cancel</Button>
            <Button type="submit" variant="primary">Assign Course</Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </Container>
  );
};

export default TrainingCourses;
