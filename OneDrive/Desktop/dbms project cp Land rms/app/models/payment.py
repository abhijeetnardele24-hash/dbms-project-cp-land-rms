"""
Payment model for property tax and other fee payments.
"""

from datetime import datetime
from app.models import db


class Payment(db.Model):
    """
    Payment model for tax and fee transactions.
    """
    
    __tablename__ = 'payments'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Payment reference number
    payment_reference = db.Column(db.String(50), unique=True, nullable=False, index=True)
    transaction_id = db.Column(db.String(100), unique=True)  # External payment gateway ID
    
    # User and property reference
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), index=True)
    
    # Payment details
    payment_type = db.Column(db.Enum('property_tax', 'mutation_fee', 'registration_fee',
                                    'penalty', 'other', name='payment_types'),
                            nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tax_year = db.Column(db.Integer)  # For property tax payments
    
    # Payment method
    payment_method = db.Column(db.Enum('online', 'cash', 'cheque', 'dd', 'card', 
                                      name='payment_methods'))
    payment_mode_details = db.Column(db.String(200))  # Cheque number, card last 4 digits, etc.
    
    # Status
    status = db.Column(db.Enum('pending', 'processing', 'completed', 'failed', 
                              'refunded', name='payment_status_types'),
                      default='pending', nullable=False, index=True)
    
    # Dates
    payment_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_date = db.Column(db.DateTime)
    
    # Receipt
    receipt_number = db.Column(db.String(50), unique=True)
    receipt_issued_date = db.Column(db.DateTime)
    
    # Additional information
    description = db.Column(db.Text)
    remarks = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Relationships
    user = db.relationship('User', back_populates='payments')
    property = db.relationship('Property', back_populates='payments')
    
    def generate_payment_reference(self):
        """Generate unique payment reference number."""
        if self.payment_reference:
            return self.payment_reference
        
        year = datetime.utcnow().year
        self.payment_reference = f"PAY{year}{self.id:08d}"
        return self.payment_reference
    
    def generate_receipt_number(self):
        """Generate receipt number after successful payment."""
        if self.receipt_number:
            return self.receipt_number
        
        year = datetime.utcnow().year
        month = datetime.utcnow().month
        self.receipt_number = f"REC{year}{month:02d}{self.id:06d}"
        return self.receipt_number
    
    def is_completed(self):
        """Check if payment is successfully completed."""
        return self.status == 'completed'
    
    def __repr__(self):
        return f'<Payment {self.payment_reference} - {self.amount} ({self.status})>'
    
    def to_dict(self):
        """Convert payment object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'payment_reference': self.payment_reference,
            'transaction_id': self.transaction_id,
            'payment_type': self.payment_type,
            'amount': self.amount,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'receipt_number': self.receipt_number
        }
