"""
Role-based access control decorators for Government Property Management Portal
"""

from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    """
    Decorator to require specific roles for accessing routes
    Usage: @role_required('Admin', 'Registrar')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                flash(f'Access denied. Required role: {", ".join(roles)}', 'error')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to require Admin role"""
    return role_required('Admin')(f)

def registrar_required(f):
    """Decorator to require Registrar or Admin role"""
    return role_required('Registrar', 'Admin')(f)

def approver_required(f):
    """Decorator to require Approver or Admin role"""
    return role_required('Approver', 'Admin')(f)

def any_authenticated_user(f):
    """Decorator to require any authenticated user"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
