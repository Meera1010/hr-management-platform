import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';

function Candidates() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);

  const fetchCandidates = async (page = 1) => {
    try {
      setLoading(true);
      const params = { page, limit: 10 };
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;

      const response = await api.getCandidates(params);
      const data = response?.data || response || {};
      setCandidates(data.candidates || []);
      setCurrentPage(data.current_page || 1);
      setTotalPages(data.total_pages || 1);
      setTotalRecords(data.total_records || (data.candidates ? data.candidates.length : 0));
    } catch (error) {
      console.error('Error fetching candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchCandidates(1);
  };

  const handleDeactivate = async (id) => {
    if (window.confirm('Are you sure you want to deactivate this candidate?')) {
      try {
        await api.deactivateCandidate(id);
        fetchCandidates(currentPage);
      } catch (error) {
        console.error('Error deactivating candidate:', error);
        alert('Failed to deactivate candidate');
      }
    }
  };

  const getStatusBadge = (status) => {
    const colors = {
      'Available': 'bg-primary',
      'Hired': 'bg-success',
      'Rejected': 'bg-danger',
      'Active': 'bg-info',
      'Inactive': 'bg-secondary'
    };
    return <span className={`badge ${colors[status] || 'bg-secondary'}`}>{status}</span>;
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Candidates ({totalRecords})</h2>
        <Link to="/hr/candidates/new" className="btn btn-primary">Add Candidate</Link>
      </div>

      <div className="card mb-4">
        <div className="card-body">
          <form onSubmit={handleSearch} className="row g-3">
            <div className="col-md-6">
              <input 
                type="text" 
                className="form-control" 
                placeholder="Search by name, email, skills..." 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <div className="col-md-4">
              <select 
                className="form-select"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="">All Statuses</option>
                <option value="Available">Available</option>
                <option value="Active">Active</option>
                <option value="Hired">Hired</option>
                <option value="Rejected">Rejected</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
            <div className="col-md-2">
              <button type="submit" className="btn btn-secondary w-100">Search</button>
            </div>
          </form>
        </div>
      </div>

      {loading ? (
        <div className="text-center"><div className="spinner-border text-primary" /></div>
      ) : (
        <>
          <div className="table-responsive">
            <table className="table table-striped table-hover">
              <thead className="table-dark">
                <tr>
                  <th>Code</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Experience</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {candidates.length > 0 ? candidates.map(candidate => (
                  <tr key={candidate.id}>
                    <td>{candidate.candidate_code}</td>
                    <td>{candidate.first_name} {candidate.last_name}</td>
                    <td>{candidate.email}</td>
                    <td>{candidate.current_role || '-'}</td>
                    <td>{candidate.experience_years} yrs</td>
                    <td>{getStatusBadge(candidate.status)}</td>
                    <td>
                      <div className="btn-group btn-group-sm">
                        <Link to={`/hr/candidates/${candidate.id}`} className="btn btn-outline-info">View</Link>
                        <Link to={`/hr/candidates/${candidate.id}/edit`} className="btn btn-outline-primary">Edit</Link>
                        {candidate.status !== 'Inactive' && (
                          <button 
                            className="btn btn-outline-danger"
                            onClick={() => handleDeactivate(candidate.id)}
                          >
                            Deactivate
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan="7" className="text-center">No candidates found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {totalPages > 1 && (
            <nav>
              <ul className="pagination justify-content-center">
                <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                  <button className="page-link" onClick={() => fetchCandidates(currentPage - 1)}>Previous</button>
                </li>
                {[...Array(totalPages).keys()].map(num => (
                  <li key={num + 1} className={`page-item ${currentPage === num + 1 ? 'active' : ''}`}>
                    <button className="page-link" onClick={() => fetchCandidates(num + 1)}>{num + 1}</button>
                  </li>
                ))}
                <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                  <button className="page-link" onClick={() => fetchCandidates(currentPage + 1)}>Next</button>
                </li>
              </ul>
            </nav>
          )}
        </>
      )}
    </div>
  );
}

export default Candidates;
