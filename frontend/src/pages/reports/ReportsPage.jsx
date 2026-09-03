import React, { useState, useEffect } from 'react';
import { Container, Card, Nav, Table, Button, Spinner, Alert } from 'react-bootstrap';
import { getHeadcountReport, getAttendanceReport, getRecruitmentReport, getPerformanceReport, downloadReportCsv } from '../../services/api';

const ReportsPage = () => {
  const [activeTab, setActiveTab] = useState('headcount');
  const [reportData, setReportData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchReport(activeTab);
  }, [activeTab]);

  const fetchReport = async (tab) => {
    try {
      setLoading(true);
      setError(null);
      let res;
      if (tab === 'headcount') res = await getHeadcountReport();
      else if (tab === 'attendance') res = await getAttendanceReport();
      else if (tab === 'recruitment') res = await getRecruitmentReport();
      else if (tab === 'performance') res = await getPerformanceReport();
      
      setReportData(res.data || []);
    } catch (err) {
      setError(err.message || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadCsv = async () => {
    try {
      setError(null);
      await downloadReportCsv(activeTab);
    } catch (err) {
      setError(err.message || 'Failed to export CSV');
    }
  };

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2>HR & Executive Reports Generator</h2>
          <p className="text-muted">Export clean CSV reports for compliance, auditing, and workforce analysis.</p>
        </div>
        <Button variant="success" onClick={handleDownloadCsv} disabled={loading || reportData.length === 0}>
          📥 Export CSV Report
        </Button>
      </div>

      <Card className="shadow-sm">
        <Card.Header className="bg-white">
          <Nav variant="tabs" activeKey={activeTab} onSelect={(k) => setActiveTab(k)}>
            <Nav.Item>
              <Nav.Link eventKey="headcount">Employee Headcount</Nav.Link>
            </Nav.Item>
            <Nav.Item>
              <Nav.Link eventKey="attendance">Attendance Summary</Nav.Link>
            </Nav.Item>
            <Nav.Item>
              <Nav.Link eventKey="recruitment">Recruitment Pipeline</Nav.Link>
            </Nav.Item>
            <Nav.Item>
              <Nav.Link eventKey="performance">Performance Reviews</Nav.Link>
            </Nav.Item>
          </Nav>
        </Card.Header>

        <Card.Body className="p-0">
          {error && <div className="p-3"><Alert variant="danger">{error}</Alert></div>}

          <Table responsive hover className="mb-0">
            <thead className="bg-light">
              {reportData.length > 0 && (
                <tr>
                  {Object.keys(reportData[0]).map((key, idx) => (
                    <th key={idx}>{key}</th>
                  ))}
                </tr>
              )}
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="10" className="text-center py-4"><Spinner animation="border" /></td></tr>
              ) : reportData.length === 0 ? (
                <tr><td colSpan="10" className="text-center py-4 text-muted">No records found for this report.</td></tr>
              ) : (
                reportData.map((row, idx) => (
                  <tr key={idx}>
                    {Object.values(row).map((val, cIdx) => (
                      <td key={cIdx}>{val !== null ? String(val) : '-'}</td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default ReportsPage;
