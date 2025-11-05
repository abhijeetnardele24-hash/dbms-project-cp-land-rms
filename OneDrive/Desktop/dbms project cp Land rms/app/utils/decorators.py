"""
Custom decorators for role-based access control.
"""

from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def role_required(*roles):
    """
    Decorator to restrict access to specific user roles.
    
    Usage:
        @role_required('admin', 'registrar')
        def some_view():
            pass
    
    Args:
        *roles: Variable number of role names that are allowed
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """
    Decorator to restrict access to admin users only.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            flash('Admin access required.', 'danger')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def registrar_required(f):
    """
    Decorator to restrict access to registrar users only.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_registrar() and not current_user.is_admin():
            flash('Registrar access required.', 'danger')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def officer_required(f):
    """
    Decorator to restrict access to officer users only.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_officer() and not current_user.is_admin():
            flash('Officer access required.', 'danger')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def citizen_required(f):
    """
    Decorator to restrict access to citizen users only.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_citizen() and not current_user.is_admin():
            flash('Citizen access required.', 'danger')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function
