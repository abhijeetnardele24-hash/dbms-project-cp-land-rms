from app import create_app
from app.models import db, User, Property, Mutation, Payment

app = create_app()
with app.app_context():
    print("="*60)
    print("DATABASE COUNTS")
    print("="*60)
    print(f"Total Users: {User.query.count()}")
    print(f"  - Citizens: {User.query.filter_by(role='citizen').count()}")
    print(f"  - Registrars: {User.query.filter_by(role='registrar').count()}")
    print(f"  - Officers: {User.query.filter_by(role='officer').count()}")
    print(f"Total Properties: {Property.query.count()}")
    print(f"Total Mutations: {Mutation.query.count()}")
    print(f"  - Pending: {Mutation.query.filter_by(status='pending').count()}")
    print(f"  - Under Review: {Mutation.query.filter_by(status='under_review').count()}")
    print(f"Total Payments: {Payment.query.count()}")
    print("="*60)
