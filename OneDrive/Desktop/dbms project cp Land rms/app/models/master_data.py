"""
Master data models for land categories, usage types, document types, and other reference data.
"""

from datetime import datetime
from app.models import db


class LandCategory(db.Model):
    """
    Land category master data (e.g., agricultural, residential, commercial).
    """
    
    __tablename__ = 'land_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    tax_rate = db.Column(db.Float)  # Default tax rate for this category
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LandCategory {self.name}>'


class UsageType(db.Model):
    """
    Land usage type master data (e.g., residential building, farm, warehouse).
    """
    
    __tablename__ = 'usage_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UsageType {self.name}>'


class DocumentType(db.Model):
    """
    Document type master data (e.g., sale deed, will, identity proof).
    """
    
    __tablename__ = 'document_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    is_mandatory = db.Column(db.Boolean, default=False)  # Required for registration
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DocumentType {self.name}>'


class PropertyStatus(db.Model):
    """
    Property status master data for workflow tracking.
    """
    
    __tablename__ = 'property_statuses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    color_code = db.Column(db.String(7))  # Hex color for UI display (e.g., #28a745)
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PropertyStatus {self.name}>'
