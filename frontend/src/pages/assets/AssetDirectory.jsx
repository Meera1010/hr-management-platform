import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Button, Badge, Modal, Form, Spinner, Alert } from 'react-bootstrap';
import assetApi from '../../services/assetApi';

export default function AssetDirectory() {
  const [assets, setAssets] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [aRes, tRes] = await Promise.all([
        assetApi.getAssets(),
        assetApi.getItTickets()
      ]);
      setAssets(aRes?.assets || aRes?.data?.assets || []);
      setTickets(tRes?.tickets || tRes?.data?.tickets || []);
    } catch (err) {
      setError(err.message || err.response?.data?.message || 'Failed to fetch asset inventory');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-5"><Spinner animation="border" variant="primary" /></div>;

  return (
    <Container fluid className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">IT & Hardware Assets Directory</h2>
          <p className="text-muted">Track company laptops, monitors, licenses, and IT support tickets.</p>
        </div>
      </div>

      {error && <Alert variant="danger" dismissible onClose={() => setError(null)}>{error}</Alert>}

      <Row className="mb-4 g-3">
        <Col md={3}>
          <Card className="border-0 shadow-sm bg-primary text-white">
            <Card.Body>
              <h6>Total Managed Assets</h6>
              <h3 className="fw-bold mb-0">{assets.length}</h3>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="border-0 shadow-sm bg-success text-white">
            <Card.Body>
              <h6>Assigned Assets</h6>
              <h3 className="fw-bold mb-0">{assets.filter(a => a.status === 'Assigned').length}</h3>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="border-0 shadow-sm bg-warning text-dark">
            <Card.Body>
              <h6>Available in Stock</h6>
              <h3 className="fw-bold mb-0">{assets.filter(a => a.status === 'Available').length}</h3>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="border-0 shadow-sm bg-danger text-white">
            <Card.Body>
              <h6>Open IT Tickets</h6>
              <h3 className="fw-bold mb-0">{tickets.filter(t => t.status === 'Open').length}</h3>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Card className="border-0 shadow-sm">
        <Card.Header className="bg-white py-3">
          <h5 className="mb-0 fw-bold">Company Hardware Inventory</h5>
        </Card.Header>
        <Card.Body className="p-0">
          <Table responsive hover className="align-middle mb-0">
            <thead className="table-light">
              <tr>
                <th>Tag</th>
                <th>Asset Name</th>
                <th>Category</th>
                <th>Serial Number</th>
                <th>Condition</th>
                <th>Status</th>
                <th>Assigned To</th>
              </tr>
            </thead>
            <tbody>
              {assets.map(a => (
                <tr key={a.id}>
                  <td className="fw-bold text-primary">{a.asset_tag}</td>
                  <td className="fw-semibold">{a.name}</td>
                  <td>{a.category_name}</td>
                  <td><code>{a.serial_number || '-'}</code></td>
                  <td><Badge bg="secondary">{a.condition}</Badge></td>
                  <td>
                    <Badge bg={a.status === 'Assigned' ? 'success' : (a.status === 'Available' ? 'info' : 'warning')}>
                      {a.status}
                    </Badge>
                  </td>
                  <td>{a.assigned_to_employee || <span className="text-muted">Unassigned</span>}</td>
                </tr>
              ))}
              {assets.length === 0 && <tr><td colSpan="7" className="text-center py-4">No assets registered yet.</td></tr>}
            </tbody>
          </Table>
        </Card.Body>
      </Card>
    </Container>
  );
}
