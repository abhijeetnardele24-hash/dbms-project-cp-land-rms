"""
Document model for property-related documents and attachments.
"""

from datetime import datetime
from app.models import db


class Document(db.Model):
    """
    Property document model for storing uploaded documents.
    """
    
    __tablename__ = 'documents'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Property reference
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    
    # Document details
    document_name = db.Column(db.String(200), nullable=False)
    document_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'))
    description = db.Column(db.Text)
    
    # File details
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    file_type = db.Column(db.String(50))  # pdf, jpg, png
    
    # Upload details
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Verification status
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    verification_notes = db.Column(db.Text)
    
    # Version control
    version = db.Column(db.Integer, default=1)
    replaced_by = db.Column(db.Integer, db.ForeignKey('documents.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = db.relationship('Property', back_populates='documents')
    document_type = db.relationship('DocumentType', backref='documents')
    uploader = db.relationship('User', foreign_keys=[uploaded_by])
    verifier = db.relationship('User', foreign_keys=[verified_by])
    
    def __repr__(self):
        return f'<Document {self.document_name} for Property {self.property_id}>'
    
    def to_dict(self):
        """Convert document object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'document_name': self.document_name,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'is_verified': self.is_verified,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None
        }
