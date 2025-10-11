from . import db

class Location(db.Model):
    __tablename__ = 'location'
    
    location_id = db.Column(db.Integer, primary_key=True)
    village = db.Column(db.String(100), nullable=False)
    taluka = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    
    # Relationships
    parcels = db.relationship('Parcel', backref='location', lazy=True)
    
    def __repr__(self):
        return f'<Location {self.village}, {self.taluka}, {self.district}>'
