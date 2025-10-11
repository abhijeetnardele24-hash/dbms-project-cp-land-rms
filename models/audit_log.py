from . import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    
    audit_id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    record_pk_value = db.Column(db.String(100), nullable=False)
    action = db.Column(db.Enum('INSERT', 'UPDATE', 'DELETE', name='audit_action_enum'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    old_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    
    def __repr__(self):
        return f'<AuditLog {self.audit_id} - {self.action} on {self.table_name}>'
