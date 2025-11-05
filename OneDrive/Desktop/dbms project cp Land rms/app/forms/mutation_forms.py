"""
Mutation forms for property ownership changes.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Optional


class MutationRequestForm(FlaskForm):
    """Form for submitting mutation requests."""
    
    property_id = SelectField('Select Property', coerce=int, validators=[DataRequired()])
    
    mutation_type = SelectField('Mutation Type', choices=[
        ('sale', 'Sale/Transfer'),
        ('inheritance', 'Inheritance'),
        ('gift', 'Gift'),
        ('partition', 'Partition'),
        ('transfer', 'General Transfer'),
        ('addition', 'Add Co-owner'),
        ('removal', 'Remove Co-owner'),
        ('correction', 'Correction')
    ], validators=[DataRequired()])
    
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=20, max=1000, message='Description must be between 20 and 1000 characters')
    ])
    
    reason = TextAreaField('Reason for Mutation', validators=[Optional(), Length(max=500)])
    
    previous_owners = TextAreaField('Previous Owners', validators=[Optional(), Length(max=500)])
    new_owners = TextAreaField('New Owners', validators=[Optional(), Length(max=500)])
    
    # Supporting documents (Optional)
    document1 = FileField('Supporting Document 1 (Optional)', validators=[
        Optional(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files allowed')
    ])
    document2 = FileField('Supporting Document 2 (Optional)', validators=[
        Optional(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files allowed')
    ])
    document3 = FileField('Supporting Document 3 (Optional)', validators=[
        Optional(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files allowed')
    ])


class MutationApprovalForm(FlaskForm):
    """Form for approving/rejecting mutation requests."""
    
    action = SelectField('Action', choices=[
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('request_info', 'Request Information')
    ], validators=[DataRequired()])
    
    officer_comments = TextAreaField('Comments/Feedback', validators=[
        DataRequired(),
        Length(min=10, max=1000)
    ])
    
    additional_info_required = TextAreaField('Additional Information Required', validators=[
        Optional(),
        Length(max=500)
    ])
