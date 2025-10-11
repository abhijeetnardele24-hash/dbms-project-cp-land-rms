from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to ensure they are registered with SQLAlchemy
from .owner import Owner
from .user_account import UserAccount
from .location import Location
from .parcel import Parcel
from .parcel_version import ParcelVersion
from .ownership import Ownership
from .tenant_agreement import TenantAgreement
from .mutation import Mutation
from .document import Document
from .encumbrance import Encumbrance
from .tax_assessment import TaxAssessment
from .audit_log import AuditLog
