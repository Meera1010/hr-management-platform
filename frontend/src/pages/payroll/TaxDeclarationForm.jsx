import React, { useState, useEffect } from 'react';
import { Container, Card, Form, Button, Row, Col, Alert, Table, Badge } from 'react-bootstrap';
import payrollApi from '../../services/payrollApi';

export default function TaxDeclarationForm() {
  const [declarations, setDeclarations] = useState([]);
  const [formData, setFormData] = useState({
    financial_year: '2026-2027',
    regime: 'New',
    sec_80c_ppf_elss: 150000.0,
    sec_80d_health_insurance: 25000.0,
    hra_rent_paid_annual: 180000.0,
    home_loan_interest_sec24: 0.0,
    other_exemptions: 0.0,
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDeclarations();
  }, []);

  const fetchDeclarations = async () => {
    try {
      const res = await payrollApi.getTaxDeclarations();
      setDeclarations(res.data.declarations || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'regime' || name === 'financial_year' ? value : parseFloat(value) || 0,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(null);
    setError(null);

    try {
      await payrollApi.submitTaxDeclaration(formData);
      setSuccess('Annual tax declaration submitted successfully.');
      fetchDeclarations();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit tax declaration');
    } finally {
      setLoading(false);
    }
  };

  const totalDeclared =
    formData.sec_80c_ppf_elss +
    formData.sec_80d_health_insurance +
    formData.hra_rent_paid_annual +
    formData.home_loan_interest_sec24 +
    formData.other_exemptions;

  return (
    <Container fluid className="py-4">
      <div className="mb-4">
        <h2 className="fw-bold mb-1">Annual Income Tax Investment Declaration</h2>
        <p className="text-muted">
          Submit investment proofs for Old or New Tax Regime calculations under FY 2026-2027.
        </p>
      </div>

      {success && <Alert variant="success" dismissible onClose={() => setSuccess(null)}>{success}</Alert>}
      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

      <Row className="g-4">
        <Col md={8}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Tax Declaration Worksheet</h5>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Row className="mb-3">
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold">Financial Year</Form.Label>
                      <Form.Select
                        name="financial_year"
                        value={formData.financial_year}
                        onChange={handleChange}
                      >
                        <option value="2026-2027">2026-2027</option>
                        <option value="2025-2026">2025-2026</option>
                      </Form.Select>
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold">Tax Regime Preference</Form.Label>
                      <Form.Select
                        name="regime"
                        value={formData.regime}
                        onChange={handleChange}
                      >
                        <option value="New">New Tax Regime (Lower Slabs, No Deductions)</option>
                        <option value="Old">Old Tax Regime (With 80C, 80D, HRA Exemptions)</option>
                      </Form.Select>
                    </Form.Group>
                  </Col>
                </Row>

                {formData.regime === 'Old' && (
                  <>
                    <h6 className="fw-bold border-bottom pb-2 mb-3 mt-4 text-primary">
                      Section 80C Deductions (Max Limit: ₹1,50,000)
                    </h6>
                    <Form.Group className="mb-3">
                      <Form.Label>PPF, ELSS Mutual Funds, EPF, LIC Premium (₹)</Form.Label>
                      <Form.Control
                        type="number"
                        name="sec_80c_ppf_elss"
                        value={formData.sec_80c_ppf_elss}
                        onChange={handleChange}
                      />
                    </Form.Group>

                    <h6 className="fw-bold border-bottom pb-2 mb-3 mt-4 text-primary">
                      Section 80D Medical Health Insurance
                    </h6>
                    <Form.Group className="mb-3">
                      <Form.Label>Self & Parents Health Insurance Premium (₹)</Form.Label>
                      <Form.Control
                        type="number"
                        name="sec_80d_health_insurance"
                        value={formData.sec_80d_health_insurance}
                        onChange={handleChange}
                      />
                    </Form.Group>

                    <h6 className="fw-bold border-bottom pb-2 mb-3 mt-4 text-primary">
                      House Rent Allowance (HRA) & Home Loan
                    </h6>
                    <Row className="mb-3">
                      <Col md={6}>
                        <Form.Group>
                          <Form.Label>Annual Rent Paid (₹)</Form.Label>
                          <Form.Control
                            type="number"
                            name="hra_rent_paid_annual"
                            value={formData.hra_rent_paid_annual}
                            onChange={handleChange}
                          />
                        </Form.Group>
                      </Col>
                      <Col md={6}>
                        <Form.Group>
                          <Form.Label>Home Loan Interest Sec 24B (₹)</Form.Label>
                          <Form.Control
                            type="number"
                            name="home_loan_interest_sec24"
                            value={formData.home_loan_interest_sec24}
                            onChange={handleChange}
                          />
                        </Form.Group>
                      </Col>
                    </Row>
                  </>
                )}

                <div className="d-flex justify-content-between align-items-center mt-4 pt-3 border-top">
                  <div>
                    <span className="text-muted">Total Declared Deductions:</span>{' '}
                    <strong className="fs-5 text-success">₹{totalDeclared.toLocaleString()}</strong>
                  </div>
                  <Button variant="primary" type="submit" disabled={loading}>
                    {loading ? 'Submitting...' : 'Submit Declaration'}
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="border-0 shadow-sm mb-4">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0 fw-bold">Declaration History</h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive hover className="align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>FY</th>
                    <th>Regime</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {declarations.map((d) => (
                    <tr key={d.id}>
                      <td className="fw-semibold">{d.financial_year}</td>
                      <td>
                        <Badge bg={d.regime === 'New' ? 'primary' : 'secondary'}>{d.regime}</Badge>
                      </td>
                      <td>
                        <Badge bg={d.status === 'Verified' ? 'success' : 'info'}>{d.status}</Badge>
                      </td>
                    </tr>
                  ))}
                  {declarations.length === 0 && (
                    <tr>
                      <td colSpan="3" className="text-center py-4 text-muted">
                        No previous declarations.
                      </td>
                    </tr>
                  )}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
