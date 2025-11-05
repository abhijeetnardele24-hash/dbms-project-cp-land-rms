"""
Owner model for property owners.
An owner can be linked to a user account (for citizens) or be a standalone record.
"""

from datetime import datetime
from app.models import db


class Owner(db.Model):
    """
    Property owner model.
    Can be linked to a user account or exist independently.
    """
    
    __tablename__ = 'owners'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Link to user account (optional - for citizens with accounts)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    # Owner details
    full_name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('male', 'female', 'other', name='gender_types'))
    
    # Identification
    aadhar_number = db.Column(db.String(12), unique=True, index=True)
    pan_number = db.Column(db.String(10), unique=True, index=True)
    
    # Contact details
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    
    # Owner type
    owner_type = db.Column(db.Enum('individual', 'joint', 'company', 'trust', 
                                   'government', name='owner_types'),
                          default='individual')
    
    # Additional information
    occupation = db.Column(db.String(100))
    remarks = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='properties_owned')
    ownerships = db.relationship('Ownership', back_populates='owner', 
                                cascade='all, delete-orphan', lazy='dynamic')
    
    def get_properties(self):
        """Get all properties owned by this owner."""
        return [ownership.property for ownership in 
                self.ownerships.filter_by(is_active=True).all()]
    
    def get_total_properties_count(self):
        """Get total count of active properties."""
        return self.ownerships.filter_by(is_active=True).count()
    
    def __repr__(self):
        return f'<Owner {self.full_name}>'
    
    def to_dict(self):
        """Convert owner object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'phone': self.phone,
            'email': self.email,
            'owner_type': self.owner_type,
            'aadhar_number': self.aadhar_number[-4:] if self.aadhar_number else None,  # Masked
            'pan_number': self.pan_number,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
