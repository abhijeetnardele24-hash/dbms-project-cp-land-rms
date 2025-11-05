"""
Ownership model - Many-to-many relationship between Property and Owner.
Supports joint ownership with ownership percentages.
"""

from datetime import datetime
from app.models import db


class Ownership(db.Model):
    """
    Property-Owner relationship model with ownership details.
    Supports single and joint ownership with percentage shares.
    """
    
    __tablename__ = 'ownerships'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign keys
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False, index=True)
    
    # Ownership details
    ownership_percentage = db.Column(db.Float, default=100.0, nullable=False)  # 0-100%
    ownership_type = db.Column(db.Enum('sole', 'joint', 'partial', name='ownership_type_enum'),
                              default='sole')
    
    # Acquisition details
    acquisition_date = db.Column(db.Date, nullable=False)
    acquisition_mode = db.Column(db.Enum('purchase', 'inheritance', 'gift', 'partition',
                                        'court_order', 'government_allotment', 'other',
                                        name='acquisition_modes'))
    acquisition_document = db.Column(db.String(200))  # Reference to document
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    end_date = db.Column(db.Date)  # When ownership ended
    
    # Additional information
    remarks = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = db.relationship('Property', back_populates='ownerships')
    owner = db.relationship('Owner', back_populates='ownerships')
    
    def __repr__(self):
        return f'<Ownership Property:{self.property_id} Owner:{self.owner_id} ({self.ownership_percentage}%)>'
    
    def to_dict(self):
        """Convert ownership object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'owner_id': self.owner_id,
            'ownership_percentage': self.ownership_percentage,
            'ownership_type': self.ownership_type,
            'acquisition_date': self.acquisition_date.isoformat() if self.acquisition_date else None,
            'acquisition_mode': self.acquisition_mode,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
