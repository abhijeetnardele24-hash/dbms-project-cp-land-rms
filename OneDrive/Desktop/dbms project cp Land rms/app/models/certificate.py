'''Certificate issuance tracking model'''
from datetime import datetime
from app.models import db

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    certificate_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Type and purpose
    certificate_type = db.Column(db.Enum('ownership', 'encumbrance', 'tax_clearance', 
                                        'no_dues', 'mutation', 'valuation', 'inheritance',
                                        name='certificate_types'), nullable=False)
    
    # References
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    mutation_id = db.Column(db.Integer, db.ForeignKey('mutations.id'), index=True)
    
    # Issuance details
    issued_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    valid_until = db.Column(db.Date)
    
    # Content
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    certificate_data = db.Column(db.Text)  # JSON with cert details
    
    # Document
    certificate_file = db.Column(db.String(500))
    qr_code = db.Column(db.String(500))  # QR code for verification
    digital_signature = db.Column(db.Text)
    
    # Status
    status = db.Column(db.Enum('active', 'expired', 'revoked', 'suspended',
                              name='certificate_status_types'), default='active', index=True)
    revoked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    revoked_at = db.Column(db.DateTime)
    revocation_reason = db.Column(db.Text)
    
    # Verification
    verification_code = db.Column(db.String(100), unique=True, index=True)
    times_verified = db.Column(db.Integer, default=0)
    last_verified_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = db.relationship('Property')
    user = db.relationship('User', foreign_keys=[user_id])
    issuer = db.relationship('User', foreign_keys=[issued_by])
    revoker = db.relationship('User', foreign_keys=[revoked_by])
    mutation = db.relationship('Mutation')
    
    def __repr__(self):
        return f'<Certificate {self.certificate_number} - {self.certificate_type}>'
