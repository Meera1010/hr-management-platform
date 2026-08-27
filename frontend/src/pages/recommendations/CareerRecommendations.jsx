import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Badge, ProgressBar, Spinner, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { getMyCareerRecommendations } from '../../services/api';

const CareerRecommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const res = await getMyCareerRecommendations();
      setRecommendations(res.recommendations || []);
    } catch (err) {
      setError(err.message || 'Failed to compute career recommendations');
    } finally {
      setLoading(false);
    }
  };

  const getMatchVariant = (score) => {
    if (score >= 75) return 'success';
    if (score >= 50) return 'info';
    return 'warning';
  };

  return (
    <Container className="py-4">
      <div className="mb-4">
        <h2>AI Career & Job Recommendations</h2>
        <p className="text-muted">
          Transparent, decision-support skill matching between your qualifications and active job openings.
        </p>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      {loading ? (
        <div className="text-center py-5"><Spinner animation="border" /></div>
      ) : recommendations.length === 0 ? (
        <Alert variant="info">No open positions matching your career profile at this time.</Alert>
      ) : (
        <Row className="g-4">
          {recommendations.map(rec => (
            <Col md={6} key={rec.job_id}>
              <Card className="shadow-sm border-0 h-100">
                <Card.Header className="bg-white d-flex justify-content-between align-items-center">
                  <div>
                    <Badge bg="secondary" className="me-2">{rec.job_code}</Badge>
                    <span className="fw-bold fs-5">{rec.job_title}</span>
                  </div>
                  <Badge bg={getMatchVariant(rec.match_score)} className="fs-6 p-2">
                    {rec.match_score}% Match
                  </Badge>
                </Card.Header>

                <Card.Body>
                  <div className="text-muted mb-2">
                    📍 {rec.location || 'Remote'} • 💼 {rec.employment_type || 'Full Time'} • 🏢 {rec.department_name}
                  </div>

                  <ProgressBar
                    now={rec.match_score}
                    variant={getMatchVariant(rec.match_score)}
                    className="mb-3"
                    style={{ height: '8px' }}
                  />

                  <div className="mb-3">
                    <strong>Matching Skill Areas:</strong>
                    <div className="mt-1 d-flex flex-wrap gap-1">
                      {rec.matched_skills.length > 0 ? (
                        rec.matched_skills.map((s, idx) => (
                          <Badge bg="success" key={idx}>{s}</Badge>
                        ))
                      ) : (
                        <span className="text-muted small">None explicitly indexed</span>
                      )}
                    </div>
                  </div>

                  {rec.missing_skills.length > 0 && (
                    <div className="mb-3">
                      <strong>Recommended Skill Gap Upgrades:</strong>
                      <div className="mt-1 d-flex flex-wrap gap-1">
                        {rec.missing_skills.map((s, idx) => (
                          <Badge bg="outline-secondary" text="dark" className="border" key={idx}>{s}</Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  <Card className="bg-light border-0 p-2 mb-3">
                    <small className="text-secondary">
                      <strong>AI Decision Support Note:</strong> {rec.reasoning}
                    </small>
                  </Card>

                  <Button
                    variant="primary"
                    className="w-100"
                    onClick={() => navigate(`/jobs/${rec.job_id}`)}
                  >
                    View Job & Apply
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </Container>
  );
};

export default CareerRecommendations;
