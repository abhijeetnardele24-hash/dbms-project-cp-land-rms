from . import db
from datetime import datetime

class Ownership(db.Model):
    __tablename__ = 'ownership'
    
    ownership_id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.parcel_id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), nullable=False)
    share_fraction = db.Column(db.Numeric(5, 4), nullable=False)  # e.g., 0.5 for 50%
    ownership_type = db.Column(db.Enum('Freehold', 'Leasehold', 'Joint', 'Inherited', name='ownership_type_enum'), nullable=False)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ownership {self.owner.name} - {self.share_fraction * 100}% of Parcel {self.parcel_id}>'
