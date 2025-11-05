"""
Property Valuation model for tracking property values over time.
"""

from datetime import datetime
from app.models import db


class PropertyValuation(db.Model):
    """
    Track property valuations performed by authorized valuers.
    """
    
    __tablename__ = 'property_valuations'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Property reference
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    
    # Valuer information
    valuer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    valuer_name = db.Column(db.String(200), nullable=False)
    valuer_license = db.Column(db.String(100))
    valuation_company = db.Column(db.String(200))
    
    # Valuation details
    valuation_date = db.Column(db.Date, nullable=False, index=True)
    valuation_type = db.Column(db.Enum('market', 'distress', 'forced', 'insurance', 
                                      'mortgage', 'taxation', name='valuation_types'), 
                               nullable=False)
    
    # Values
    land_value = db.Column(db.Float, nullable=False)
    building_value = db.Column(db.Float, default=0.0)
    total_value = db.Column(db.Float, nullable=False)
    
    # Market data
    market_rate_per_sqft = db.Column(db.Float)
    comparable_sales = db.Column(db.Text)  # JSON data of comparable properties
    market_trend = db.Column(db.Enum('rising', 'stable', 'declining', name='market_trends'))
    
    # Report details
    report_number = db.Column(db.String(100), unique=True, index=True)
    report_file = db.Column(db.String(500))
    methodology = db.Column(db.Text)
    remarks = db.Column(db.Text)
    
    # Status
    status = db.Column(db.Enum('draft', 'submitted', 'approved', 'rejected', 
                              name='valuation_status_types'), default='draft')
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approval_date = db.Column(db.DateTime)
    
    # Validity
    valid_until = db.Column(db.Date)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = db.relationship('Property', back_populates='valuations')
    valuer = db.relationship('User', foreign_keys=[valuer_id])
    approver = db.relationship('User', foreign_keys=[approved_by])
    
    def __repr__(self):
        return f'<PropertyValuation {self.report_number} - Rs.{self.total_value}>'
