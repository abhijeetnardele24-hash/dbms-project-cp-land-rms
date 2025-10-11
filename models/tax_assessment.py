from . import db
from datetime import datetime

class TaxAssessment(db.Model):
    __tablename__ = 'tax_assessment'
    
    tax_id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.parcel_id'), nullable=False)
    assessment_year = db.Column(db.Integer, nullable=False)
    land_value = db.Column(db.Numeric(15, 2))
    building_value = db.Column(db.Numeric(15, 2))
    total_assessed_value = db.Column(db.Numeric(15, 2), nullable=False)
    tax_due = db.Column(db.Numeric(12, 2), nullable=False)
    amount_paid = db.Column(db.Numeric(12, 2), default=0)
    paid_on = db.Column(db.Date)
    status = db.Column(db.Enum('Paid', 'Unpaid', 'Partial', name='tax_status_enum'), nullable=False, default='Unpaid')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TaxAssessment {self.tax_id} - Year {self.assessment_year} - {self.status}>'
