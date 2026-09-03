import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ allowedRoles, children }) => {
  const { currentUser, loading } = useAuth();

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (!currentUser) {
    // Not logged in
    return <Navigate to="/login" replace />;
  }

  const role = currentUser?.role || currentUser?.role_name;
  if (allowedRoles && !allowedRoles.includes(role)) {
    // Logged in but insufficient role
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">
          <h4 className="alert-heading">Access Denied</h4>
          <p>You do not have permission to access this page.</p>
        </div>
      </div>
    );
  }

  return children ? children : <Outlet />;
};

export default ProtectedRoute;
