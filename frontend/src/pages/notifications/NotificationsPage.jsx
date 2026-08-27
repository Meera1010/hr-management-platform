import React, { useState, useEffect } from 'react';
import { Container, Card, ListGroup, Button, Badge, Spinner, Alert } from 'react-bootstrap';
import { getNotifications, markNotificationRead, markAllNotificationsRead, deleteNotification } from '../../services/api';

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const res = await getNotifications();
      if (res && res.success) {
        setNotifications(res.data || []);
      }
    } catch (err) {
      setError(err.message || 'Failed to load notifications');
    } finally {
      setLoading(false);
    }
  };

  const handleRead = async (id) => {
    try {
      await markNotificationRead(id);
      fetchNotifications();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleReadAll = async () => {
    try {
      await markAllNotificationsRead();
      fetchNotifications();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteNotification(id);
      fetchNotifications();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2>Notifications Center</h2>
          <p className="text-muted">Stay updated on your requests, workflow status changes, and announcements.</p>
        </div>
        <Button variant="outline-primary" onClick={handleReadAll}>
          Mark All as Read
        </Button>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      <Card className="shadow-sm">
        <Card.Body className="p-0">
          <ListGroup variant="flush">
            {loading ? (
              <div className="text-center py-4"><Spinner animation="border" /></div>
            ) : notifications.length === 0 ? (
              <div className="text-center py-4 text-muted">No notifications found.</div>
            ) : (
              notifications.map(n => (
                <ListGroup.Item
                  key={n.id}
                  className={`p-3 d-flex justify-content-between align-items-center ${!n.is_read ? 'bg-light' : ''}`}
                >
                  <div>
                    <div className="d-flex align-items-center gap-2">
                      <span className="fw-bold">{n.title}</span>
                      {!n.is_read && <Badge bg="primary" pill>New</Badge>}
                      <small className="text-muted">{n.created_at ? new Date(n.created_at).toLocaleString() : ''}</small>
                    </div>
                    <p className="mb-0 mt-1 text-secondary">{n.message}</p>
                  </div>
                  <div className="d-flex gap-2">
                    {!n.is_read && (
                      <Button size="sm" variant="outline-success" onClick={() => handleRead(n.id)}>
                        Mark Read
                      </Button>
                    )}
                    <Button size="sm" variant="outline-danger" onClick={() => handleDelete(n.id)}>
                      Dismiss
                    </Button>
                  </div>
                </ListGroup.Item>
              ))
            )}
          </ListGroup>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default NotificationsPage;
