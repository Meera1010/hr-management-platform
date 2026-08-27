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
import Candidates from './pages/candidates/Candidates';
import CandidateForm from './pages/candidates/CandidateForm';
import CandidateProfile from './pages/candidates/CandidateProfile';
import CandidateSelfProfile from './pages/candidates/CandidateSelfProfile';
import CandidateApplications from './pages/applications/CandidateApplications';
import RecruiterApplications from './pages/applications/RecruiterApplications';
import ApplicationDetail from './pages/applications/ApplicationDetail';
import CandidateResumes from './pages/resumes/CandidateResumes';
import HRResumes from './pages/resumes/HRResumes';
import RecruiterResumes from './pages/resumes/RecruiterResumes';
import CandidateMatches from './pages/matching/CandidateMatches';
import RecruiterJobMatches from './pages/matching/RecruiterJobMatches';
import RecruiterJobRankings from './pages/recruiter/RecruiterJobRankings';
import RecruiterInterviews from './pages/recruiter/RecruiterInterviews';
import InterviewFormPage from './pages/recruiter/InterviewForm';
import InterviewFeedbackForm from './pages/recruiter/InterviewFeedbackForm';
import CandidateInterviews from './pages/candidate/CandidateInterviews';
import HROffers from './pages/hr/HROffers';
import CandidateOffers from './pages/candidate/CandidateOffers';

// Step 11+ Components and Pages
import HRDashboard from './pages/dashboards/HRDashboard';
import RecruiterDashboard from './pages/dashboards/RecruiterDashboard';
import EmployeeDashboard from './pages/dashboards/EmployeeDashboard';
import CandidateDashboard from './pages/dashboards/CandidateDashboard';
import TrainingCourses from './pages/training/TrainingCourses';
import EmployeeTraining from './pages/training/EmployeeTraining';
import NotificationsPage from './pages/notifications/NotificationsPage';
import AnalyticsDashboard from './pages/analytics/AnalyticsDashboard';
import ReportsPage from './pages/reports/ReportsPage';
import SearchResults from './pages/search/SearchResults';
import CareerRecommendations from './pages/recommendations/CareerRecommendations';
import NotificationsDropdown from './components/NotificationsDropdown';
import GlobalSearchInput from './components/GlobalSearchInput';

// Enterprise Sub-system Pages
import PayrollDashboard from './pages/payroll/PayrollDashboard';
import AssetDirectory from './pages/assets/AssetDirectory';
import OnboardingDashboard from './pages/lifecycle/OnboardingDashboard';
import OkrDashboard from './pages/okrs/OkrDashboard';
import CourseCatalog from './pages/learning/CourseCatalog';
import TimesheetLogger from './pages/timesheets/TimesheetLogger';
import ExpenseClaimList from './pages/expenses/ExpenseClaimList';
import GrievanceCenter from './pages/compliance/GrievanceCenter';
import WorkforcePlanner from './pages/workforce/WorkforcePlanner';

import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider, useAuth } from './context/AuthContext';
import api from './services/api';

function Home() {
  const [healthStatus, setHealthStatus] = useState(null);
  const { currentUser } = useAuth();

  useEffect(() => {
    api.get('/health')
      .then(res => setHealthStatus({ status: 'success', message: 'API is running' }))
      .catch(err => setHealthStatus({ status: 'error', message: 'Could not connect to API' }));
  }, []);

  return (
    <div className="container mt-5">
      <h1>AI HR Platform</h1>
      <p className="lead">Welcome to the AI-Powered HR, Recruitment & Employee Management Platform.</p>
      
      {currentUser && (
        <div className="alert alert-info border-0 shadow-sm mb-4">
          <strong>Logged in as:</strong> {currentUser.first_name} {currentUser.last_name} ({currentUser.role})
        </div>
      )}

      <div className="card mt-4 shadow-sm">
        <div className="card-header bg-white fw-bold">
          Backend API Status
        </div>
        <div className="card-body">
          {healthStatus ? (
            <div className={`alert ${healthStatus.status === 'success' ? 'alert-success' : 'alert-danger'} mb-0`}>
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

  const getDashboardLink = () => {
    if (!currentUser) return '/';
    switch (currentUser.role) {
      case 'Admin':
      case 'HR': return '/hr/dashboard';
      case 'Recruiter': return '/recruiter/dashboard';
      case 'Employee': return '/employee/dashboard';
      case 'Candidate': return '/candidate/dashboard';
      default: return '/';
    }
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand fw-bold" to={getDashboardLink()}>AI HR Platform</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            {currentUser && (
              <li className="nav-item">
                <Link className="nav-link" to={getDashboardLink()}>Dashboard</Link>
              </li>
            )}
            
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
                <li className="nav-item">
                  <Link className="nav-link" to="/payroll">Payroll</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/assets">Assets</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/lifecycle">Lifecycle</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/okrs">OKRs</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workforce">Workforce</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/training">Training</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/analytics">Analytics</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/reports">Reports</Link>
                </li>
              </>
            )}
            
            {['Admin', 'HR', 'Recruiter'].includes(currentUser?.role) && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/jobs">Manage Jobs</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/hr/candidates">Candidates</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/applications">Applications</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to={currentUser?.role === 'Recruiter' ? "/recruiter/resumes" : "/hr/resumes"}>Resumes</Link>
                </li>
                {currentUser?.role === 'Recruiter' && (
                  <>
                    <li className="nav-item">
                      <Link className="nav-link" to="/recruiter/rankings">AI Rankings</Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" to="/recruiter/interviews">Interviews</Link>
                    </li>
                  </>
                )}
                {(currentUser?.role === 'HR' || currentUser?.role === 'Admin') && (
                  <li className="nav-item">
                    <Link className="nav-link" to="/hr/offers">Offers</Link>
                  </li>
                )}
              </>
            )}
            
            {['Candidate'].includes(currentUser?.role) && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/candidate/jobs">Find Jobs</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/candidate/applications">My Applications</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/candidate/resumes">My Resumes</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/candidate/matches">Job Matches</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/candidate/interviews">My Interviews</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/candidate/offers">My Offers</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link text-warning" to="/career-recommendations">AI Recommendations</Link>
                </li>
              </>
            )}

            {['Employee', 'Interviewer'].includes(currentUser?.role) && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/learning">LXP Courses</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/timesheets">Timesheets</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/expenses">Expenses</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/compliance">Compliance</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link text-warning" to="/career-recommendations">AI Growth</Link>
                </li>
              </>
            )}

          </ul>

          <div className="d-flex align-items-center">
            {currentUser && <GlobalSearchInput />}
            {currentUser && <NotificationsDropdown />}

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
      </div>
    </nav>
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
            
            {/* Role Dashboards */}
            <Route path="/hr/dashboard" element={<ProtectedRoute allowedRoles={['Admin', 'HR']}><HRDashboard /></ProtectedRoute>} />
            <Route path="/recruiter/dashboard" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><RecruiterDashboard /></ProtectedRoute>} />
            <Route path="/employee/dashboard" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><EmployeeDashboard /></ProtectedRoute>} />
            <Route path="/candidate/dashboard" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Candidate']}><CandidateDashboard /></ProtectedRoute>} />

            {/* Enterprise Sub-systems */}
            <Route path="/payroll" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><PayrollDashboard /></ProtectedRoute>} />
            <Route path="/assets" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><AssetDirectory /></ProtectedRoute>} />
            <Route path="/lifecycle" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><OnboardingDashboard /></ProtectedRoute>} />
            <Route path="/okrs" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><OkrDashboard /></ProtectedRoute>} />
            <Route path="/learning" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><CourseCatalog /></ProtectedRoute>} />
            <Route path="/timesheets" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><TimesheetLogger /></ProtectedRoute>} />
            <Route path="/expenses" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><ExpenseClaimList /></ProtectedRoute>} />
            <Route path="/compliance" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><GrievanceCenter /></ProtectedRoute>} />
            <Route path="/workforce" element={<ProtectedRoute allowedRoles={['Admin', 'HR']}><WorkforcePlanner /></ProtectedRoute>} />

            {/* Global Search & Notifications */}
            <Route path="/search" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter', 'Employee', 'Candidate', 'Interviewer']}><SearchResults /></ProtectedRoute>} />
            <Route path="/notifications" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter', 'Employee', 'Candidate', 'Interviewer']}><NotificationsPage /></ProtectedRoute>} />
            <Route path="/career-recommendations" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee', 'Candidate']}><CareerRecommendations /></ProtectedRoute>} />

            {/* Training Management */}
            <Route path="/training" element={<ProtectedRoute allowedRoles={['Admin', 'HR']}><TrainingCourses /></ProtectedRoute>} />
            <Route path="/my-training" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><EmployeeTraining /></ProtectedRoute>} />

            {/* Analytics & Reports */}
            <Route path="/analytics" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><AnalyticsDashboard /></ProtectedRoute>} />
            <Route path="/reports" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><ReportsPage /></ProtectedRoute>} />

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

            {/* Candidate Management Routes (HR/Recruiter) */}
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']} />}>
              <Route path="/hr/candidates" element={<Candidates />} />
              <Route path="/hr/candidates/new" element={<CandidateForm />} />
              <Route path="/hr/candidates/:id" element={<CandidateProfile />} />
              <Route path="/hr/candidates/:id/edit" element={<CandidateForm />} />
            </Route>
            
            {/* Applications & Resumes Routes (Recruiter/HR/Admin) */}
            <Route path="/applications" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><RecruiterApplications /></ProtectedRoute>} />
            <Route path="/applications/:id" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><ApplicationDetail /></ProtectedRoute>} />
            <Route path="/hr/resumes" element={<ProtectedRoute allowedRoles={['Admin', 'HR']}><HRResumes /></ProtectedRoute>} />
            <Route path="/recruiter/resumes" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><RecruiterResumes /></ProtectedRoute>} />
            <Route path="/recruiter/jobs/:jobId/matches" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><RecruiterJobMatches /></ProtectedRoute>} />

            {/* Candidate Routes */}
            <Route path="/candidate/jobs" element={<ProtectedRoute allowedRoles={['Candidate']}><CandidateJobs /></ProtectedRoute>} />
            <Route path="/candidate/profile" element={<ProtectedRoute allowedRoles={['Candidate']}><CandidateSelfProfile /></ProtectedRoute>} />
            <Route path="/candidate/applications" element={<ProtectedRoute allowedRoles={['Candidate']}><CandidateApplications /></ProtectedRoute>} />
            <Route path="/candidate/resumes" element={<ProtectedRoute allowedRoles={['Candidate']}><CandidateResumes /></ProtectedRoute>} />
            <Route path="/candidate/matches" element={<ProtectedRoute allowedRoles={['Candidate']}><CandidateMatches /></ProtectedRoute>} />
            <Route path="/candidate/interviews" element={<ProtectedRoute allowedRoles={['Candidate']}><CandidateInterviews /></ProtectedRoute>} />
            <Route path="/candidate/offers" element={<ProtectedRoute allowedRoles={['Candidate']}><CandidateOffers /></ProtectedRoute>} />

            {/* Recruiter Interview & Ranking Routes */}
            <Route path="/recruiter/rankings" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><RecruiterJobRankings /></ProtectedRoute>} />
            <Route path="/recruiter/interviews" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><RecruiterInterviews /></ProtectedRoute>} />
            <Route path="/recruiter/interviews/schedule" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><InterviewFormPage /></ProtectedRoute>} />
            <Route path="/recruiter/interviews/:id/feedback" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><InterviewFeedbackForm /></ProtectedRoute>} />

            {/* HR Offers Routes */}
            <Route path="/hr/offers" element={<ProtectedRoute allowedRoles={['Admin', 'HR']}><HROffers /></ProtectedRoute>} />

            {/* Legacy Role Redirect Fallbacks */}
            <Route path="/admin" element={<ProtectedRoute allowedRoles={['Admin']}><HRDashboard /></ProtectedRoute>} />
            <Route path="/hr" element={<ProtectedRoute allowedRoles={['Admin', 'HR']}><HRDashboard /></ProtectedRoute>} />
            <Route path="/recruiter" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter']}><RecruiterDashboard /></ProtectedRoute>} />
            <Route path="/employee" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']}><EmployeeDashboard /></ProtectedRoute>} />
            <Route path="/candidate" element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Recruiter', 'Candidate']}><CandidateDashboard /></ProtectedRoute>} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
