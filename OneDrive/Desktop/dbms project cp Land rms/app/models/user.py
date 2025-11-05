"""
User model for authentication and role-based access control.
Supports four roles: Admin, Registrar, Officer, and Citizen.
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db


class User(UserMixin, db.Model):
    """
    User model with role-based access control.
    
    Roles:
    - admin: Complete system oversight and management
    - registrar: Property registration review and approval
    - officer: Mutation requests and ownership updates
    - citizen: Property owners and applicants
    """
    
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Authentication fields
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Role field - CRITICAL for access control
    role = db.Column(db.Enum('admin', 'registrar', 'officer', 'citizen', name='user_roles'), 
                     nullable=False, default='citizen', index=True)
    
    # Profile fields
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    properties_owned = db.relationship('Owner', back_populates='user', lazy='dynamic')
    mutations_requested = db.relationship('Mutation', back_populates='requester', 
                                         foreign_keys='Mutation.requester_id', lazy='dynamic')
    mutations_processed = db.relationship('Mutation', back_populates='processed_by_user',
                                         foreign_keys='Mutation.processed_by', lazy='dynamic')
    payments = db.relationship('Payment', back_populates='user', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='user', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', back_populates='user', lazy='dynamic')
    
    # New advanced relationships
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id',
                                   back_populates='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id',
                                       back_populates='receiver', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='user', lazy='dynamic')
    complaints = db.relationship('Complaint', foreign_keys='Complaint.user_id',
                                back_populates='user', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == 'admin'
    
    def is_registrar(self):
        """Check if user has registrar role."""
        return self.role == 'registrar'
    
    def is_officer(self):
        """Check if user has officer role."""
        return self.role == 'officer'
    
    def is_citizen(self):
        """Check if user has citizen role."""
        return self.role == 'citizen'
    
    def has_permission(self, permission):
        """
        Check if user has specific permission based on role.
        
        Permission hierarchy:
        - admin: All permissions
        - registrar: Registration approval, property management
        - officer: Mutation approval, ownership updates
        - citizen: View own data, submit requests
        """
        admin_permissions = ['*']  # All permissions
        registrar_permissions = ['view_properties', 'approve_registration', 'manage_properties', 
                                'generate_certificates', 'view_applications']
        officer_permissions = ['view_mutations', 'approve_mutation', 'update_ownership', 
                              'verify_documents', 'generate_mutation_certificate']
        citizen_permissions = ['view_own_properties', 'submit_registration', 'submit_mutation',
                              'make_payment', 'view_own_documents']
        
        if self.role == 'admin':
            return True  # Admin has all permissions
        elif self.role == 'registrar':
            return permission in registrar_permissions
        elif self.role == 'officer':
            return permission in officer_permissions
        elif self.role == 'citizen':
            return permission in citizen_permissions
        
        return False
    
    def get_dashboard_url(self):
        """Return the appropriate dashboard URL based on user role."""
        role_dashboards = {
            'admin': '/admin/dashboard',
            'registrar': '/registrar/dashboard',
            'officer': '/officer/dashboard',
            'citizen': '/citizen/dashboard'
        }
        return role_dashboards.get(self.role, '/citizen/dashboard')
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
    
    def to_dict(self):
        """Convert user object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'phone': self.phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
