import React, { useState, useEffect } from 'react';
import { Container, Card, Nav, Badge, Spinner, Alert, Button } from 'react-bootstrap';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { globalSearch } from '../../services/api';

const SearchResults = () => {
  const [searchParams] = useSearchParams();
  const queryStr = searchParams.get('q') || '';
  const navigate = useNavigate();

  const [results, setResults] = useState({ employees: [], candidates: [], jobs: [], applications: [], departments: [] });
  const [activeTab, setActiveTab] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (queryStr) {
      performSearch(queryStr);
    }
  }, [queryStr]);

  const performSearch = async (q) => {
    try {
      setLoading(true);
      setError(null);
      const res = await globalSearch(q);
      setResults(res.results || { employees: [], candidates: [], jobs: [], applications: [], departments: [] });
    } catch (err) {
      setError(err.message || 'Search error');
    } finally {
      setLoading(false);
    }
  };

  const totalHits = (results.employees?.length || 0) +
                    (results.candidates?.length || 0) +
                    (results.jobs?.length || 0) +
                    (results.applications?.length || 0) +
                    (results.departments?.length || 0);

  return (
    <Container className="py-4">
      <h2>Search Results</h2>
      <p className="text-muted">Global search results for: <strong>"{queryStr}"</strong> ({totalHits} total results found)</p>

      {error && <Alert variant="danger">{error}</Alert>}

      <Card className="shadow-sm">
        <Card.Header className="bg-white">
          <Nav variant="tabs" activeKey={activeTab} onSelect={(k) => setActiveTab(k)}>
            <Nav.Item><Nav.Link eventKey="all">All Results ({totalHits})</Nav.Link></Nav.Item>
            <Nav.Item><Nav.Link eventKey="jobs">Jobs ({results.jobs?.length || 0})</Nav.Link></Nav.Item>
            <Nav.Item><Nav.Link eventKey="employees">Employees ({results.employees?.length || 0})</Nav.Link></Nav.Item>
            <Nav.Item><Nav.Link eventKey="candidates">Candidates ({results.candidates?.length || 0})</Nav.Link></Nav.Item>
            <Nav.Item><Nav.Link eventKey="applications">Applications ({results.applications?.length || 0})</Nav.Link></Nav.Item>
            <Nav.Item><Nav.Link eventKey="departments">Departments ({results.departments?.length || 0})</Nav.Link></Nav.Item>
          </Nav>
        </Card.Header>

        <Card.Body>
          {loading ? (
            <div className="text-center py-5"><Spinner animation="border" /></div>
          ) : totalHits === 0 ? (
            <div className="text-center py-5 text-muted">No matching entities found for "{queryStr}".</div>
          ) : (
            <div>
              {/* Jobs */}
              {(activeTab === 'all' || activeTab === 'jobs') && results.jobs?.length > 0 && (
                <div className="mb-4">
                  <h5>Jobs</h5>
                  <div className="list-group">
                    {results.jobs.map(j => (
                      <div key={j.id} className="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <Badge bg="secondary" className="me-2">{j.code}</Badge>
                          <strong>{j.title}</strong> - <span className="text-muted">{j.location}</span>
                        </div>
                        <Button size="sm" variant="outline-primary" onClick={() => navigate(`/jobs/${j.id}`)}>View Job</Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Employees */}
              {(activeTab === 'all' || activeTab === 'employees') && results.employees?.length > 0 && (
                <div className="mb-4">
                  <h5>Employees</h5>
                  <div className="list-group">
                    {results.employees.map(e => (
                      <div key={e.id} className="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <Badge bg="info" className="me-2">{e.code}</Badge>
                          <strong>{e.name}</strong> - {e.designation} ({e.department})
                        </div>
                        <Button size="sm" variant="outline-primary" onClick={() => navigate(`/hr/employees/${e.id}`)}>View Employee</Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Candidates */}
              {(activeTab === 'all' || activeTab === 'candidates') && results.candidates?.length > 0 && (
                <div className="mb-4">
                  <h5>Candidates</h5>
                  <div className="list-group">
                    {results.candidates.map(c => (
                      <div key={c.id} className="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <Badge bg="dark" className="me-2">{c.code}</Badge>
                          <strong>{c.name}</strong> - {c.current_role || 'Candidate'} ({c.email})
                        </div>
                        <Button size="sm" variant="outline-primary" onClick={() => navigate(`/hr/candidates/${c.id}`)}>View Profile</Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Applications */}
              {(activeTab === 'all' || activeTab === 'applications') && results.applications?.length > 0 && (
                <div className="mb-4">
                  <h5>Applications</h5>
                  <div className="list-group">
                    {results.applications.map(a => (
                      <div key={a.id} className="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                          <Badge bg="warning" text="dark" className="me-2">{a.code}</Badge>
                          <strong>{a.candidate_name}</strong> applied for {a.job_title}
                        </div>
                        <Button size="sm" variant="outline-primary" onClick={() => navigate(`/applications/${a.id}`)}>View Application</Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Departments */}
              {(activeTab === 'all' || activeTab === 'departments') && results.departments?.length > 0 && (
                <div className="mb-4">
                  <h5>Departments</h5>
                  <div className="list-group">
                    {results.departments.map(d => (
                      <div key={d.id} className="list-group-item d-flex justify-content-between align-items-center">
                        <div><strong>{d.name}</strong></div>
                        <Button size="sm" variant="outline-primary" onClick={() => navigate('/hr/departments')}>View Departments</Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </Card.Body>
      </Card>
    </Container>
  );
};

export default SearchResults;
