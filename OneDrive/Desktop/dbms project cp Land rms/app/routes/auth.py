"""
Authentication routes for login, logout, and registration.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from datetime import datetime
from app.models import db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.forms.auth_forms import LoginForm, RegisterForm

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for all user types."""
    if current_user.is_authenticated:
        return redirect(current_user.get_dashboard_url())
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact administrator.', 'danger')
                return redirect(url_for('auth.login'))
            
            # Login user
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            
            # Log the login action
            AuditLog.log_action(
                user_id=user.id,
                action='user_login',
                action_type='login',
                description=f'{user.full_name} logged in successfully',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                status='success'
            )
            
            db.session.commit()
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            # Redirect to role-specific dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(user.get_dashboard_url())
        
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page for citizens only."""
    if current_user.is_authenticated:
        return redirect(current_user.get_dashboard_url())
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Create new citizen user
        user = User(
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            address=form.address.data,
            role='citizen',  # New registrations are always citizens
            is_active=True
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # Log the registration
        AuditLog.log_action(
            user_id=user.id,
            action='user_registration',
            action_type='create',
            description=f'New citizen registered: {user.full_name}',
            ip_address=request.remote_addr,
            status='success'
        )
        
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
def logout():
    """Logout current user."""
    if current_user.is_authenticated:
        # Log the logout action
        AuditLog.log_action(
            user_id=current_user.id,
            action='user_logout',
            action_type='logout',
            description=f'{current_user.full_name} logged out',
            ip_address=request.remote_addr,
            status='success'
        )
        db.session.commit()
        
        logout_user()
        flash('You have been logged out successfully.', 'info')
    
    return redirect(url_for('auth.login'))
