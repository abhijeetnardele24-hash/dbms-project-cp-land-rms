from . import db
from datetime import datetime

class TenantAgreement(db.Model):
    __tablename__ = 'tenant_agreement'
    
    agreement_id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.parcel_id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    rent_amount = db.Column(db.Numeric(12, 2))
    phone_number = db.Column(db.String(15))
    tenant_name = db.Column(db.String(255))
    deposit_amount = db.Column(db.Numeric(12, 2))
    document_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    document = db.relationship('Document', backref='tenant_agreements', lazy=True)
    
    def __repr__(self):
        return f'<TenantAgreement {self.agreement_id} - Parcel {self.parcel_id}>'
