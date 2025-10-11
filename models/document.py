from . import db
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'document'
    
    document_id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.Enum('Sale Deed', 'Lease Deed', 'Mutation Record', 'Encumbrance', 'Tax Receipt', name='doc_type_enum'), nullable=False)
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(500))
    registered_at = db.Column(db.DateTime)
    registration_office = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Document {self.document_id} - {self.doc_type}>'
