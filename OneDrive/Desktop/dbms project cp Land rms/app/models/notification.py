"""
Notification model for in-app and email notifications.
"""

from datetime import datetime
from app.models import db


class Notification(db.Model):
    """
    Notification model for user notifications.
    Supports both in-app and email notifications.
    """
    
    __tablename__ = 'notifications'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User reference
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Notification details
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.Enum('info', 'success', 'warning', 'error', 
                                         'property_approved', 'property_rejected',
                                         'mutation_approved', 'mutation_rejected',
                                         'payment_confirmed', 'document_required',
                                         'system_announcement', name='notification_types'),
                                   default='info')
    
    # Link to related entities
    related_entity_type = db.Column(db.String(50))  # 'property', 'mutation', 'payment'
    related_entity_id = db.Column(db.Integer)
    
    # Status
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    read_at = db.Column(db.DateTime)
    
    # Email notification
    email_sent = db.Column(db.Boolean, default=False)
    email_sent_at = db.Column(db.DateTime)
    
    # Priority
    priority = db.Column(db.Enum('low', 'normal', 'high', name='notification_priority'),
                        default='normal')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = db.relationship('User', back_populates='notifications')
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.read_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Notification {self.title} for User {self.user_id}>'
    
    def to_dict(self):
        """Convert notification object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'is_read': self.is_read,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
