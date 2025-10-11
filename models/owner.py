from . import db
from datetime import datetime
from utils.encryption import aadhaar_crypto

class Owner(db.Model):
    __tablename__ = 'owner'
    
    owner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    owner_type = db.Column(db.Enum('Individual', 'Company', 'Government', name='owner_type_enum'), nullable=False)
    aadhaar_encrypted = db.Column(db.String(255))
    pan = db.Column(db.String(10))
    address = db.Column(db.Text)
    contact_no = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ownerships = db.relationship('Ownership', backref='owner', lazy=True)
    tenant_agreements_as_owner = db.relationship('TenantAgreement', foreign_keys='TenantAgreement.owner_id', backref='property_owner', lazy=True)
    tenant_agreements_as_tenant = db.relationship('TenantAgreement', foreign_keys='TenantAgreement.tenant_id', backref='tenant', lazy=True)
    mutations_from = db.relationship('Mutation', foreign_keys='Mutation.from_owner_id', backref='from_owner', lazy=True)
    mutations_to = db.relationship('Mutation', foreign_keys='Mutation.to_owner_id', backref='to_owner', lazy=True)
    encumbrances = db.relationship('Encumbrance', backref='related_party', lazy=True)
    
    def set_aadhaar(self, aadhaar_number):
        """Encrypt and store Aadhaar number"""
        if aadhaar_number:
            self.aadhaar_encrypted = aadhaar_crypto.encrypt_aadhaar(aadhaar_number)
    
    def get_aadhaar(self):
        """Decrypt and return Aadhaar number"""
        if self.aadhaar_encrypted:
            try:
                return aadhaar_crypto.decrypt_aadhaar(self.aadhaar_encrypted)
            except Exception as e:
                print(f"Aadhaar decryption error for owner {self.owner_id}: {str(e)}")
                return None
        return None
    
    def get_masked_aadhaar(self):
        """Get masked Aadhaar for display"""
        try:
            aadhaar = self.get_aadhaar()
            if aadhaar:
                return aadhaar_crypto.mask_aadhaar(aadhaar)
        except Exception as e:
            print(f"Aadhaar masking error for owner {self.owner_id}: {str(e)}")
        return "XXXX-XXXX-XXXX"
    
    def __repr__(self):
        return f'<Owner {self.name}>'
