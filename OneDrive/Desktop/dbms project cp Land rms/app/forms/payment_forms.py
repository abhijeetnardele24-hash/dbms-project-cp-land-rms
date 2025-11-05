"""
Payment forms for tax and fee payments.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, IntegerField, TextAreaField, StringField
from wtforms.validators import DataRequired, NumberRange, Optional, Length


class PaymentForm(FlaskForm):
    """Form for making payments."""
    
    property_id = SelectField('Select Property', coerce=int, validators=[DataRequired()])
    
    payment_type = SelectField('Payment Type', choices=[
        ('property_tax', 'Property Tax'),
        ('mutation_fee', 'Mutation Fee'),
        ('registration_fee', 'Registration Fee'),
        ('penalty', 'Penalty'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    
    amount = FloatField('Amount (₹)', validators=[
        DataRequired(),
        NumberRange(min=1, message='Amount must be greater than 0')
    ])
    
    tax_year = IntegerField('Tax Year', validators=[Optional()])
    
    payment_method = SelectField('Payment Method', choices=[
        ('online', 'Online Payment'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('dd', 'Demand Draft'),
        ('card', 'Card')
    ], validators=[DataRequired()])
    
    payment_mode_details = StringField('Payment Details (Cheque/DD No., Card Last 4 digits, etc.)',
                                      validators=[Optional(), Length(max=200)])
    
    description = TextAreaField('Description/Remarks', validators=[Optional(), Length(max=500)])
