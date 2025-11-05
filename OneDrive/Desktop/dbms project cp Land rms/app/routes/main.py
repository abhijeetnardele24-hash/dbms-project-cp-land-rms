"""
Main routes for home page and common pages.
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Home page - redirect based on authentication status."""
    if current_user.is_authenticated:
        return redirect(current_user.get_dashboard_url())
    return render_template('index.html')


@bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@bp.route('/contact')
def contact():
    """Contact page."""
    return render_template('contact.html')
