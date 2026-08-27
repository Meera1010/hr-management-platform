import React, { useState, useEffect } from 'react';
import { NavDropdown, Badge, Button, ListGroup } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { getNotifications, markNotificationRead, markAllNotificationsRead } from '../services/api';

const NotificationsDropdown = () => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 15000); // refresh every 15s
    return () => clearInterval(interval);
  }, []);

  const fetchNotifications = async () => {
    try {
      const res = await getNotifications();
      if (res && res.success) {
        setNotifications(res.data || []);
        setUnreadCount(res.unread_count || 0);
      }
    } catch (e) {
      console.error("Notifications error", e);
    }
  };

  const handleMarkRead = async (id, e) => {
    e.stopPropagation();
    try {
      await markNotificationRead(id);
      fetchNotifications();
    } catch (err) {
      console.error(err);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await markAllNotificationsRead();
      fetchNotifications();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <NavDropdown
      title={
        <span>
          🔔
          {unreadCount > 0 && (
            <Badge bg="danger" pill className="ms-1" style={{ fontSize: '0.7rem' }}>
              {unreadCount}
            </Badge>
          )}
        </span>
      }
      id="notifications-dropdown"
      align="end"
      className="me-2"
    >
      <div className="p-2 border-bottom d-flex justify-content-between align-items-center" style={{ minWidth: '300px' }}>
        <strong>Notifications</strong>
        {unreadCount > 0 && (
          <Button variant="link" size="sm" className="p-0 text-decoration-none" onClick={handleMarkAllRead}>
            Mark all read
          </Button>
        )}
      </div>

      <ListGroup variant="flush" style={{ maxHeight: '300px', overflowY: 'auto' }}>
        {notifications.length === 0 ? (
          <ListGroup.Item className="text-muted text-center py-3">No notifications</ListGroup.Item>
        ) : (
          notifications.slice(0, 5).map(n => (
            <ListGroup.Item
              key={n.id}
              className={`p-2 ${!n.is_read ? 'bg-light font-weight-bold' : ''}`}
            >
              <div className="d-flex justify-content-between align-items-start">
                <div>
                  <div style={{ fontSize: '0.85rem', fontWeight: n.is_read ? 'normal' : 'bold' }}>{n.title}</div>
                  <div style={{ fontSize: '0.75rem' }} className="text-secondary">{n.message}</div>
                </div>
                {!n.is_read && (
                  <Button variant="outline-secondary" size="sm" style={{ fontSize: '0.65rem' }} onClick={(e) => handleMarkRead(n.id, e)}>
                    ✓
                  </Button>
                )}
              </div>
            </ListGroup.Item>
          ))
        )}
      </ListGroup>

      <div className="p-2 border-top text-center">
        <Link to="/notifications" className="text-decoration-none" style={{ fontSize: '0.85rem' }}>
          View all notifications
        </Link>
      </div>
    </NavDropdown>
  );
};

export default NotificationsDropdown;
