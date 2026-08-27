import React from 'react';
import { Modal, Button, Row, Col, Table, Badge } from 'react-bootstrap';

export default function PaySlipModal({ show, onHide, payslip }) {
  if (!payslip) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" centered className="payslip-modal">
      <Modal.Header closeButton className="border-bottom pb-3">
        <div>
          <Modal.Title className="fw-bold">Pay Slip Statement</Modal.Title>
          <span className="text-muted fs-6">Pay Period: {payslip.period_label}</span>
        </div>
      </Modal.Header>
      <Modal.Body className="p-4">
        <div className="payslip-container p-3 border rounded shadow-sm bg-white">
          {/* Header Info */}
          <Row className="mb-4 pb-3 border-bottom align-items-center">
            <Col md={8}>
              <h4 className="fw-bold text-primary mb-1">ENTERPRISE HR PLATFORM PVT LTD</h4>
              <p className="text-muted small mb-0">
                100 Innovation Park, Tech Corridor, Outer Ring Road, Bengaluru 560103
              </p>
              <p className="text-muted small mb-0">CIN: U72200KA2026PTC123456 | GSTIN: 29AAAAA0000A1Z5</p>
            </Col>
            <Col md={4} className="text-end">
              <Badge bg={payslip.payment_status === 'Paid' ? 'success' : 'warning'} className="px-3 py-2 fs-6">
                {payslip.payment_status || 'Paid'}
              </Badge>
              <div className="small text-muted mt-1">Ref: {payslip.transaction_reference || 'TXN-9982341'}</div>
            </Col>
          </Row>

          {/* Employee Details Grid */}
          <Row className="mb-4 bg-light p-3 rounded mx-0">
            <Col md={6} className="mb-2 mb-md-0">
              <div className="small text-muted">Employee Code & Name:</div>
              <div className="fw-bold fs-6">[{payslip.employee_code || 'EMP-001'}] {payslip.employee_name}</div>
              <div className="small text-muted mt-2">Department:</div>
              <div className="fw-semibold">{payslip.department || 'Engineering'}</div>
            </Col>
            <Col md={6}>
              <div className="small text-muted">Pay Period & Days:</div>
              <div className="fw-bold fs-6">{payslip.period_label} | {payslip.payable_days} Days Payable</div>
              <div className="small text-muted mt-2">Payment Mode:</div>
              <div className="fw-semibold">{payslip.payment_mode || 'Direct Deposit'}</div>
            </Col>
          </Row>

          {/* Earnings vs Deductions Table */}
          <Row className="g-4 mb-4">
            {/* Earnings Column */}
            <Col md={6}>
              <div className="card h-100 border-0 bg-light">
                <div className="card-header bg-success text-white fw-bold">Earnings (Gross)</div>
                <div className="card-body p-0">
                  <Table borderless hover className="align-middle mb-0">
                    <tbody>
                      <tr>
                        <td>Basic Salary</td>
                        <td className="text-end fw-semibold">₹{payslip.basic_pay?.toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td>House Rent Allowance (HRA)</td>
                        <td className="text-end fw-semibold">₹{payslip.hra?.toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td>Special Allowance</td>
                        <td className="text-end fw-semibold">₹{(payslip.special_allowance || 0).toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td>Conveyance Allowance</td>
                        <td className="text-end fw-semibold">₹{(payslip.conveyance_allowance || 0).toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td>Medical Allowance</td>
                        <td className="text-end fw-semibold">₹{(payslip.medical_allowance || 0).toLocaleString()}</td>
                      </tr>
                      {payslip.bonus_payout > 0 && (
                        <tr>
                          <td>Bonus Payout</td>
                          <td className="text-end fw-semibold">₹{payslip.bonus_payout.toLocaleString()}</td>
                        </tr>
                      )}
                      {payslip.overtime_payout > 0 && (
                        <tr>
                          <td>Overtime Payout</td>
                          <td className="text-end fw-semibold">₹{payslip.overtime_payout.toLocaleString()}</td>
                        </tr>
                      )}
                      <tr className="table-success fw-bold">
                        <td>Total Gross Earnings</td>
                        <td className="text-end">₹{payslip.gross_earnings?.toLocaleString()}</td>
                      </tr>
                    </tbody>
                  </Table>
                </div>
              </div>
            </Col>

            {/* Deductions Column */}
            <Col md={6}>
              <div className="card h-100 border-0 bg-light">
                <div className="card-header bg-danger text-white fw-bold">Deductions</div>
                <div className="card-body p-0">
                  <Table borderless hover className="align-middle mb-0">
                    <tbody>
                      <tr>
                        <td>Provident Fund (Employee EPF)</td>
                        <td className="text-end fw-semibold">₹{(payslip.pf_deduction || 0).toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td>Professional Tax (PT)</td>
                        <td className="text-end fw-semibold">₹{(payslip.professional_tax || 0).toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td>Income Tax (TDS)</td>
                        <td className="text-end fw-semibold">₹{(payslip.tds_deduction || 0).toLocaleString()}</td>
                      </tr>
                      {payslip.unpaid_leave_deduction > 0 && (
                        <tr>
                          <td>Unpaid Leave Deduction</td>
                          <td className="text-end fw-semibold">₹{payslip.unpaid_leave_deduction.toLocaleString()}</td>
                        </tr>
                      )}
                      <tr className="table-danger fw-bold">
                        <td>Total Deductions</td>
                        <td className="text-end">₹{payslip.total_deductions?.toLocaleString()}</td>
                      </tr>
                    </tbody>
                  </Table>
                </div>
              </div>
            </Col>
          </Row>

          {/* Net Salary Highlight Box */}
          <div className="p-3 bg-primary text-white rounded text-center mb-3 shadow-sm">
            <span className="fs-6 text-uppercase tracking-wider opacity-75">Net Salary Payable Direct to Bank</span>
            <h2 className="fw-bold mb-0 mt-1">₹{payslip.net_salary?.toLocaleString()}</h2>
          </div>

          <div className="text-muted small text-center italic">
            This is a system generated salary statement document. No physical signature required.
          </div>
        </div>
      </Modal.Body>
      <Modal.Footer className="bg-light">
        <Button variant="outline-secondary" onClick={onHide}>Close</Button>
        <Button variant="primary" onClick={handlePrint}>Print / Save PDF</Button>
      </Modal.Footer>
    </Modal>
  );
}
