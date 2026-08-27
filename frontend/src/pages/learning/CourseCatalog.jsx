import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Badge, Button, Spinner, Alert } from 'react-bootstrap';
import learningApi from '../../services/learningApi';

export default function CourseCatalog() {
  const [courses, setCourses] = useState([]);
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [cRes, eRes] = await Promise.all([
        learningApi.getCourses(),
        learningApi.getEnrollments()
      ]);
      setCourses(cRes.data.courses || []);
      setEnrollments(eRes.data.enrollments || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch courses');
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async (courseId) => {
    try {
      await learningApi.enrollCourse({ course_id: courseId });
      fetchData();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to enroll in course');
    }
  };

  if (loading) return <div className="text-center py-5"><Spinner animation="border" variant="primary" /></div>;

  return (
    <Container fluid className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">Learning Experience Platform (LXP)</h2>
          <p className="text-muted">Explore enterprise courses, earn certificates, and close skill gaps.</p>
        </div>
      </div>

      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

      <Row className="g-4">
        {courses.map(course => {
          const isEnrolled = enrollments.some(e => e.course_id === course.id);

          return (
            <Col key={course.id} md={4}>
              <Card className="h-100 border-0 shadow-sm">
                <Card.Body className="d-flex flex-column">
                  <div className="d-flex justify-content-between align-items-start mb-2">
                    <Badge bg="primary">{course.category}</Badge>
                    <Badge bg="secondary">{course.level}</Badge>
                  </div>
                  <Card.Title className="fw-bold text-dark">{course.title}</Card.Title>
                  <Card.Text className="text-muted flex-grow-1">{course.description}</Card.Text>
                  <div className="d-flex justify-content-between align-items-center mt-3 pt-3 border-top">
                    <small className="text-muted"><i className="bi bi-clock me-1"></i>{course.duration_hours} Hours</small>
                    {isEnrolled ? (
                      <Badge bg="success" className="py-2 px-3">Enrolled</Badge>
                    ) : (
                      <Button variant="outline-primary" size="sm" onClick={() => handleEnroll(course.id)}>
                        Enroll Now
                      </Button>
                    )}
                  </div>
                </Card.Body>
              </Card>
            </Col>
          );
        })}
        {courses.length === 0 && <Col><p className="text-muted text-center py-5">No courses published in catalog.</p></Col>}
      </Row>
    </Container>
  );
}
