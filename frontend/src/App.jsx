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
import HRLeaves from './pages/hr/HRLeaves';
import HRAttendance from './pages/hr/HRAttendance';
import HRPerformance from './pages/hr/HRPerformance';
import CandidateOffers from './pages/candidate/CandidateOffers';
import EmployeeAttendance from './pages/employee/EmployeeAttendance';
import EmployeeLeaves from './pages/employee/EmployeeLeaves';
import EmployeePerformance from './pages/employee/EmployeePerformance';

// HR Modules
import HRAttendance from './pages/hr/HRAttendance';
import HRLeaves from './pages/hr/HRLeaves';
import HRPerformance from './pages/hr/HRPerformance';
import PerformanceForm from './pages/hr/PerformanceForm';
import OfferForm from './pages/hr/OfferForm';

// Employee Self-Service Modules
import EmployeeAttendance from './pages/employee/EmployeeAttendance';
import EmployeeLeaves from './pages/employee/EmployeeLeaves';
import EmployeePerformance from './pages/employee/EmployeePerformance';

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
  const { currentUser, login } = useAuth();
  const navigate = useNavigate();

  const quickLogin = async (email) => {
    const res = await login(email, 'demo-password');
    if (res.success) {
      const role = res.data?.user?.role || res.data?.user?.role_name;
      if (role === 'Admin' || role === 'HR') navigate('/hr/dashboard');
      else if (role === 'Recruiter') navigate('/recruiter/dashboard');
      else if (role === 'Employee') navigate('/employee/dashboard');
      else if (role === 'Candidate') navigate('/candidate/dashboard');
      else navigate('/hr/dashboard');
    }
  };

  const getDashboardLink = () => {
    if (!currentUser) return '/login';
    const role = currentUser.role || currentUser.role_name;
    switch (role) {
      case 'Admin':
      case 'HR': return '/hr/dashboard';
      case 'Recruiter': return '/recruiter/dashboard';
      case 'Employee': return '/employee/dashboard';
      case 'Candidate': return '/candidate/dashboard';
      default: return '/hr/dashboard';
    }
  };

  return (
    <div className="container py-5">
      {currentUser ? (
        <div>
          <div className="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom">
            <div>
              <h2 className="fw-bold mb-1">Welcome back, {currentUser.first_name || currentUser.name}! 👋</h2>
              <p className="text-muted mb-0">Role: <span className="badge bg-primary fs-6">{currentUser.role || currentUser.role_name}</span> • Connected to AI HR Cloud</p>
            </div>
            <Link to={getDashboardLink()} className="btn btn-primary btn-lg shadow-sm">
              📊 Open My Dashboard &rarr;
            </Link>
          </div>

          <div className="row g-4 mb-5">
            <div className="col-md-4">
              <div className="card shadow-sm border-0 h-100 p-3 hover-shadow">
                <div className="card-body">
                  <h5 className="fw-bold text-primary mb-3">👥 Workforce & HR</h5>
                  <p className="text-muted small">Employee profiles, department directories, leave requests, attendance and OKRs.</p>
                  <div className="d-grid gap-2">
                    <Link to="/hr/employees" className="btn btn-sm btn-outline-primary text-start">👤 Employee Directory</Link>
                    <Link to="/hr/departments" className="btn btn-sm btn-outline-primary text-start">🏢 Departments</Link>
                    <Link to="/hr/leaves" className="btn btn-sm btn-outline-primary text-start">🏖️ Leave Approvals</Link>
                    <Link to="/hr/attendance" className="btn btn-sm btn-outline-primary text-start">⏱️ Attendance Logs</Link>
                  </div>
                </div>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card shadow-sm border-0 h-100 p-3 hover-shadow">
                <div className="card-body">
                  <h5 className="fw-bold text-success mb-3">⚙️ Operations & Finance</h5>
                  <p className="text-muted small">Payroll calculations, hardware IT asset tracking, timesheets and compliance logs.</p>
                  <div className="d-grid gap-2">
                    <Link to="/payroll" className="btn btn-sm btn-outline-success text-start">💰 Payroll & Tax</Link>
                    <Link to="/assets" className="btn btn-sm btn-outline-success text-start">💻 IT Asset Inventory</Link>
                    <Link to="/timesheets" className="btn btn-sm btn-outline-success text-start">⏱️ Timesheets</Link>
                    <Link to="/expenses" className="btn btn-sm btn-outline-success text-start">🧾 Expense Claims</Link>
                  </div>
                </div>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card shadow-sm border-0 h-100 p-3 hover-shadow">
                <div className="card-body">
                  <h5 className="fw-bold text-info mb-3">🎯 Recruitment & AI</h5>
                  <p className="text-muted small">Job openings, resume parsing, candidate scoring, and interview pipelines.</p>
                  <div className="d-grid gap-2">
                    <Link to="/jobs" className="btn btn-sm btn-outline-info text-start">📋 Manage Jobs</Link>
                    <Link to="/hr/candidates" className="btn btn-sm btn-outline-info text-start">👥 Candidates Pool</Link>
                    <Link to="/applications" className="btn btn-sm btn-outline-info text-start">📥 Applications</Link>
                    <Link to="/training" className="btn btn-sm btn-outline-info text-start">🎓 LXP Training</Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="text-center py-4">
          <div className="badge bg-primary-subtle text-primary border px-3 py-2 rounded-pill fw-semibold mb-3">
            ✨ Next-Gen Human Capital & Recruitment Platform
          </div>
          <h1 className="display-4 fw-bold mb-3">⚡ AI-Powered HR Platform</h1>
          <p className="lead text-muted mx-auto mb-5" style={{ maxWidth: '700px' }}>
            Seamless workforce management, AI candidate matching, automated payroll calculations, asset inventory, attendance tracking, and executive analytics.
          </p>

          <div className="card shadow-lg border-0 rounded-4 mx-auto p-4 p-md-5 mb-5" style={{ maxWidth: '800px' }}>
            <h4 className="fw-bold mb-4">🚀 Instant 1-Click Role Login</h4>
            <div className="row g-3">
              <div className="col-md-6 col-lg-4">
                <button 
                  className="btn btn-dark w-100 p-3 text-start shadow-sm border-0"
                  onClick={() => quickLogin('admin@example.com')}
                >
                  <div className="fw-bold fs-5 mb-1">👑 Admin</div>
                  <small className="text-white-50">Full system privileges</small>
                </button>
              </div>

              <div className="col-md-6 col-lg-4">
                <button 
                  className="btn btn-primary w-100 p-3 text-start shadow-sm border-0"
                  onClick={() => quickLogin('hr@example.com')}
                >
                  <div className="fw-bold fs-5 mb-1">👥 HR Specialist</div>
                  <small className="text-white-50">Workforce, leaves, payroll</small>
                </button>
              </div>

              <div className="col-md-6 col-lg-4">
                <button 
                  className="btn btn-info text-dark w-100 p-3 text-start shadow-sm border-0"
                  onClick={() => quickLogin('recruiter@example.com')}
                >
                  <div className="fw-bold fs-5 mb-1">🎯 Recruiter</div>
                  <small className="text-black-50">Jobs, candidates, AI ranking</small>
                </button>
              </div>

              <div className="col-md-6 col-lg-6">
                <button 
                  className="btn btn-success w-100 p-3 text-start shadow-sm border-0"
                  onClick={() => quickLogin('employee@example.com')}
                >
                  <div className="fw-bold fs-5 mb-1">💼 Employee</div>
                  <small className="text-white-50">Self-service portal, attendance, expenses</small>
                </button>
              </div>

              <div className="col-md-6 col-lg-6">
                <button 
                  className="btn btn-warning text-dark w-100 p-3 text-start shadow-sm border-0"
                  onClick={() => quickLogin('candidate@example.com')}
                >
                  <div className="fw-bold fs-5 mb-1">🌟 Candidate</div>
                  <small className="text-black-50">Apply for jobs, interviews, offers</small>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Navigation() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();
  const [openDropdown, setOpenDropdown] = useState(null);
  const [navExpanded, setNavExpanded] = useState(false);

  // Close dropdown on outside click or navigation
  useEffect(() => {
    const handleDocumentClick = (e) => {
      if (!e.target.closest('.nav-item.dropdown') && !e.target.closest('.navbar-toggler')) {
        setOpenDropdown(null);
      }
    };
    document.addEventListener('click', handleDocumentClick);
    return () => document.removeEventListener('click', handleDocumentClick);
  }, []);

  const toggleDropdown = (name, e) => {
    e?.stopPropagation();
    e?.preventDefault();
    setOpenDropdown(prev => prev === name ? null : name);
  };

  const handleMenuClick = () => {
    setOpenDropdown(null);
    setNavExpanded(false);
  };

  const handleLogout = async () => {
    setOpenDropdown(null);
    await logout();
    navigate('/login');
  };

  const getDashboardLink = () => {
    if (!currentUser) return '/';
    const role = currentUser.role || currentUser.role_name;
    switch (role) {
      case 'Admin':
      case 'HR': return '/hr/dashboard';
      case 'Recruiter': return '/recruiter/dashboard';
      case 'Employee': return '/employee/dashboard';
      case 'Candidate': return '/candidate/dashboard';
      default: return '/';
    }
  };

  const userRole = currentUser?.role || currentUser?.role_name;
  const isHRorAdmin = userRole === 'Admin' || userRole === 'HR';
  const isRecruiterOrHR = isHRorAdmin || userRole === 'Recruiter';

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm sticky-top">
      <div className="container">
        <Link className="navbar-brand fw-bold text-primary d-flex align-items-center gap-2" to={getDashboardLink()} onClick={handleMenuClick}>
          <span>⚡ AI HR Platform</span>
        </Link>
        
        <button 
          className="navbar-toggler" 
          type="button" 
          onClick={() => setNavExpanded(!navExpanded)}
          aria-expanded={navExpanded}
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className={`collapse navbar-collapse ${navExpanded ? 'show' : ''}`} id="navbarNav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            {currentUser && (
              <li className="nav-item">
                <Link className="nav-link fw-semibold" to={getDashboardLink()} onClick={handleMenuClick}>
                  📊 Dashboard
                </Link>
              </li>
            )}
            
            {/* Recruitment Dropdown */}
            {isRecruiterOrHR && (
              <li className={`nav-item dropdown ${openDropdown === 'recruitment' ? 'show' : ''}`}>
                <button
                  type="button"
                  className="nav-link dropdown-toggle btn btn-link text-white text-decoration-none fw-semibold border-0 shadow-none"
                  onClick={(e) => toggleDropdown('recruitment', e)}
                  aria-expanded={openDropdown === 'recruitment'}
                >
                  🎯 Recruitment
                </button>
                <ul className={`dropdown-menu shadow ${openDropdown === 'recruitment' ? 'show' : ''}`}>
                  <li><Link className="dropdown-item py-2" to="/jobs" onClick={handleMenuClick}>📋 Manage Jobs</Link></li>
                  <li><Link className="dropdown-item py-2" to="/hr/candidates" onClick={handleMenuClick}>👥 Candidates Pool</Link></li>
                  <li><Link className="dropdown-item py-2" to="/applications" onClick={handleMenuClick}>📥 Job Applications</Link></li>
                  <li><Link className="dropdown-item py-2" to={userRole === 'Recruiter' ? "/recruiter/resumes" : "/hr/resumes"} onClick={handleMenuClick}>📄 Resumes Vault</Link></li>
                  {userRole === 'Recruiter' && (
                    <>
                      <li><hr className="dropdown-divider" /></li>
                      <li><Link className="dropdown-item py-2" to="/recruiter/rankings" onClick={handleMenuClick}>🏆 AI Resume Rankings</Link></li>
                      <li><Link className="dropdown-item py-2" to="/recruiter/interviews" onClick={handleMenuClick}>🗓️ Interview Schedule</Link></li>
                    </>
                  )}
                  {isHRorAdmin && (
                    <>
                      <li><hr className="dropdown-divider" /></li>
                      <li><Link className="dropdown-item py-2" to="/hr/offers" onClick={handleMenuClick}>💼 Offers Management</Link></li>
                    </>
                  )}
                </ul>
              </li>
            )}

            {/* Workforce & HR Dropdown */}
            {isRecruiterOrHR && (
              <li className={`nav-item dropdown ${openDropdown === 'workforce' ? 'show' : ''}`}>
                <button
                  type="button"
                  className="nav-link dropdown-toggle btn btn-link text-white text-decoration-none fw-semibold border-0 shadow-none"
                  onClick={(e) => toggleDropdown('workforce', e)}
                  aria-expanded={openDropdown === 'workforce'}
                >
                  👥 Workforce & HR
                </button>
                <ul className={`dropdown-menu shadow ${openDropdown === 'workforce' ? 'show' : ''}`}>
                  <li><Link className="dropdown-item py-2" to="/hr/employees" onClick={handleMenuClick}>👤 Employee Directory</Link></li>
                  <li><Link className="dropdown-item py-2" to="/hr/departments" onClick={handleMenuClick}>🏢 Departments</Link></li>
                  <li><Link className="dropdown-item py-2" to="/lifecycle" onClick={handleMenuClick}>🚀 Onboarding & Exit</Link></li>
                  <li><Link className="dropdown-item py-2" to="/okrs" onClick={handleMenuClick}>🎯 Performance & OKRs</Link></li>
                  <li><Link className="dropdown-item py-2" to="/workforce" onClick={handleMenuClick}>📈 Workforce Planner</Link></li>
                </ul>
              </li>
            )}

            {/* Operations & Finance Dropdown */}
            {isRecruiterOrHR && (
              <li className={`nav-item dropdown ${openDropdown === 'operations' ? 'show' : ''}`}>
                <button
                  type="button"
                  className="nav-link dropdown-toggle btn btn-link text-white text-decoration-none fw-semibold border-0 shadow-none"
                  onClick={(e) => toggleDropdown('operations', e)}
                  aria-expanded={openDropdown === 'operations'}
                >
                  ⚙️ Operations
                </button>
                <ul className={`dropdown-menu shadow ${openDropdown === 'operations' ? 'show' : ''}`}>
                  <li><Link className="dropdown-item py-2" to="/payroll" onClick={handleMenuClick}>💰 Payroll & Salary</Link></li>
                  <li><Link className="dropdown-item py-2" to="/assets" onClick={handleMenuClick}>💻 IT Asset Inventory</Link></li>
                  <li><Link className="dropdown-item py-2" to="/timesheets" onClick={handleMenuClick}>⏱️ Timesheets & Shifts</Link></li>
                  <li><Link className="dropdown-item py-2" to="/expenses" onClick={handleMenuClick}>🧾 Expense Claims</Link></li>
                  <li><Link className="dropdown-item py-2" to="/compliance" onClick={handleMenuClick}>🛡️ Compliance & Grievances</Link></li>
                </ul>
              </li>
            )}

            {/* Analytics Dropdown */}
            {isRecruiterOrHR && (
              <li className={`nav-item dropdown ${openDropdown === 'analytics' ? 'show' : ''}`}>
                <button
                  type="button"
                  className="nav-link dropdown-toggle btn btn-link text-white text-decoration-none fw-semibold border-0 shadow-none"
                  onClick={(e) => toggleDropdown('analytics', e)}
                  aria-expanded={openDropdown === 'analytics'}
                >
                  📊 Analytics
                </button>
                <ul className={`dropdown-menu shadow ${openDropdown === 'analytics' ? 'show' : ''}`}>
                  <li><Link className="dropdown-item py-2" to="/analytics" onClick={handleMenuClick}>📈 Executive Analytics</Link></li>
                  <li><Link className="dropdown-item py-2" to="/reports" onClick={handleMenuClick}>📑 Reports Generator</Link></li>
                  <li><Link className="dropdown-item py-2" to="/training" onClick={handleMenuClick}>🎓 LXP Training Hub</Link></li>
                </ul>
              </li>
            )}

            {/* Admin Settings Dropdown */}
            {userRole === 'Admin' && (
              <li className={`nav-item dropdown ${openDropdown === 'admin' ? 'show' : ''}`}>
                <button
                  type="button"
                  className="nav-link dropdown-toggle btn btn-link text-white text-decoration-none fw-semibold border-0 shadow-none"
                  onClick={(e) => toggleDropdown('admin', e)}
                  aria-expanded={openDropdown === 'admin'}
                >
                  🔒 Admin
                </button>
                <ul className={`dropdown-menu shadow ${openDropdown === 'admin' ? 'show' : ''}`}>
                  <li><Link className="dropdown-item py-2" to="/admin/users" onClick={handleMenuClick}>👤 Manage Users</Link></li>
                  <li><Link className="dropdown-item py-2" to="/admin/roles" onClick={handleMenuClick}>🛡️ Manage Roles</Link></li>
                </ul>
              </li>
            )}

            {/* Candidate Portal Links */}
            {userRole === 'Candidate' && (
              <>
<<<<<<< HEAD
                {/* Recruitment Dropdown */}
                <li className="nav-item dropdown">
                  <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Recruitment</a>
                  <ul className="dropdown-menu">
                    <li><Link className="dropdown-item" to="/jobs">Manage Jobs</Link></li>
                    <li><Link className="dropdown-item" to="/hr/candidates">Candidates Pool</Link></li>
                    <li><Link className="dropdown-item" to="/applications">Applications</Link></li>
                    <li><Link className="dropdown-item" to={currentUser?.role === 'Recruiter' ? "/recruiter/resumes" : "/hr/resumes"}>Resumes Vault</Link></li>
                    {currentUser?.role === 'Recruiter' && (
                      <>
                        <li><Link className="dropdown-item" to="/recruiter/rankings">AI Resume Rankings</Link></li>
                        <li><Link className="dropdown-item" to="/recruiter/interviews">Interviews</Link></li>
                      </>
                    )}
                    {(currentUser?.role === 'HR' || currentUser?.role === 'Admin') && (
                      <li><Link className="dropdown-item" to="/hr/offers">Offers Management</Link></li>
                    )}
                  </ul>
                </li>

                {/* Workforce & HR Dropdown */}
                <li className="nav-item dropdown">
                  <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Workforce & HR</a>
                  <ul className="dropdown-menu">
                    <li><Link className="dropdown-item" to="/hr/employees">Employee Directory</Link></li>
                    <li><Link className="dropdown-item" to="/hr/departments">Departments</Link></li>
                    <li><Link className="dropdown-item" to="/hr/leaves">Leave Management</Link></li>
                    <li><Link className="dropdown-item" to="/hr/attendance">Attendance</Link></li>
                    <li><Link className="dropdown-item" to="/hr/performance">Performance Reviews</Link></li>
                    <li><Link className="dropdown-item" to="/lifecycle">Onboarding & Exit</Link></li>
                    <li><Link className="dropdown-item" to="/okrs">Performance & OKRs</Link></li>
                    <li><Link className="dropdown-item" to="/workforce">Workforce Planner</Link></li>
                  </ul>
                </li>

                {/* Operations & Finance Dropdown */}
                <li className="nav-item dropdown">
                  <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Operations</a>
                  <ul className="dropdown-menu">
                    <li><Link className="dropdown-item" to="/payroll">Payroll & Tax</Link></li>
                    <li><Link className="dropdown-item" to="/assets">IT Assets</Link></li>
                    <li><Link className="dropdown-item" to="/timesheets">Timesheets</Link></li>
                    <li><Link className="dropdown-item" to="/expenses">Expense Claims</Link></li>
                    <li><Link className="dropdown-item" to="/compliance">Compliance Center</Link></li>
                  </ul>
                </li>

                {/* Analytics Dropdown */}
                <li className="nav-item dropdown">
                  <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Analytics</a>
                  <ul className="dropdown-menu">
                    <li><Link className="dropdown-item" to="/training">LXP Training</Link></li>
                    <li><Link className="dropdown-item" to="/analytics">Executive Analytics</Link></li>
                    <li><Link className="dropdown-item" to="/reports">Reports Generator</Link></li>
                  </ul>
                </li>

                {currentUser?.role === 'Admin' && (
                  <li className="nav-item dropdown">
                    <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Admin Settings</a>
                    <ul className="dropdown-menu">
                      <li><Link className="dropdown-item" to="/admin/users">Manage Users</Link></li>
                      <li><Link className="dropdown-item" to="/admin/roles">Manage Roles</Link></li>
                    </ul>
                  </li>
                )}
=======
                <li className="nav-item"><Link className="nav-link" to="/candidate/jobs" onClick={handleMenuClick}>🔍 Find Jobs</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/candidate/applications" onClick={handleMenuClick}>📥 My Applications</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/candidate/interviews" onClick={handleMenuClick}>🗓️ My Interviews</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/candidate/offers" onClick={handleMenuClick}>💼 My Offers</Link></li>
                <li className="nav-item"><Link className="nav-link text-warning fw-semibold" to="/career-recommendations" onClick={handleMenuClick}>✨ AI Recommendations</Link></li>
>>>>>>> 8ff31b8c099d5cec38965a82ac8c6e030c590ab3
              </>
            )}

            {/* Employee Portal Links */}
            {userRole === 'Employee' && (
              <>
                <li className="nav-item"><Link className="nav-link" to="/payroll" onClick={handleMenuClick}>💰 My Payroll</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/timesheets" onClick={handleMenuClick}>⏱️ My Timesheet</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/expenses" onClick={handleMenuClick}>🧾 My Expenses</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/learning" onClick={handleMenuClick}>🎓 LXP Courses</Link></li>
                <li className="nav-item"><Link className="nav-link text-warning fw-semibold" to="/career-recommendations" onClick={handleMenuClick}>✨ AI Growth</Link></li>
              </>
            )}
<<<<<<< HEAD

            {currentUser?.role === 'Employee' && (
              <>
                <li className="nav-item"><Link className="nav-link" to="/payroll">My Payroll</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/timesheets">My Timesheet</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/expenses">My Expenses</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/employee/attendance">My Attendance</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/employee/leaves">My Leaves</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/employee/performance">My Performance</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/learning">LXP Courses</Link></li>
                <li className="nav-item"><Link className="nav-link text-warning" to="/career-recommendations">AI Growth</Link></li>
              </>
            )}


=======
>>>>>>> 8ff31b8c099d5cec38965a82ac8c6e030c590ab3
          </ul>

          <div className="d-flex align-items-center gap-2">
            {currentUser && <GlobalSearchInput />}
            {currentUser && <NotificationsDropdown />}

            <ul className="navbar-nav">
              {currentUser ? (
                <li className={`nav-item dropdown ${openDropdown === 'user' ? 'show' : ''}`}>
                  <button 
                    type="button"
                    className="nav-link dropdown-toggle btn btn-link text-white text-decoration-none border-0 shadow-none d-flex align-items-center gap-2"
                    onClick={(e) => toggleDropdown('user', e)}
                    aria-expanded={openDropdown === 'user'}
                  >
                    <span className="badge bg-primary rounded-pill">{userRole}</span>
                    <span>{currentUser.first_name || currentUser.name || 'User'}</span>
                  </button>
                  <ul className={`dropdown-menu dropdown-menu-end shadow ${openDropdown === 'user' ? 'show' : ''}`}>
                    <li className="dropdown-header">Signed in as <strong>{currentUser.email}</strong></li>
                    <li><hr className="dropdown-divider" /></li>
                    <li><Link className="dropdown-item py-2" to={getDashboardLink()} onClick={handleMenuClick}>📊 My Dashboard</Link></li>
                    {userRole === 'Candidate' && (
                      <li><Link className="dropdown-item py-2" to="/candidate/profile" onClick={handleMenuClick}>👤 My Profile</Link></li>
                    )}
                    <li><hr className="dropdown-divider" /></li>
                    <li><button className="dropdown-item py-2 text-danger" onClick={handleLogout}>🚪 Logout</button></li>
                  </ul>
                </li>
              ) : (
                <li className="nav-item">
                  <Link className="btn btn-primary btn-sm px-3" to="/login" onClick={handleMenuClick}>Login</Link>
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
<<<<<<< HEAD
              <Route path="/hr/leaves" element={<HRLeaves />} />
              <Route path="/hr/attendance" element={<HRAttendance />} />
              <Route path="/hr/performance" element={<HRPerformance />} />
=======
              <Route path="/hr/attendance" element={<HRAttendance />} />
              <Route path="/hr/leaves" element={<HRLeaves />} />
              <Route path="/hr/performance" element={<HRPerformance />} />
              <Route path="/hr/performance/new" element={<PerformanceForm />} />
              <Route path="/hr/offers/new" element={<OfferForm />} />
>>>>>>> 8ff31b8c099d5cec38965a82ac8c6e030c590ab3
            </Route>

            {/* Employee Self-Service Routes */}
            <Route element={<ProtectedRoute allowedRoles={['Admin', 'HR', 'Employee']} />}>
              <Route path="/employee/attendance" element={<EmployeeAttendance />} />
              <Route path="/employee/leaves" element={<EmployeeLeaves />} />
              <Route path="/employee/performance" element={<EmployeePerformance />} />
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

            {/* Role Redirects & Fallbacks */}
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
