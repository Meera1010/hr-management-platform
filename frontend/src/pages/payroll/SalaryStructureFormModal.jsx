import React, { useState } from 'react';
import { Modal, Form, Button, Row, Col, Alert } from 'react-bootstrap';
import payrollApi from '../../services/payrollApi';

export default function SalaryStructureFormModal({ show, onHide, onSuccess }) {
  const [formData, setFormData] = useState({
    title: '',
    code: '',
    description: '',
    base_salary_pct: 40.0,
    hra_pct: 20.0,
    special_allowance_pct: 20.0,
    pf_employer_pct: 12.0,
    pf_employee_pct: 12.0,
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name.endsWith('_pct') ? parseFloat(value) || 0 : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const totalPct =
      formData.base_salary_pct +
      formData.hra_pct +
      formData.special_allowance_pct;

    if (totalPct > 100) {
      setError(`Total allowance allocation (${totalPct}%) exceeds 100% of CTC.`);
      return;
    }

    setLoading(true);
    try {
      await payrollApi.createStructure(formData);
      onSuccess();
      onHide();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create salary structure');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" backdrop="static">
      <Form onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title className="fw-bold">
            <i className="bi bi-diagram-3-fill me-2 text-primary"></i>
            Create New Salary Structure Band
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

          <Row className="mb-3">
            <Col md={6}>
              <Form.Group>
                <Form.Label className="fw-semibold">Structure Band Title</Form.Label>
                <Form.Control
                  type="text"
                  name="title"
                  placeholder="e.g. Senior Engineering Band - Grade 4"
                  value={formData.title}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label className="fw-semibold">Structure Code</Form.Label>
                <Form.Control
                  type="text"
                  name="code"
                  placeholder="e.g. ENG-BAND-G4"
                  value={formData.code}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <Form.Group className="mb-3">
            <Form.Label className="fw-semibold">Description</Form.Label>
            <Form.Control
              as="textarea"
              rows={2}
              name="description"
              placeholder="Provide context regarding eligible designations and salary bands..."
              value={formData.description}
              onChange={handleChange}
            />
          </Form.Group>

          <h6 className="fw-bold border-bottom pb-2 mb-3 mt-4 text-secondary">
            Allowance Percentage Breakdown (% of Annual CTC)
          </h6>

          <Row className="mb-3">
            <Col md={4}>
              <Form.Group>
                <Form.Label>Basic Pay (%)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  name="base_salary_pct"
                  value={formData.base_salary_pct}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label>House Rent Allowance (%)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  name="hra_pct"
                  value={formData.hra_pct}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Special Allowance (%)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  name="special_allowance_pct"
                  value={formData.special_allowance_pct}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <h6 className="fw-bold border-bottom pb-2 mb-3 mt-4 text-secondary">
            Statutory Deductions (% of Basic Pay)
          </h6>

          <Row className="mb-3">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Provident Fund (Employer Contribution %)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  name="pf_employer_pct"
                  value={formData.pf_employer_pct}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Provident Fund (Employee Contribution %)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  name="pf_employee_pct"
                  value={formData.pf_employee_pct}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
          </Row>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={onHide}>
            Cancel
          </Button>
          <Button variant="primary" type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Save Salary Structure'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
}
