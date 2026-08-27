import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const response = await login(email, password);
      if (response.success) {
        // Redirect to their dashboard or home based on role
        const role = response.data.user.role;
        const from = location.state?.from?.pathname;
        
        if (from) {
          navigate(from, { replace: true });
        } else {
          // Default routing based on role
          if (role === 'Admin') navigate('/admin');
          else if (role === 'HR') navigate('/hr');
          else if (role === 'Recruiter') navigate('/recruiter');
          else if (role === 'Employee') navigate('/employee');
          else if (role === 'Candidate') navigate('/candidate');
          else if (role === 'Interviewer') navigate('/interviewer');
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

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-4">
          <div className="card shadow-sm">
            <div className="card-header bg-primary text-white">
              <h4 className="mb-0 text-center">Login to HR Platform</h4>
            </div>
            <div className="card-body p-4">
              {error && <div className="alert alert-danger">{error}</div>}
              
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Email address</label>
                  <input
                    type="email"
                    className="form-control"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    disabled={isSubmitting}
                  />
                </div>
                <div className="mb-4">
                  <label className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    disabled={isSubmitting}
                  />
                </div>
                <button 
                  type="submit" 
                  className="btn btn-primary w-100 py-2"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Logging in...
                    </>
                  ) : (
                    'Login'
                  )}
                </button>
              </form>
            </div>
          </div>
          
          <div className="alert alert-info mt-4 small">
            <strong>Demo Credentials:</strong><br/>
            Admin: admin@example.com<br/>
            HR: hr@example.com<br/>
            Recruiter: recruiter@example.com<br/>
            Employee: employee@example.com<br/>
            Candidate: candidate@example.com<br/>
            Password for all: demo-password
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
