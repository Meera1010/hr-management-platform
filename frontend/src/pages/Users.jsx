import React, { useState, useEffect } from 'react';
import { getUsers, createUser, updateUser, deactivateUser, getRoles } from '../services/api';
import UserForm from '../components/UserForm';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  
  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [usersData, rolesData] = await Promise.all([getUsers(), getRoles()]);
      setUsers(usersData);
      setRoles(rolesData);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCreate = async (data) => {
    try {
      await createUser(data);
      setShowForm(false);
      fetchData();
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdate = async (data) => {
    try {
      await updateUser(editingUser.id, data);
      setEditingUser(null);
      setShowForm(false);
      fetchData();
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeactivate = async (id) => {
    if (window.confirm('Are you sure you want to deactivate this user?')) {
      try {
        await deactivateUser(id);
        fetchData();
      } catch (err) {
        setError(err.message);
      }
    }
  };

  const filteredUsers = users.filter(u => {
    const matchesSearch = `${u.first_name} ${u.last_name} ${u.email}`.toLowerCase().includes(search.toLowerCase());
    const matchesRole = roleFilter ? u.role_id.toString() === roleFilter : true;
    return matchesSearch && matchesRole;
  });

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Admin: User Management</h2>
        {!showForm && (
          <button className="btn btn-primary" onClick={() => { setEditingUser(null); setShowForm(true); }}>
            + Add User
          </button>
        )}
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {showForm ? (
        <div className="card">
          <div className="card-header">
            {editingUser ? 'Edit User' : 'Add New User'}
          </div>
          <div className="card-body">
            <UserForm 
              initialData={editingUser} 
              onSubmit={editingUser ? handleUpdate : handleCreate} 
              onCancel={() => { setShowForm(false); setEditingUser(null); setError(null); }}
              roles={roles}
            />
          </div>
        </div>
      ) : (
        <>
          <div className="row mb-3">
            <div className="col-md-6">
              <input 
                type="text" 
                className="form-control" 
                placeholder="Search by name or email..." 
                value={search}
                onChange={e => setSearch(e.target.value)}
              />
            </div>
            <div className="col-md-4">
              <select className="form-select" value={roleFilter} onChange={e => setRoleFilter(e.target.value)}>
                <option value="">All Roles</option>
                {roles.map(r => (
                  <option key={r.id} value={r.id}>{r.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="table-responsive">
            <table className="table table-striped table-hover">
              <thead className="table-dark">
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Created Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.length > 0 ? filteredUsers.map(user => (
                  <tr key={user.id}>
                    <td>{user.first_name} {user.last_name}</td>
                    <td>{user.email}</td>
                    <td>{user.phone || '-'}</td>
                    <td><span className="badge bg-secondary">{user.role_name}</span></td>
                    <td>
                      {user.is_active ? 
                        <span className="badge bg-success">Active</span> : 
                        <span className="badge bg-danger">Inactive</span>
                      }
                    </td>
                    <td>{new Date(user.created_at).toLocaleDateString()}</td>
                    <td>
                      <button className="btn btn-sm btn-outline-primary me-2" onClick={() => { setEditingUser(user); setShowForm(true); }}>Edit</button>
                      {user.is_active && (
                        <button className="btn btn-sm btn-outline-danger" onClick={() => handleDeactivate(user.id)}>Deactivate</button>
                      )}
                    </td>
                  </tr>
                )) : (
                  <tr><td colSpan="7" className="text-center">No users found.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
};

export default Users;
