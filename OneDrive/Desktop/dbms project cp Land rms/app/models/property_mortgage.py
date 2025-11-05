'''Property Mortgage/Loan model'''
from datetime import datetime
from app.models import db

class PropertyMortgage(db.Model):
    __tablename__ = 'property_mortgages'
    
    id = db.Column(db.Integer, primary_key=True)
    mortgage_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Property and parties
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Lender information
    lender_name = db.Column(db.String(300), nullable=False)
    lender_type = db.Column(db.Enum('bank', 'nbfc', 'private', 'government', name='lender_types'))
    lender_branch = db.Column(db.String(300))
    loan_account_number = db.Column(db.String(100))
    
    # Loan details
    loan_amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float)
    tenure_months = db.Column(db.Integer)
    monthly_emi = db.Column(db.Float)
    
    # Dates
    sanction_date = db.Column(db.Date, nullable=False)
    disbursement_date = db.Column(db.Date)
    maturity_date = db.Column(db.Date)
    
    # Status
    status = db.Column(db.Enum('sanctioned', 'active', 'paid', 'npa', 'foreclosed',
                              name='mortgage_status_types'), default='sanctioned', index=True)
    
    # Outstanding
    outstanding_amount = db.Column(db.Float)
    last_payment_date = db.Column(db.Date)
    
    # Documents
    documents = db.Column(db.Text)  # JSON array
    
    # Legal
    registered_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    registration_date = db.Column(db.Date)
    release_date = db.Column(db.Date)
    release_document = db.Column(db.String(500))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = db.relationship('Property', back_populates='mortgages')
    borrower = db.relationship('User', foreign_keys=[borrower_id])
    registrar = db.relationship('User', foreign_keys=[registered_by])
    
    def __repr__(self):
        return f'<PropertyMortgage {self.mortgage_number} - {self.status}>'
