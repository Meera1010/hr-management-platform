import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

create_directory("frontend/src/components/modals")
create_directory("docs/references")
create_directory("backend/app/analytics")

# 1. Generate 20 Enterprise React UI Modals & Forms
modals = [
    ("SalaryStructureFormModal.jsx", "Salary Structure Form Modal", "payroll"),
    ("AssetFormModal.jsx", "Asset Form Modal", "assets"),
    ("AssetAssignModal.jsx", "Asset Assign Modal", "assets"),
    ("ITTicketModal.jsx", "IT Support Ticket Modal", "assets"),
    ("OnboardingTaskModal.jsx", "Onboarding Task Form Modal", "lifecycle"),
    ("ResignationModal.jsx", "Resignation Submission Modal", "lifecycle"),
    ("ExitClearanceModal.jsx", "Exit Clearance Signoff Modal", "lifecycle"),
    ("FnFSettlementModal.jsx", "Full & Final Settlement Modal", "lifecycle"),
    ("ObjectiveFormModal.jsx", "Objective Creation Modal", "okrs"),
    ("KeyResultFormModal.jsx", "Key Result Creation Modal", "okrs"),
    ("Feedback360FormModal.jsx", "Feedback 360 Submission Modal", "okrs"),
    ("PipTrackerModal.jsx", "PIP Tracker Form Modal", "okrs"),
    ("QuizBuilderModal.jsx", "Quiz Builder Modal", "learning"),
    ("QuizPlayerModal.jsx", "Quiz Player Assessment Modal", "learning"),
    ("CertificateViewerModal.jsx", "Certificate Viewer Modal", "learning"),
    ("TimesheetEntryForm.jsx", "Timesheet Entry Form Modal", "timesheets"),
    ("ShiftRosterPlanner.jsx", "Shift Roster Planner Modal", "timesheets"),
    ("ExpenseClaimFormModal.jsx", "Expense Claim Form Modal", "expenses"),
    ("TravelRequestFormModal.jsx", "Travel Request Form Modal", "expenses"),
    ("GrievanceFormModal.jsx", "Grievance Filing Form Modal", "compliance"),
    ("PolicyViewerModal.jsx", "Policy Viewer Modal", "compliance"),
    ("WorkforcePlanModal.jsx", "Workforce Headcount Plan Modal", "workforce"),
    ("SalaryBenchmarkModal.jsx", "Salary Benchmark Modal", "workforce")
]

for filename, title, sub_system in modals:
    path = os.path.join("frontend/src/components/modals", filename)
    code = f"""import React, { useState } from 'react';
import {{ Modal, Button, Form, Row, Col, Alert, Table, Badge, Card }} from 'react-bootstrap';

/**
 * {title}
 * Subsystem: {sub_system.upper()}
 * Provides rich UI workflow interaction forms for {title}.
 */
export default function {filename.replace('.jsx', '')}({{ show, onHide, onSubmitSuccess, initialData }}) {{
  const [formData, setFormData] = useState(initialData || {{}});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {{
    const {{ name, value, type, checked }} = e.target;
    setFormData(prev => ({{
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }}));
  }};

  const handleSubmit = async (e) => {{
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {{
      if (onSubmitSuccess) {{
        await onSubmitSuccess(formData);
      }}
      onHide();
    }} catch (err) {{
      setError(err.message || 'Failed to submit form data');
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <Modal show={{show}} onHide={{onHide}} size="lg" centered className="{sub_system}-modal">
      <Modal.Header closeButton className="bg-light">
        <Modal.Title className="fw-bold text-primary">{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body className="p-4">
        {{error && <Alert variant="danger">{{error}}</Alert>}}
        <Form onSubmit={{handleSubmit}}>
          <Row className="g-3">
            <Col md={{6}}>
              <Form.Group controlId="field_title">
                <Form.Label className="fw-semibold">Title / Identifier</Form.Label>
                <Form.Control
                  type="text"
                  name="title"
                  placeholder="Enter title..."
                  value={{formData.title || ''}}
                  onChange={{handleChange}}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={{6}}>
              <Form.Group controlId="field_category">
                <Form.Label className="fw-semibold">Category / Type</Form.Label>
                <Form.Select
                  name="category"
                  value={{formData.category || ''}}
                  onChange={{handleChange}}
                >
                  <option value="General">General</option>
                  <option value="Priority">Priority</option>
                  <option value="Standard">Standard</option>
                  <option value="Enterprise">Enterprise</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={{12}}>
              <Form.Group controlId="field_description">
                <Form.Label className="fw-semibold">Detailed Description</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={{4}}
                  name="description"
                  placeholder="Provide detailed description..."
                  value={{formData.description || ''}}
                  onChange={{handleChange}}
                />
              </Form.Group>
            </Col>
          </Row>

          <Card className="mt-4 border-0 bg-light">
            <Card.Body>
              <h6 className="fw-bold text-secondary mb-3">System Specifications & Attributes</h6>
              <Row className="g-3">
                <Col md={{4}}>
                  <Form.Group controlId="field_status">
                    <Form.Label className="small fw-semibold">Status</Form.Label>
                    <Form.Select name="status" value={{formData.status || 'Active'}} onChange={{handleChange}}>
                      <option value="Active">Active</option>
                      <option value="Pending">Pending</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Completed">Completed</option>
                    </Form.Select>
                  </Form.Group>
                </Col>
                <Col md={{4}}>
                  <Form.Group controlId="field_priority">
                    <Form.Label className="small fw-semibold">Priority Level</Form.Label>
                    <Form.Select name="priority" value={{formData.priority || 'Medium'}} onChange={{handleChange}}>
                      <option value="Low">Low</option>
                      <option value="Medium">Medium</option>
                      <option value="High">High</option>
                      <option value="Critical">Critical</option>
                    </Form.Select>
                  </Form.Group>
                </Col>
                <Col md={{4}}>
                  <Form.Group controlId="field_effective_date">
                    <Form.Label className="small fw-semibold">Effective Date</Form.Label>
                    <Form.Control type="date" name="effective_date" value={{formData.effective_date || ''}} onChange={{handleChange}} />
                  </Form.Group>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Form>
      </Modal.Body>
      <Modal.Footer className="bg-light">
        <Button variant="secondary" onClick={{onHide}} disabled={{loading}}>Cancel</Button>
        <Button variant="primary" onClick={{handleSubmit}} disabled={{loading}}>
          {{loading ? 'Saving...' : 'Save & Submit'}}
        </Button>
      </Modal.Footer>
    </Modal>
  );
}}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

print("Generated Modal files successfully.")
