"""
Add payment records for existing mutations
"""

from app import create_app
from app.models import db, Mutation, Payment
from datetime import datetime, timedelta
import random
from decimal import Decimal

random.seed(2024)

PAYMENT_STATUSES = ['pending', 'completed', 'failed']

app = create_app()

with app.app_context():
    print("="*60)
    print("ADDING PAYMENTS FOR EXISTING MUTATIONS")
    print("="*60)
    
    # Get all mutations
    all_mutations = Mutation.query.all()
    
    # Get existing payment property IDs
    existing_payment_prop_ids = {p.property_id for p in Payment.query.filter_by(payment_type='mutation_fee').all()}
    
    # Filter mutations that don't have payments yet
    mutations_without_payments = [m for m in all_mutations if m.property_id not in existing_payment_prop_ids]
    
    print(f"Total Mutations: {len(all_mutations)}")
    print(f"Mutations with payments: {len(existing_payment_prop_ids)}")
    print(f"Mutations without payments: {len(mutations_without_payments)}")
    
    if not mutations_without_payments:
        print("\nAll mutations already have payments!")
    else:
        print(f"\nAdding payments for {len(mutations_without_payments)} mutations...")
        
        payment_counter = Payment.query.count()
        payments_created = 0
        
        for mutation in mutations_without_payments:
            try:
                # 80% have payment records
                if random.random() < 0.8:
                    payment_counter += 1
                    payments_created += 1
                    
                    payment_status = 'completed' if mutation.payment_status == 'paid' else random.choice(PAYMENT_STATUSES)
                    payment_date = mutation.created_at + timedelta(days=random.randint(0, 7))
                    
                    payment = Payment(
                        payment_reference=f'PAY-2025-{40000 + payment_counter:06d}',
                        transaction_id=f'TXN{random.randint(100000000, 999999999)}',
                        user_id=mutation.requester_id,
                        property_id=mutation.property_id,
                        payment_type='mutation_fee',
                        amount=mutation.mutation_fee,
                        payment_method=random.choice(['online', 'card', 'cash', 'cheque', 'dd']),
                        status=payment_status,
                        payment_date=payment_date,
                        completed_date=payment_date + timedelta(hours=random.randint(1, 48)) if payment_status == 'completed' else None,
                        receipt_number=f'RCP-{random.randint(100000, 999999)}' if payment_status == 'completed' else None,
                        created_at=payment_date
                    )
                    db.session.add(payment)
                    
                    if payments_created % 100 == 0:
                        db.session.commit()
                        print(f"  [+] Created {payments_created} payments...")
                        
            except Exception as e:
                print(f"Error creating payment for mutation {mutation.id}: {str(e)}")
                db.session.rollback()
                continue
        
        db.session.commit()
        print(f"\n[✓] Total payments created: {payments_created}")
        
        # Final stats
        total_payments = Payment.query.count()
        completed_payments = Payment.query.filter_by(status='completed').count()
        total_revenue = db.session.query(db.func.sum(Payment.amount)).filter(Payment.status == 'completed').scalar() or 0
        
        print(f"\n📊 FINAL STATISTICS:")
        print(f"  • Total Payments: {total_payments}")
        print(f"  • Completed Payments: {completed_payments}")
        print(f"  • Total Revenue: ₹{total_revenue:,.2f}")
        print("="*60)
