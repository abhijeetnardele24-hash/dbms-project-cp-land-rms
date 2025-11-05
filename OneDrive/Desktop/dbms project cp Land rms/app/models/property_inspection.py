"""
Property Inspection model for tracking physical property inspections.
"""

from datetime import datetime
from app.models import db


class PropertyInspection(db.Model):
    """
    Track property inspections conducted by officers.
    """
    
    __tablename__ = 'property_inspections'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # References
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    inspector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Inspection details
    inspection_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    inspection_type = db.Column(db.Enum('initial', 'verification', 'mutation', 'complaint',
                                       'periodic', 'valuation', 'legal', name='inspection_types'),
                                nullable=False)
    
    # Scheduling
    scheduled_date = db.Column(db.DateTime, nullable=False, index=True)
    actual_date = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    
    # Status
    status = db.Column(db.Enum('scheduled', 'in_progress', 'completed', 'cancelled',
                              'rescheduled', name='inspection_status_types'),
                      default='scheduled', nullable=False, index=True)
    
    # Findings
    current_usage = db.Column(db.String(200))
    occupancy_status = db.Column(db.Enum('owner_occupied', 'tenant_occupied', 'vacant',
                                        'under_construction', 'disputed', name='occupancy_types'))
    condition = db.Column(db.Enum('excellent', 'good', 'fair', 'poor', 'dilapidated',
                                  name='property_conditions'))
    
    # Physical verification
    boundary_verified = db.Column(db.Boolean, default=False)
    area_verified = db.Column(db.Boolean, default=False)
    documents_verified = db.Column(db.Boolean, default=False)
    ownership_verified = db.Column(db.Boolean, default=False)
    
    # Measurements
    measured_length = db.Column(db.Float)
    measured_width = db.Column(db.Float)
    measured_area = db.Column(db.Float)
    area_deviation_percentage = db.Column(db.Float)
    
    # Observations
    observations = db.Column(db.Text)
    discrepancies = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    
    # Media
    photos = db.Column(db.Text)  # JSON array of photo paths
    videos = db.Column(db.Text)  # JSON array of video paths
    documents = db.Column(db.Text)  # JSON array of document paths
    
    # GPS Coordinates
    gps_latitude = db.Column(db.Float)
    gps_longitude = db.Column(db.Float)
    gps_accuracy = db.Column(db.Float)
    
    # Report
    report_file = db.Column(db.String(500))
    report_generated_at = db.Column(db.DateTime)
    
    # Approval
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approval_date = db.Column(db.DateTime)
    approval_remarks = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = db.relationship('Property', back_populates='inspections')
    inspector = db.relationship('User', foreign_keys=[inspector_id])
    requester = db.relationship('User', foreign_keys=[requested_by])
    approver = db.relationship('User', foreign_keys=[approved_by])
    
    def __repr__(self):
        return f'<PropertyInspection {self.inspection_number} - {self.status}>'
