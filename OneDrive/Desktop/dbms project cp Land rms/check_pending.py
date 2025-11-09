from app import create_app
from app.models import db, Property, Mutation

app = create_app()
with app.app_context():
    pending_props = Property.query.filter_by(status='pending').count()
    under_review_props = Property.query.filter_by(status='under_review').count()
    pending_muts = Mutation.query.filter_by(status='pending').count()
    under_review_muts = Mutation.query.filter_by(status='under_review').count()
    
    print(f"Pending Properties: {pending_props}")
    print(f"Under Review Properties: {under_review_props}")
    print(f"Pending Mutations: {pending_muts}")
    print(f"Under Review Mutations: {under_review_muts}")
    print(f"Total Pending Items (shown on dashboard): {pending_props + pending_muts}")
