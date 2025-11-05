"""
Message model for internal user communication.
"""

from datetime import datetime
from app.models import db


class Message(db.Model):
    """
    Internal messaging system between users.
    """
    
    __tablename__ = 'messages'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Participants
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Message details
    subject = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.Enum('normal', 'urgent', 'notification', 'system',
                                    name='message_types'), default='normal')
    
    # References
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), index=True)
    mutation_id = db.Column(db.Integer, db.ForeignKey('mutations.id'), index=True)
    
    # Status tracking
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    read_at = db.Column(db.DateTime)
    is_starred = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)
    
    # Reply tracking
    parent_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), index=True)
    
    # Attachments
    attachments = db.Column(db.Text)  # JSON array of file paths
    
    # Timestamps
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')
    property = db.relationship('Property')
    mutation = db.relationship('Mutation')
    parent = db.relationship('Message', remote_side=[id], backref='replies')
    
    def __repr__(self):
        return f'<Message from User#{self.sender_id} to User#{self.receiver_id}>'
