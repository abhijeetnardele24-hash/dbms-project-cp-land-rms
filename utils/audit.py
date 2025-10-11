"""
Audit logging utilities for Government Property Management Portal
"""

import json
from datetime import datetime
from flask import request
from flask_login import current_user
from models import db
from models.audit_log import AuditLog
from sqlalchemy import event
from sqlalchemy.orm import Session

class AuditLogger:
    """Handles audit logging for database changes"""
    
    @staticmethod
    def log_change(table_name, record_pk, action, old_values=None, new_values=None):
        """
        Log a database change to audit_log table using separate session
        """
        try:
            # Create a new session for audit logging to avoid transaction conflicts
            from sqlalchemy.orm import sessionmaker
            Session = sessionmaker(bind=db.engine)
            audit_session = Session()
            
            audit_entry = AuditLog(
                table_name=table_name,
                record_pk_value=str(record_pk),
                action=action,
                user_id=current_user.user_id if current_user.is_authenticated else None,
                timestamp=datetime.utcnow(),
                old_values=old_values,
                new_values=new_values
            )
            
            audit_session.add(audit_entry)
            audit_session.commit()
            audit_session.close()
            
        except Exception as e:
            print(f"Audit logging error: {str(e)}")
            try:
                audit_session.rollback()
                audit_session.close()
            except:
                pass
    
    @staticmethod
    def get_model_data(instance):
        """Extract model data as dictionary"""
        data = {}
        for column in instance.__table__.columns:
            value = getattr(instance, column.name)
            if isinstance(value, datetime):
                data[column.name] = value.isoformat()
            else:
                data[column.name] = value
        return data

def setup_audit_listeners():
    """Setup SQLAlchemy event listeners for automatic audit logging"""
    
    # List of models to audit
    from models.owner import Owner
    from models.parcel import Parcel
    from models.ownership import Ownership
    from models.mutation import Mutation
    from models.tax_assessment import TaxAssessment
    
    audited_models = [Owner, Parcel, Ownership, Mutation, TaxAssessment]
    
    for model in audited_models:
        # After insert
        @event.listens_for(model, 'after_insert')
        def after_insert(mapper, connection, target):
            if hasattr(target, '__tablename__'):
                new_values = AuditLogger.get_model_data(target)
                AuditLogger.log_change(
                    table_name=target.__tablename__,
                    record_pk=getattr(target, mapper.primary_key[0].name),
                    action='INSERT',
                    new_values=new_values
                )
        
        # After update
        @event.listens_for(model, 'after_update')
        def after_update(mapper, connection, target):
            if hasattr(target, '__tablename__'):
                new_values = AuditLogger.get_model_data(target)
                # Get old values from history
                old_values = {}
                for attr in mapper.attrs:
                    hist = getattr(target, attr.key + '_history', None)
                    if hist and hist.has_changes():
                        old_values[attr.key] = hist.deleted[0] if hist.deleted else None
                
                AuditLogger.log_change(
                    table_name=target.__tablename__,
                    record_pk=getattr(target, mapper.primary_key[0].name),
                    action='UPDATE',
                    old_values=old_values,
                    new_values=new_values
                )
        
        # After delete
        @event.listens_for(model, 'after_delete')
        def after_delete(mapper, connection, target):
            if hasattr(target, '__tablename__'):
                old_values = AuditLogger.get_model_data(target)
                AuditLogger.log_change(
                    table_name=target.__tablename__,
                    record_pk=getattr(target, mapper.primary_key[0].name),
                    action='DELETE',
                    old_values=old_values
                )

# Global audit logger instance
audit_logger = AuditLogger()
