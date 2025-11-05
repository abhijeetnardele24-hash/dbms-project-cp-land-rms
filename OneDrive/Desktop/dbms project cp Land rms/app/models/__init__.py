"""
Database models for Land Registry Management System.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models here for easy access
from app.models.user import User
from app.models.property import Property
from app.models.owner import Owner
from app.models.ownership import Ownership
from app.models.mutation import Mutation, MutationDocument
from app.models.document import Document
from app.models.payment import Payment
from app.models.notification import Notification
from app.models.audit_log import AuditLog
from app.models.tax_assessment import TaxAssessment
from app.models.master_data import LandCategory, UsageType, DocumentType, PropertyStatus

# Import new advanced models
from app.models.property_valuation import PropertyValuation
from app.models.property_inspection import PropertyInspection
from app.models.property_dispute import PropertyDispute
from app.models.property_mortgage import PropertyMortgage
from app.models.message import Message
from app.models.comment import Comment
from app.models.task import Task
from app.models.meeting import Meeting
from app.models.certificate import Certificate
from app.models.complaint import Complaint

__all__ = [
    'db',
    'User',
    'Property',
    'Owner',
    'Ownership',
    'Mutation',
    'MutationDocument',
    'Document',
    'Payment',
    'Notification',
    'AuditLog',
    'TaxAssessment',
    'LandCategory',
    'UsageType',
    'DocumentType',
    'PropertyStatus',
    # New advanced models
    'PropertyValuation',
    'PropertyInspection',
    'PropertyDispute',
    'PropertyMortgage',
    'Message',
    'Comment',
    'Task',
    'Meeting',
    'Certificate',
    'Complaint'
]
