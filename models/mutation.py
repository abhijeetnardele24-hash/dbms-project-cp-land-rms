from . import db
from datetime import datetime

class Mutation(db.Model):
    __tablename__ = 'mutation'
    
    mutation_id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.parcel_id'), nullable=False)
    from_owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), nullable=False)
    to_owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), nullable=False)
    mutation_type = db.Column(db.Enum('Sale', 'Gift', 'Inheritance', 'Lease Transfer', 'Government Acquisition', name='mutation_type_enum'), nullable=False)
    date_of_mutation = db.Column(db.Date, nullable=False)
    consideration_value = db.Column(db.Numeric(15, 2))
    approved_by = db.Column(db.Integer, db.ForeignKey('user_account.user_id'))
    approved_on = db.Column(db.Date)
    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected', name='mutation_status_enum'), nullable=False, default='Pending')
    document_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    document = db.relationship('Document', backref='mutations', lazy=True)
    
    def __repr__(self):
        return f'<Mutation {self.mutation_id} - {self.mutation_type} - {self.status}>'
