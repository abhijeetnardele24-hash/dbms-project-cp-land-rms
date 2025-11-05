"""
Mutation model for property ownership changes and transfers.
Handles the workflow from citizen request to officer approval.
"""

from datetime import datetime
from app.models import db


class Mutation(db.Model):
    """
    Mutation request model for ownership changes.
    Tracks the complete workflow from request to approval/rejection.
    """
    
    __tablename__ = 'mutations'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Mutation reference number
    mutation_number = db.Column(db.String(50), unique=True, index=True)
    
    # Property reference
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    
    # Requester (citizen who submitted the mutation request)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Mutation type
    mutation_type = db.Column(db.Enum('sale', 'inheritance', 'gift', 'partition', 
                                     'transfer', 'addition', 'removal', 'correction',
                                     name='mutation_types'), nullable=False)
    
    # Details of mutation
    description = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text)
    
    # Previous and new owner details
    previous_owners = db.Column(db.Text)  # JSON or comma-separated list
    new_owners = db.Column(db.Text)  # JSON or comma-separated list
    
    # Status workflow
    status = db.Column(db.Enum('pending', 'under_review', 'documents_verified',
                              'information_required', 'approved', 'rejected',
                              name='mutation_status'), default='pending', 
                      nullable=False, index=True)
    
    # Processing details
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Officer who processed
    processing_date = db.Column(db.DateTime)
    approval_date = db.Column(db.DateTime)
    rejection_date = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    
    # Officer comments and feedback
    officer_comments = db.Column(db.Text)
    additional_info_required = db.Column(db.Text)
    citizen_response = db.Column(db.Text)
    
    # Mutation certificate
    mutation_certificate_number = db.Column(db.String(50), unique=True)
    certificate_issued_date = db.Column(db.DateTime)
    
    # Fee and payment
    mutation_fee = db.Column(db.Float, default=0.0)
    payment_status = db.Column(db.Enum('pending', 'paid', 'exempted', name='payment_status_enum'),
                              default='pending')
    
    # Priority and escalation
    priority = db.Column(db.Enum('low', 'normal', 'high', 'urgent', name='priority_levels'),
                        default='normal')
    escalated = db.Column(db.Boolean, default=False)
    escalation_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False, index=True)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Relationships
    property = db.relationship('Property', back_populates='mutations')
    requester = db.relationship('User', back_populates='mutations_requested',
                               foreign_keys=[requester_id])
    processed_by_user = db.relationship('User', back_populates='mutations_processed',
                                       foreign_keys=[processed_by])
    documents = db.relationship('MutationDocument', back_populates='mutation',
                               cascade='all, delete-orphan', lazy='dynamic')
    
    def generate_mutation_number(self):
        """Generate unique mutation reference number."""
        if self.mutation_number:
            return self.mutation_number
        
        year = datetime.utcnow().year
        self.mutation_number = f"MUT{year}{self.id:06d}"
        return self.mutation_number
    
    def generate_certificate_number(self):
        """Generate mutation certificate number after approval."""
        if self.mutation_certificate_number:
            return self.mutation_certificate_number
        
        year = datetime.utcnow().year
        self.mutation_certificate_number = f"MC{year}{self.id:06d}"
        return self.mutation_certificate_number
    
    def is_pending(self):
        """Check if mutation is awaiting processing."""
        return self.status in ['pending', 'under_review', 'documents_verified', 
                              'information_required']
    
    def is_approved(self):
        """Check if mutation is approved."""
        return self.status == 'approved'
    
    def is_rejected(self):
        """Check if mutation is rejected."""
        return self.status == 'rejected'
    
    def days_pending(self):
        """Calculate number of days mutation has been pending."""
        if self.is_approved() or self.is_rejected():
            return 0
        
        return (datetime.utcnow() - self.created_at).days
    
    def __repr__(self):
        return f'<Mutation {self.mutation_number} - {self.mutation_type} ({self.status})>'
    
    def to_dict(self):
        """Convert mutation object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'mutation_number': self.mutation_number,
            'property_id': self.property_id,
            'mutation_type': self.mutation_type,
            'status': self.status,
            'description': self.description,
            'priority': self.priority,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None
        }


class MutationDocument(db.Model):
    """
    Documents attached to mutation requests.
    """
    
    __tablename__ = 'mutation_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    mutation_id = db.Column(db.Integer, db.ForeignKey('mutations.id'), nullable=False, index=True)
    
    document_name = db.Column(db.String(200), nullable=False)
    document_type = db.Column(db.String(100))  # sale_deed, will, gift_deed, etc.
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    mutation = db.relationship('Mutation', back_populates='documents')
    
    def __repr__(self):
        return f'<MutationDocument {self.document_name}>'
