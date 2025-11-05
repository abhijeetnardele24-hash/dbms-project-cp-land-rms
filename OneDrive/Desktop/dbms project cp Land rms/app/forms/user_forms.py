"""
User management and profile forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo


class UserManagementForm(FlaskForm):
    """Form for creating/editing users (Admin only)."""
    
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    
    role = SelectField('Role', choices=[
        ('admin', 'Administrator'),
        ('registrar', 'Land Registrar'),
        ('officer', 'Registration Officer'),
        ('citizen', 'Citizen')
    ], validators=[DataRequired()])
    
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=500)])
    
    is_active = BooleanField('Active Account')
    
    password = PasswordField('Password (leave blank to keep existing)', validators=[
        Optional(),
        Length(min=8, message='Password must be at least 8 characters')
    ])


class ProfileForm(FlaskForm):
    """Form for users to edit their own profile."""
    
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=500)])
