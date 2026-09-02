import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogin = async (userEmail, userPass) => {
    setError('');
    setIsSubmitting(true);

    try {
      const response = await login(userEmail, userPass);
      if (response.success) {
        const role = response.data?.user?.role || response.data?.user?.role_name;
        const from = location.state?.from?.pathname;
        
        if (from && from !== '/login') {
          navigate(from, { replace: true });
        } else {
          if (role === 'Admin' || role === 'HR') navigate('/hr/dashboard');
          else if (role === 'Recruiter') navigate('/recruiter/dashboard');
          else if (role === 'Employee') navigate('/employee/dashboard');
          else if (role === 'Candidate') navigate('/candidate/dashboard');
          else navigate('/');
        }
      } else {
        setError(response.message || 'Login failed');
      }
    } catch (err) {
      setError('An error occurred during login. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleLogin(email, password);
  };

  const quickLogin = (userEmail) => {
    setEmail(userEmail);
    setPassword('demo-password');
    handleLogin(userEmail, 'demo-password');
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-5">
          <div className="card shadow-lg border-0 rounded-4 overflow-hidden mb-4">
            <div className="card-header bg-primary text-white py-4 text-center">
              <h3 className="fw-bold mb-1">⚡ AI HR Platform</h3>
              <p className="mb-0 text-white-50">Enterprise Human Resource & Recruitment</p>
            </div>
            
            <div className="card-body p-4 p-md-5">
              {error && <div className="alert alert-danger rounded-3">{error}</div>}
              
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label fw-semibold">Email Address</label>
                  <input
                    type="email"
                    className="form-control form-control-lg fs-6"
                    placeholder="Enter email..."
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    disabled={isSubmitting}
                  />
                </div>
                <div className="mb-4">
                  <label className="form-label fw-semibold">Password</label>
                  <input
                    type="password"
                    className="form-control form-control-lg fs-6"
                    placeholder="Enter password..."
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    disabled={isSubmitting}
                  />
                </div>
                <button 
                  type="submit" 
                  className="btn btn-primary btn-lg w-100 fw-semibold shadow-sm mb-3"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                      Authenticating...
                    </>
                  ) : (
                    'Sign In'
                  )}
                </button>
              </form>

              <hr className="my-4" />

              <div className="text-center mb-3">
                <span className="text-muted small fw-bold text-uppercase">Or Instant 1-Click Demo Login</span>
              </div>

              <div className="d-grid gap-2">
                <button 
                  type="button" 
                  className="btn btn-outline-dark d-flex justify-content-between align-items-center py-2 px-3"
                  onClick={() => quickLogin('admin@example.com')}
                  disabled={isSubmitting}
                >
                  <span>👑 <strong>Admin</strong> (Full System Access)</span>
                  <span className="badge bg-dark">Login &rarr;</span>
                </button>
                <button 
                  type="button" 
                  className="btn btn-outline-primary d-flex justify-content-between align-items-center py-2 px-3"
                  onClick={() => quickLogin('hr@example.com')}
                  disabled={isSubmitting}
                >
                  <span>👥 <strong>HR Specialist</strong> (Workforce & Operations)</span>
                  <span className="badge bg-primary">Login &rarr;</span>
                </button>
                <button 
                  type="button" 
                  className="btn btn-outline-info d-flex justify-content-between align-items-center py-2 px-3"
                  onClick={() => quickLogin('recruiter@example.com')}
                  disabled={isSubmitting}
                >
                  <span>🎯 <strong>Recruiter</strong> (Jobs, Resumes & AI Match)</span>
                  <span className="badge bg-info text-dark">Login &rarr;</span>
                </button>
                <button 
                  type="button" 
                  className="btn btn-outline-success d-flex justify-content-between align-items-center py-2 px-3"
                  onClick={() => quickLogin('employee@example.com')}
                  disabled={isSubmitting}
                >
                  <span>💼 <strong>Employee</strong> (Self-Service Portal)</span>
                  <span className="badge bg-success">Login &rarr;</span>
                </button>
                <button 
                  type="button" 
                  className="btn btn-outline-warning text-dark d-flex justify-content-between align-items-center py-2 px-3"
                  onClick={() => quickLogin('candidate@example.com')}
                  disabled={isSubmitting}
                >
                  <span>🌟 <strong>Candidate</strong> (Applications & Offers)</span>
                  <span className="badge bg-warning text-dark">Login &rarr;</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
