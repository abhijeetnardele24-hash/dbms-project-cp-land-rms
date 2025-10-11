from . import db
from datetime import datetime

class Encumbrance(db.Model):
    __tablename__ = 'encumbrance'
    
    encumbrance_id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.parcel_id'), nullable=False)
    type = db.Column(db.Enum('Mortgage', 'Lien', 'Court Case', 'Dispute', 'Tax Dues', name='encumbrance_type_enum'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    related_party_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'))
    case_number = db.Column(db.String(100))
    status = db.Column(db.Enum('Active', 'Resolved', name='encumbrance_status_enum'), nullable=False, default='Active')
    document_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    document = db.relationship('Document', backref='encumbrances', lazy=True)
    
    def __repr__(self):
        return f'<Encumbrance {self.encumbrance_id} - {self.type} - {self.status}>'
