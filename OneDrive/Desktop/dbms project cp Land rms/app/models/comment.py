'''
Comment/Discussion model for collaborative feedback.
'''

from datetime import datetime
from app.models import db


class Comment(db.Model):
    '''
    Comments on properties, mutations, and other entities.
    '''
    
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Comment details
    comment_text = db.Column(db.Text, nullable=False)
    comment_type = db.Column(db.Enum('note', 'question', 'issue', 'approval', 'rejection',
                                    name='comment_types'), default='note')
    
    # References - polymorphic
    entity_type = db.Column(db.Enum('property', 'mutation', 'inspection', 'valuation',
                                   name='comment_entity_types'), nullable=False, index=True)
    entity_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Threading
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), index=True)
    
    # Status
    is_internal = db.Column(db.Boolean, default=False)  # Internal staff only
    is_resolved = db.Column(db.Boolean, default=False)
    
    # Attachments
    attachments = db.Column(db.Text)  # JSON array
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='comments')
    parent = db.relationship('Comment', remote_side=[id], backref='replies')
    
    def __repr__(self):
        return f'<Comment by User#{self.user_id} on {self.entity_type}#{self.entity_id}>'
