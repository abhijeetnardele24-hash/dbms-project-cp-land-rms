"""
Main entry point for Land Registry Management System.
Run this file to start the Flask development server.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (override system variables)
load_dotenv(override=True)

from app import create_app
from app.models import db

# Create Flask application
app = create_app(os.getenv('FLASK_ENV') or 'default')


@app.shell_context_processor
def make_shell_context():
    """
    Automatically import models for Flask shell.
    """
    from app.models import (
        User, Property, Owner, Ownership, Mutation, Document,
        Payment, Notification, AuditLog, TaxAssessment,
        LandCategory, UsageType, DocumentType, PropertyStatus
    )
    
    return {
        'db': db,
        'User': User,
        'Property': Property,
        'Owner': Owner,
        'Ownership': Ownership,
        'Mutation': Mutation,
        'Document': Document,
        'Payment': Payment,
        'Notification': Notification,
        'AuditLog': AuditLog,
        'TaxAssessment': TaxAssessment,
        'LandCategory': LandCategory,
        'UsageType': UsageType,
        'DocumentType': DocumentType,
        'PropertyStatus': PropertyStatus
    }


@app.cli.command()
def init_db():
    """Initialize the database with tables."""
    db.create_all()
    print('Database tables created successfully!')


@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    from seed_data import seed_all_data
    seed_all_data()
    print('Database seeded successfully!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
