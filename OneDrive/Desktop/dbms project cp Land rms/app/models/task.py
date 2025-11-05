'''
Task Management model for workflow and assignments.
'''

from datetime import datetime
from app.models import db


class Task(db.Model):
    '''
    Task assignment and workflow management.
    '''
    
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Assignment
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Task details
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    task_type = db.Column(db.Enum('inspection', 'verification', 'approval', 'review',
                                  'valuation', 'meeting', 'other', name='task_types'))
    priority = db.Column(db.Enum('low', 'medium', 'high', 'urgent', name='priority_types'),
                        default='medium', index=True)
    
    # References
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), index=True)
    mutation_id = db.Column(db.Integer, db.ForeignKey('mutations.id'), index=True)
    
    # Status
    status = db.Column(db.Enum('pending', 'in_progress', 'completed', 'cancelled',
                              'on_hold', name='task_status_types'),
                      default='pending', index=True)
    
    # Dates
    due_date = db.Column(db.DateTime, index=True)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Results
    completion_notes = db.Column(db.Text)
    attachments = db.Column(db.Text)  # JSON array
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    assigner = db.relationship('User', foreign_keys=[assigned_by])
    property = db.relationship('Property')
    mutation = db.relationship('Mutation')
    
    def __repr__(self):
        return f'<Task {self.title} - {self.status}>'
