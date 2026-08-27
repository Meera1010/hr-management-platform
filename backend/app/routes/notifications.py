from flask import Blueprint, jsonify, request
from app import db
from app.models.notification import Notification
from app.utils.auth import token_required

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notifications_bp.route('', methods=['GET'])
@token_required
def get_notifications(current_user):
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(50).all()
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return jsonify({
        'success': True,
        'unread_count': unread_count,
        'count': len(notifs),
        'data': [n.to_dict() for n in notifs]
    }), 200

@notifications_bp.route('/<int:notif_id>/read', methods=['PUT'])
@token_required
def mark_read(current_user, notif_id):
    notif = Notification.query.filter_by(id=notif_id, user_id=current_user.id).first_or_404()
    notif.is_read = True
    db.session.commit()
    return jsonify({'success': True, 'data': notif.to_dict()}), 200

@notifications_bp.route('/read-all', methods=['PUT'])
@token_required
def mark_all_read(current_user):
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True, 'message': 'All notifications marked as read.'}), 200

@notifications_bp.route('/<int:notif_id>', methods=['DELETE'])
@token_required
def delete_notification(current_user, notif_id):
    notif = Notification.query.filter_by(id=notif_id, user_id=current_user.id).first_or_404()
    db.session.delete(notif)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Notification deleted.'}), 200
