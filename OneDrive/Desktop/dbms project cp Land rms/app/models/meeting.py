'''Meeting/Appointment scheduling model'''
from datetime import datetime
from app.models import db

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    meeting_type = db.Column(db.Enum('inspection', 'consultation', 'hearing', 
                                    'review', 'site_visit', name='meeting_types'))
    
    # Scheduling
    scheduled_datetime = db.Column(db.DateTime, nullable=False, index=True)
    duration_minutes = db.Column(db.Integer, default=60)
    location = db.Column(db.String(500))
    meeting_link = db.Column(db.String(500))  # For online meetings
    
    # Participants
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    participants = db.Column(db.Text)  # JSON array of user_ids
    
    # References
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), index=True)
    mutation_id = db.Column(db.Integer, db.ForeignKey('mutations.id'), index=True)
    
    # Status
    status = db.Column(db.Enum('scheduled', 'in_progress', 'completed', 'cancelled',
                              'rescheduled', name='meeting_status_types'),
                      default='scheduled', index=True)
    
    # Meeting notes
    agenda = db.Column(db.Text)
    minutes = db.Column(db.Text)
    decisions = db.Column(db.Text)
    action_items = db.Column(db.Text)  # JSON array
    
    # Attachments
    attachments = db.Column(db.Text)  # JSON array
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organizer = db.relationship('User')
    property = db.relationship('Property')
    mutation = db.relationship('Mutation')
    
    def __repr__(self):
        return f'<Meeting {self.title} - {self.scheduled_datetime}>'
