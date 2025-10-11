from . import db
from datetime import datetime

class Parcel(db.Model):
    __tablename__ = 'parcel'
    
    parcel_id = db.Column(db.Integer, primary_key=True)
    ulpin = db.Column(db.String(50), unique=True, nullable=False)
    survey_no = db.Column(db.String(50), nullable=False)
    total_area = db.Column(db.Numeric(10, 4), nullable=False)
    land_category = db.Column(db.Enum('Agricultural', 'Residential', 'Commercial', 'Industrial', 'State Owned', name='land_category_enum'), nullable=False)
    current_use_type = db.Column(db.String(100))
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    centroid_lat = db.Column(db.Numeric(10, 8))
    centroid_lon = db.Column(db.Numeric(11, 8))
    current_version_id = db.Column(db.Integer, db.ForeignKey('parcel_version.version_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    versions = db.relationship('ParcelVersion', foreign_keys='ParcelVersion.parcel_id', backref='parcel', lazy=True)
    current_version = db.relationship('ParcelVersion', foreign_keys=[current_version_id], post_update=True)
    ownerships = db.relationship('Ownership', backref='parcel', lazy=True)
    tenant_agreements = db.relationship('TenantAgreement', backref='parcel', lazy=True)
    mutations = db.relationship('Mutation', backref='parcel', lazy=True)
    encumbrances = db.relationship('Encumbrance', backref='parcel', lazy=True)
    tax_assessments = db.relationship('TaxAssessment', backref='parcel', lazy=True)
    
    def __repr__(self):
        return f'<Parcel {self.ulpin}>'
