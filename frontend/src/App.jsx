import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import Users from './pages/Users';
import Roles from './pages/Roles';
import Login from './pages/Login';
import Departments from './pages/Departments';
import Employees from './pages/Employees';
import EmployeeProfile from './pages/EmployeeProfile';
import EmployeeForm from './pages/EmployeeForm';
import Jobs from './pages/jobs/Jobs';
import JobForm from './pages/jobs/JobForm';
import JobProfile from './pages/jobs/JobProfile';
import CandidateJobs from './pages/jobs/CandidateJobs';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider, useAuth } from './context/AuthContext';
import api from './services/api';

function Home() {
  const [healthStatus, setHealthStatus] = useState(null);

  useEffect(() => {
    api.get('/health')
      .then(res => setHealthStatus({ status: 'success', message: 'API is running' }))
      .catch(err => setHealthStatus({ status: 'error', message: 'Could not connect to API' }));
  }, []);

  return (
    <div className="container mt-5">
      <h1>AI HR Platform</h1>
      <p className="lead">Welcome to the AI-Powered HR, Recruitment & Employee Management Platform.</p>
      
      <div className="card mt-4">
        <div className="card-header">
          Backend API Status
        </div>
        <div className="card-body">
          {healthStatus ? (
            <div className={`alert ${healthStatus.status === 'success' ? 'alert-success' : 'alert-danger'}`}>
              <strong>Status:</strong> {healthStatus.status} <br/>
              <strong>Message:</strong> {healthStatus.message}
            </div>
          ) : (
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function Navigation() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">AI HR Platform</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">Home</Link>
            </li>
            
            {/* Dynamic Role-Based Links */}
            {currentUser?.role === 'Admin' && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/admin/users">Manage Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/admin/roles">Manage Roles</Link>
                </li>
              </>
            )}

            {(currentUser?.role === 'Admin' || currentUser?.role === 'HR') && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/hr/departments">Departments</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/hr/employees">Employees</Link>
                </li>
              </>
            )}
            
            {['Admin', 'HR', 'Recruiter'].includes(currentUser?.role) && (
              <li className="nav-item">
                <Link className="nav-link" to="/jobs">Manage Jobs</Link>
              </li>
            )}
            
            {['Candidate', 'Employee', 'Interviewer'].includes(currentUser?.role) && (
              <li className="nav-item">
                <Link className="nav-link" to="/careers">Careers (Open Jobs)</Link>
              </li>
            )}

          </ul>
          <ul className="navbar-nav">
            {currentUser ? (
              <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  {currentUser.first_name} ({currentUser.role})
                </a>
                <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                  <li><button className="dropdown-item" onClick={handleLogout}>Logout</button></li>
                </ul>
              </li>
            ) : (
              <li className="nav-item">
                <Link className="nav-link" to="/login">Login</Link>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

function DashboardPlaceholder({ role }) {
  return (
    <div className="container mt-5">
      <h2>{role} Dashboard</h2>
      <p>This module is not implemented yet.</p>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div>
          <Navigation />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            
            {/* Admin Routes */}
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR']} />}>
              <Route path="/admin/users" element={<Users />} />
              <Route path="/admin/roles" element={<Roles />} />
            </Route>

            {/* HR Routes */}
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR']} />}>
              <Route path="/hr/departments" element={<Departments />} />
              <Route path="/hr/employees" element={<Employees />} />
              <Route path="/hr/employees/new" element={<EmployeeForm />} />
              <Route path="/hr/employees/:id" element={<EmployeeProfile />} />
            </Route>
            
            {/* Jobs Routes */}
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']} />}>
              <Route path="/jobs" element={<Jobs />} />
              <Route path="/jobs/new" element={<JobForm />} />
              <Route path="/jobs/:id/edit" element={<JobForm />} />
            </Route>
            
            {/* Shared Jobs Route */}
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter', 'Employee', 'Candidate', 'Interviewer']} />}>
              <Route path="/jobs/:id" element={<JobProfile />} />
              <Route path="/careers" element={<CandidateJobs />} />
            </Route>

            {/* Other Role Placeholders */}
            <Route element={<ProtectedRoute allowedRoles={['Admin']} />}>
              <Route path="/admin" element={<DashboardPlaceholder role="Admin" />} />
            </Route>
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR']} />}>
              <Route path="/hr" element={<DashboardPlaceholder role="HR" />} />
            </Route>
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']} />}>
              <Route path="/recruiter" element={<DashboardPlaceholder role="Recruiter" />} />
            </Route>
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']} />}>
              <Route path="/employee" element={<DashboardPlaceholder role="Employee" />} />
            </Route>
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter', 'Candidate']} />}>
              <Route path="/candidate" element={<DashboardPlaceholder role="Candidate" />} />
            </Route>
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter', 'Interviewer']} />}>
              <Route path="/interviewer" element={<DashboardPlaceholder role="Interviewer" />} />
            </Route>
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
