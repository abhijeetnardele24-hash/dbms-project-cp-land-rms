"""
Tax Assessment model for property tax calculations and records.
"""

from datetime import datetime
from app.models import db


class TaxAssessment(db.Model):
    """
    Tax assessment model for property tax calculations.
    """
    
    __tablename__ = 'tax_assessments'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Property reference
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    
    # Assessment details
    assessment_year = db.Column(db.Integer, nullable=False, index=True)
    assessment_date = db.Column(db.Date, nullable=False)
    assessed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Valuation
    assessed_value = db.Column(db.Float, nullable=False)  # Property value for tax calculation
    previous_assessed_value = db.Column(db.Float)
    
    # Tax calculation
    tax_rate = db.Column(db.Float, nullable=False)  # Tax rate (percentage)
    annual_tax = db.Column(db.Float, nullable=False)  # Calculated annual tax
    
    # Payment tracking
    tax_paid = db.Column(db.Float, default=0.0)
    tax_due = db.Column(db.Float)
    
    # Due dates
    due_date = db.Column(db.Date)
    last_payment_date = db.Column(db.Date)
    
    # Penalty
    penalty_amount = db.Column(db.Float, default=0.0)
    penalty_reason = db.Column(db.Text)
    
    # Status
    status = db.Column(db.Enum('pending', 'paid', 'partially_paid', 'overdue', 
                              name='tax_status'), default='pending')
    
    # Additional information
    remarks = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = db.relationship('Property', back_populates='tax_assessments')
    assessor = db.relationship('User', foreign_keys=[assessed_by])
    
    def calculate_tax_due(self):
        """Calculate remaining tax due."""
        self.tax_due = (self.annual_tax + self.penalty_amount) - self.tax_paid
        return self.tax_due
    
    def is_overdue(self):
        """Check if tax payment is overdue."""
        if self.due_date and datetime.utcnow().date() > self.due_date:
            return True
        return False
    
    def calculate_penalty(self, penalty_rate=0.02):
        """Calculate penalty for late payment."""
        if self.is_overdue() and self.tax_due > 0:
            # Calculate months overdue
            months_overdue = (datetime.utcnow().date().year - self.due_date.year) * 12 + \
                           (datetime.utcnow().date().month - self.due_date.month)
            
            self.penalty_amount = self.tax_due * penalty_rate * max(1, months_overdue)
            return self.penalty_amount
        return 0.0
    
    def __repr__(self):
        return f'<TaxAssessment Property {self.property_id} Year {self.assessment_year}>'
    
    def to_dict(self):
        """Convert tax assessment object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'assessment_year': self.assessment_year,
            'assessed_value': self.assessed_value,
            'annual_tax': self.annual_tax,
            'tax_paid': self.tax_paid,
            'tax_due': self.tax_due,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None
        }
