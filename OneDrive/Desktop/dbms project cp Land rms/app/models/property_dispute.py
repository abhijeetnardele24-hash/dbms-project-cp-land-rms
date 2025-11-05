'''Property Dispute model'''
from datetime import datetime
from app.models import db

class PropertyDispute(db.Model):
    __tablename__ = 'property_disputes'
    
    id = db.Column(db.Integer, primary_key=True)
    dispute_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Property and parties
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    complainant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    respondent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Dispute details
    dispute_type = db.Column(db.Enum('ownership', 'boundary', 'inheritance', 'fraud',
                                    'encroachment', 'documentation', 'other', name='dispute_types'))
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Legal
    case_number = db.Column(db.String(200))
    court_name = db.Column(db.String(300))
    lawyer_name = db.Column(db.String(200))
    
    # Status
    status = db.Column(db.Enum('filed', 'under_review', 'investigation', 'hearing_scheduled',
                              'mediation', 'resolved', 'dismissed', 'escalated', name='dispute_status_types'),
                      default='filed', index=True)
    priority = db.Column(db.Enum('low', 'medium', 'high', 'urgent', name='dispute_priority_types'),
                        default='medium')
    
    # Handling
    assigned_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    filed_date = db.Column(db.Date, nullable=False)
    resolution_date = db.Column(db.Date)
    resolution_details = db.Column(db.Text)
    
    # Documents and evidence
    documents = db.Column(db.Text)  # JSON array
    evidence = db.Column(db.Text)  # JSON array
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = db.relationship('Property', back_populates='disputes')
    complainant = db.relationship('User', foreign_keys=[complainant_id])
    respondent = db.relationship('User', foreign_keys=[respondent_id])
    assigned_officer = db.relationship('User', foreign_keys=[assigned_officer_id])
    
    def __repr__(self):
        return f'<PropertyDispute {self.dispute_number} - {self.status}>'
