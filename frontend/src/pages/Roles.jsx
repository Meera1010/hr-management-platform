import React, { useState, useEffect } from 'react';
import { getRoles } from '../services/api';

const Roles = () => {
  const [roles, setRoles] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRoles();
  }, []);

  const fetchRoles = async () => {
    try {
      const data = await getRoles();
      setRoles(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Admin: Role Management</h2>
      <p className="text-muted">Roles are currently managed through backend seed data.</p>
      
      {error && <div className="alert alert-danger">{error}</div>}

      <div className="table-responsive mt-3">
        <table className="table table-bordered">
          <thead className="table-light">
            <tr>
              <th>ID</th>
              <th>Role Name</th>
              <th>Description</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {roles.length > 0 ? roles.map(role => (
              <tr key={role.id}>
                <td>{role.id}</td>
                <td><strong>{role.name}</strong></td>
                <td>{role.description}</td>
                <td>{new Date(role.created_at).toLocaleDateString()}</td>
              </tr>
            )) : (
              <tr><td colSpan="4" className="text-center">No roles found. Ensure the database is seeded.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Roles;
