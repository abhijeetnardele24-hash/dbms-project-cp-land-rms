"""
Audit Log model for tracking all critical system operations.
"""

from datetime import datetime
from app.models import db


class AuditLog(db.Model):
    """
    Audit trail for all critical system operations.
    Records user actions for security and compliance.
    """
    
    __tablename__ = 'audit_logs'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User reference
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    
    # Action details
    action = db.Column(db.String(100), nullable=False, index=True)  # login, create_property, approve_mutation, etc.
    action_type = db.Column(db.Enum('create', 'read', 'update', 'delete', 'approve', 
                                    'reject', 'login', 'logout', 'other', 
                                    name='action_types'),
                           nullable=False)
    
    # Entity details
    entity_type = db.Column(db.String(50))  # property, mutation, payment, user
    entity_id = db.Column(db.Integer)
    
    # Description and details
    description = db.Column(db.Text)
    old_value = db.Column(db.Text)  # JSON string of old values
    new_value = db.Column(db.Text)  # JSON string of new values
    
    # Request metadata
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.String(500))
    request_method = db.Column(db.String(10))  # GET, POST, PUT, DELETE
    request_url = db.Column(db.String(500))
    
    # Status
    status = db.Column(db.Enum('success', 'failure', 'error', name='audit_status'),
                      default='success')
    error_message = db.Column(db.Text)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), nullable=False, index=True)
    
    # Relationships
    user = db.relationship('User', back_populates='audit_logs')
    
    @staticmethod
    def log_action(user_id, action, action_type='other', entity_type=None, entity_id=None,
                  description=None, old_value=None, new_value=None, ip_address=None,
                  user_agent=None, status='success'):
        """
        Create an audit log entry.
        
        Args:
            user_id: ID of the user performing the action
            action: Name of the action (e.g., 'approve_property')
            action_type: Type of action (create, read, update, delete, etc.)
            entity_type: Type of entity affected (property, mutation, etc.)
            entity_id: ID of the entity affected
            description: Human-readable description
            old_value: Previous value (for updates)
            new_value: New value (for updates)
            ip_address: User's IP address
            user_agent: User's browser/client
            status: success, failure, or error
        """
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            action_type=action_type,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status
        )
        
        db.session.add(log_entry)
        return log_entry
    
    def __repr__(self):
        return f'<AuditLog {self.action} by User {self.user_id} at {self.created_at}>'
    
    def to_dict(self):
        """Convert audit log object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'action_type': self.action_type,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'description': self.description,
            'status': self.status,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
