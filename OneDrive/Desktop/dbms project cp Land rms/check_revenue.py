from app import create_app
from app.models import Payment

app = create_app()

with app.app_context():
    completed = Payment.query.filter_by(status='completed').all()
    pending = Payment.query.filter_by(status='pending').all()
    failed = Payment.query.filter_by(status='failed').all()
    
    total_revenue = sum(p.amount for p in completed)
    
    print(f"\nPayment Summary:")
    print(f"================")
    print(f"Completed Payments: {len(completed)}")
    print(f"Pending Payments: {len(pending)}")
    print(f"Failed Payments: {len(failed)}")
    print(f"Total Payments: {len(completed) + len(pending) + len(failed)}")
    print(f"\nTotal Revenue (Completed): ₹{total_revenue:,.2f}")
