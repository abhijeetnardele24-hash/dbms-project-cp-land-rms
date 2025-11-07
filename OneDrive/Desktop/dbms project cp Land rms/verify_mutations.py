"""Verify mutations in database"""
from dotenv import load_dotenv
load_dotenv(override=True)

from app import create_app
from app.models import Mutation

app = create_app()

with app.app_context():
    total = Mutation.query.count()
    print(f"✅ Total Mutations: {total}")
    print("\n📊 By Status:")
    print(f"  Pending: {Mutation.query.filter_by(status='pending').count()}")
    print(f"  Under Review: {Mutation.query.filter_by(status='under_review').count()}")
    print(f"  Approved: {Mutation.query.filter_by(status='approved').count()}")
    print(f"  Rejected: {Mutation.query.filter_by(status='rejected').count()}")
    
    print("\n🆕 Recent 5 mutations:")
    for m in Mutation.query.order_by(Mutation.id.desc()).limit(5).all():
        print(f"  {m.mutation_number} - {m.mutation_type} - {m.status}")
