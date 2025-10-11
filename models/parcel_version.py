from . import db
from datetime import datetime

class ParcelVersion(db.Model):
    __tablename__ = 'parcel_version'
    
    version_id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.parcel_id'), nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valid_to = db.Column(db.DateTime)
    boundary_geometry = db.Column(db.Text)  # GeoJSON format
    area_at_version = db.Column(db.Numeric(10, 4), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ParcelVersion {self.version_id} for Parcel {self.parcel_id}>'
