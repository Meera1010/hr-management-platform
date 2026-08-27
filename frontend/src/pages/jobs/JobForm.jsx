import React, { useState, useEffect } from 'react';
import { Container, Card, Form, Button, Row, Col, Alert } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { getJob, createJob, updateJob, api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const JobForm = () => {
  const { id } = useParams();
  const isEditMode = !!id;
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [departments, setDepartments] = useState([]);
  const [formData, setFormData] = useState({
    job_code: '',
    title: '',
    department_id: '',
    description: '',
    responsibilities: '',
    required_skills: '',
    preferred_skills: '',
    experience_required: '',
    education_required: '',
    location: '',
    employment_type: 'Full Time',
    salary_range: '',
    application_deadline: '',
    status: 'Draft'
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Only Admin, HR, Recruiter can access this page
    if (!['Admin', 'HR', 'Recruiter'].includes(user?.role)) {
      navigate('/jobs');
      return;
    }
    
    fetchDepartments();
    
    if (isEditMode) {
      fetchJobDetails();
    }
  }, [id, user, navigate]);

  const fetchDepartments = async () => {
    try {
      // Assuming GET /api/departments/ exists
      const res = await fetch('http://localhost:5001/api/departments/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await res.json();
      if (data.success) {
        setDepartments(data.data);
      }
    } catch (err) {
      console.error("Failed to load departments:", err);
    }
  };

  const fetchJobDetails = async () => {
    try {
      setLoading(true);
      const data = await getJob(id);
      
      // format date if needed
      let deadline = '';
      if (data.application_deadline) {
        deadline = new Date(data.application_deadline).toISOString().split('T')[0];
      }
      
      setFormData({
        job_code: data.job_code || '',
        title: data.title || '',
        department_id: data.department_id || '',
        description: data.description || '',
        responsibilities: data.responsibilities || '',
        required_skills: data.required_skills || '',
        preferred_skills: data.preferred_skills || '',
        experience_required: data.experience_required || '',
        education_required: data.education_required || '',
        location: data.location || '',
        employment_type: data.employment_type || 'Full Time',
        salary_range: data.salary_range || '',
        application_deadline: deadline,
        status: data.status || 'Draft'
      });
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      
      // Format deadline or set to null if empty
      const payload = { ...formData };
      if (!payload.application_deadline) {
        delete payload.application_deadline;
      }
      
      if (isEditMode) {
        await updateJob(id, payload);
      } else {
        await createJob(payload);
      }
      navigate('/jobs');
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>{isEditMode ? 'Edit Job' : 'Create Job'}</h2>
        <Button variant="secondary" onClick={() => navigate('/jobs')}>
          Back to Jobs
        </Button>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      <Card>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Row className="mb-3">
              <Form.Group as={Col} md={6}>
                <Form.Label>Job Code *</Form.Label>
                <Form.Control
                  type="text"
                  name="job_code"
                  value={formData.job_code}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
              
              <Form.Group as={Col} md={6}>
                <Form.Label>Job Title *</Form.Label>
                <Form.Control
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Row>

            <Row className="mb-3">
              <Form.Group as={Col} md={6}>
                <Form.Label>Department *</Form.Label>
                <Form.Select
                  name="department_id"
                  value={formData.department_id}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Department</option>
                  {departments.map(d => (
                    <option key={d.id} value={d.id}>{d.name}</option>
                  ))}
                </Form.Select>
              </Form.Group>
              
              <Form.Group as={Col} md={6}>
                <Form.Label>Employment Type</Form.Label>
                <Form.Select
                  name="employment_type"
                  value={formData.employment_type}
                  onChange={handleChange}
                >
                  <option value="Full Time">Full Time</option>
                  <option value="Part Time">Part Time</option>
                  <option value="Contract">Contract</option>
                  <option value="Internship">Internship</option>
                </Form.Select>
              </Form.Group>
            </Row>

            <Row className="mb-3">
              <Form.Group as={Col} md={6}>
                <Form.Label>Location</Form.Label>
                <Form.Control
                  type="text"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                />
              </Form.Group>
              
              <Form.Group as={Col} md={6}>
                <Form.Label>Status</Form.Label>
                <Form.Select
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                >
                  <option value="Draft">Draft</option>
                  <option value="Open">Open</option>
                  <option value="Closed">Closed</option>
                  <option value="Archived">Archived</option>
                </Form.Select>
              </Form.Group>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Description *</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                name="description"
                value={formData.description}
                onChange={handleChange}
                required
              />
            </Form.Group>
            
            <Form.Group className="mb-3">
              <Form.Label>Responsibilities</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                name="responsibilities"
                value={formData.responsibilities}
                onChange={handleChange}
              />
            </Form.Group>

            <Row className="mb-3">
              <Form.Group as={Col} md={6}>
                <Form.Label>Required Skills</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={2}
                  name="required_skills"
                  value={formData.required_skills}
                  onChange={handleChange}
                />
              </Form.Group>
              
              <Form.Group as={Col} md={6}>
                <Form.Label>Preferred Skills</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={2}
                  name="preferred_skills"
                  value={formData.preferred_skills}
                  onChange={handleChange}
                />
              </Form.Group>
            </Row>

            <Row className="mb-3">
              <Form.Group as={Col} md={4}>
                <Form.Label>Experience Required</Form.Label>
                <Form.Control
                  type="text"
                  name="experience_required"
                  value={formData.experience_required}
                  onChange={handleChange}
                />
              </Form.Group>
              
              <Form.Group as={Col} md={4}>
                <Form.Label>Education Required</Form.Label>
                <Form.Control
                  type="text"
                  name="education_required"
                  value={formData.education_required}
                  onChange={handleChange}
                />
              </Form.Group>
              
              <Form.Group as={Col} md={4}>
                <Form.Label>Application Deadline</Form.Label>
                <Form.Control
                  type="date"
                  name="application_deadline"
                  value={formData.application_deadline}
                  onChange={handleChange}
                />
              </Form.Group>
            </Row>

            <Form.Group className="mb-4">
              <Form.Label>Salary Range</Form.Label>
              <Form.Control
                type="text"
                name="salary_range"
                value={formData.salary_range}
                onChange={handleChange}
              />
            </Form.Group>

            <div className="d-grid">
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? 'Saving...' : 'Save Job'}
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default JobForm;
