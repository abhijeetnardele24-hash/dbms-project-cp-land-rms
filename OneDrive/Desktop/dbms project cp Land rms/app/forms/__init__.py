"""
Forms package initialization.
"""

from app.forms.auth_forms import LoginForm, RegisterForm
from app.forms.property_forms import PropertyRegistrationForm, PropertySearchForm
from app.forms.mutation_forms import MutationRequestForm
from app.forms.payment_forms import PaymentForm
from app.forms.user_forms import UserManagementForm, ProfileForm

__all__ = [
    'LoginForm',
    'RegisterForm',
    'PropertyRegistrationForm',
    'PropertySearchForm',
    'MutationRequestForm',
    'PaymentForm',
    'UserManagementForm',
    'ProfileForm'
]
