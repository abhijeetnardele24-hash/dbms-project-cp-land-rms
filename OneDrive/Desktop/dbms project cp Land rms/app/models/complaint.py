'''Complaint/Grievance model'''
from datetime import datetime
from app.models import db

class Complaint(db.Model):
    __tablename__ = 'complaints'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Complainant
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Complaint details
    category = db.Column(db.Enum('property', 'service', 'staff', 'technical', 'corruption',
                                'delay', 'documentation', 'other', name='complaint_categories'),
                        nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # References
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), index=True)
    mutation_id = db.Column(db.Integer, db.ForeignKey('mutations.id'), index=True)
    
    # Priority and status
    priority = db.Column(db.Enum('low', 'medium', 'high', 'critical', name='complaint_priority_types'),
                        default='medium', index=True)
    status = db.Column(db.Enum('submitted', 'acknowledged', 'investigating', 'in_progress',
                              'resolved', 'closed', 'escalated', name='complaint_status_types'),
                      default='submitted', index=True)
    
    # Assignment
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    assigned_at = db.Column(db.DateTime)
    
    # Resolution
    resolution_details = db.Column(db.Text)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    
    # Satisfaction
    satisfaction_rating = db.Column(db.Integer)  # 1-5 stars
    feedback = db.Column(db.Text)
    
    # Evidence
    attachments = db.Column(db.Text)  # JSON array
    
    # Timestamps
    filed_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], back_populates='complaints')
    property = db.relationship('Property')
    mutation = db.relationship('Mutation')
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    resolver = db.relationship('User', foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f'<Complaint {self.complaint_number} - {self.status}>'
