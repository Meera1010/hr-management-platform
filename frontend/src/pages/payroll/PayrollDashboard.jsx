import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Button, Badge, Modal, Form, Spinner, Alert } from 'react-bootstrap';
import payrollApi from '../../services/payrollApi';

export default function PayrollDashboard() {
  const [runs, setRuns] = useState([]);
  const [payslips, setPayslips] = useState([]);
  const [salaries, setSalaries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showRunModal, setShowRunModal] = useState(false);
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [rRes, pRes, sRes] = await Promise.all([
        payrollApi.getRuns(),
        payrollApi.getPayslips(),
        payrollApi.getEmployeeSalaries()
      ]);
      setRuns(rRes.data.runs || []);
      setPayslips(pRes.data.payslips || []);
      setSalaries(sRes.data.salaries || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch payroll data');
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteRun = async (e) => {
    e.preventDefault();
    try {
      await payrollApi.executeRun({ month, year });
      setSuccess(`Payroll for ${year}-${month.toString().padStart(2, '0')} processed successfully.`);
      setShowRunModal(false);
      fetchData();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to process payroll run');
    }
  };

  if (loading) return <div className="text-center py-5"><Spinner animation="border" variant="primary" /></div>;

  return (
    <Container fluid className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">Payroll & Compensation Management</h2>
          <p className="text-muted">Process monthly payroll, manage salary components, and view pay slips.</p>
        </div>
        <Button variant="primary" onClick={() => setShowRunModal(true)}>
          <i className="bi bi-play-fill me-2"></i>Execute Monthly Payroll Run
        </Button>
      </div>

      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}
      {success && <Alert variant="success" dismissible onClose={() => setSuccess(null)}>{success}</Alert>}

      <Row className="mb-4 g-3">
        <Col md={3}>
          <Card className="border-0 shadow-sm bg-primary text-white">
            <Card.Body>
              <h6 className="text-white-50">Active Salary Structures</h6>
              <h3 className="fw-bold mb-0">{salaries.length}</h3>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="border-0 shadow-sm bg-success text-white">
            <Card.Body>
              <h6 className="text-white-50">Completed Payroll Runs</h6>
              <h3 className="fw-bold mb-0">{runs.filter(r => r.status === 'Approved').length}</h3>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="border-0 shadow-sm bg-info text-white">
            <Card.Body>
              <h6 className="text-white-50">Total Payslips Generated</h6>
              <h3 className="fw-bold mb-0">{payslips.length}</h3>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="border-0 shadow-sm bg-dark text-white">
            <Card.Body>
              <h6 className="text-white-50">Total Payout Volume</h6>
              <h3 className="fw-bold mb-0">₹{runs.reduce((acc, r) => acc + (r.total_net_payout || 0), 0).toLocaleString()}</h3>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Card className="border-0 shadow-sm mb-4">
        <Card.Header className="bg-white py-3">
          <h5 className="mb-0 fw-bold">Recent Payroll Runs</h5>
        </Card.Header>
        <Card.Body className="p-0">
          <Table responsive hover className="align-middle mb-0">
            <thead className="table-light">
              <tr>
                <th>Period</th>
                <th>Employees</th>
                <th>Gross Payout</th>
                <th>Deductions</th>
                <th>Net Payout</th>
                <th>Status</th>
                <th>Processed At</th>
              </tr>
            </thead>
            <tbody>
              {runs.map(run => (
                <tr key={run.id}>
                  <td className="fw-semibold">{run.period_label}</td>
                  <td>{run.total_employees}</td>
                  <td>₹{run.total_gross_payout?.toLocaleString()}</td>
                  <td>₹{run.total_deductions?.toLocaleString()}</td>
                  <td className="fw-bold text-success">₹{run.total_net_payout?.toLocaleString()}</td>
                  <td><Badge bg={run.status === 'Approved' ? 'success' : 'warning'}>{run.status}</Badge></td>
                  <td>{run.processed_at ? new Date(run.processed_at).toLocaleDateString() : '-'}</td>
                </tr>
              ))}
              {runs.length === 0 && <tr><td colSpan="7" className="text-center py-4">No payroll runs executed yet.</td></tr>}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      <Modal show={showRunModal} onHide={() => setShowRunModal(false)}>
        <Form onSubmit={handleExecuteRun}>
          <Modal.Header closeButton>
            <Modal.Title>Run Monthly Payroll</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Select Month</Form.Label>
              <Form.Select value={month} onChange={(e) => setMonth(parseInt(e.target.value))}>
                {Array.from({ length: 12 }, (_, i) => i + 1).map(m => (
                  <option key={m} value={m}>{new Date(2026, m - 1).toLocaleString('default', { month: 'long' })}</option>
                ))}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Select Year</Form.Label>
              <Form.Control type="number" value={year} onChange={(e) => setYear(parseInt(e.target.value))} />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowRunModal(false)}>Cancel</Button>
            <Button variant="primary" type="submit">Execute Payroll</Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </Container>
  );
}
