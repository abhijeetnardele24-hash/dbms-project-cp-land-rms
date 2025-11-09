"""
Add mutations and payments to existing properties
"""

from app import create_app
from app.models import (
    db, User, Property, Mutation, Payment, Ownership, Notification
)
from datetime import datetime, timedelta
import random
from decimal import Decimal

random.seed(2024)

MUTATION_TYPES = ['sale', 'inheritance', 'gift', 'partition', 'transfer', 'addition', 'removal', 'correction']
MUTATION_STATUSES = ['pending', 'under_review', 'approved', 'rejected']
PAYMENT_STATUSES = ['pending', 'completed', 'failed']
FIRST_NAMES = [
    'Rajesh', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 'Suresh', 'Meera',
    'Arjun', 'Kavya', 'Rahul', 'Pooja', 'Karan', 'Divya', 'Rohan', 'Suman'
]
LAST_NAMES = [
    'Kumar', 'Sharma', 'Patel', 'Desai', 'Mehta', 'Singh', 'Gupta', 'Reddy'
]

def random_date(start_days_ago, end_days_ago):
    """Generate random date within range"""
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    random_days = random.randint(0, max(delta.days, 1))
    return start + timedelta(days=random_days)

def add_mutations_payments():
    app = create_app()
    
    with app.app_context():
        print("="*80)
        print("ADDING MUTATIONS AND PAYMENTS TO EXISTING PROPERTIES")
        print("="*80)
        
        # Get all properties that don't have mutations yet
        all_properties = Property.query.all()
        existing_mutation_prop_ids = {m.property_id for m in Mutation.query.all()}
        properties_without_mutations = [p for p in all_properties if p.id not in existing_mutation_prop_ids]
        
        print(f"\nTotal Properties: {len(all_properties)}")
        print(f"Properties with mutations: {len(existing_mutation_prop_ids)}")
        print(f"Properties without mutations: {len(properties_without_mutations)}")
        
        # Get officers
        officers = User.query.filter_by(role='officer').all()
        if not officers:
            print("ERROR: No officers found!")
            return
        
        print(f"\nAvailable officers: {len(officers)}")
        
        input("\nPress Enter to continue adding mutations...")
        
        # Add mutations for properties without them (target ~75% of remaining)
        target_mutations = int(len(properties_without_mutations) * 0.75)
        properties_to_add_mutations = random.sample(properties_without_mutations, min(target_mutations, len(properties_without_mutations)))
        
        print(f"\n[1/4] Adding mutations for {len(properties_to_add_mutations)} properties...")
        
        mutations_created = 0
        existing_mut_count = Mutation.query.count()
        
        for idx, property_obj in enumerate(properties_to_add_mutations):
            try:
                # Get ownership
                ownership = Ownership.query.filter_by(property_id=property_obj.id, is_active=True).first()
                if not ownership or not ownership.owner or not ownership.owner.user:
                    continue
                
                requester = ownership.owner.user
                mutation_type = random.choice(MUTATION_TYPES)
                status = random.choices(
                    MUTATION_STATUSES,
                    weights=[25, 30, 35, 10]  # pending, under_review, approved, rejected
                )[0]
                
                # Create realistic dates
                created_date = random_date(180, 1)
                processing_date = None
                approval_date = None
                rejection_date = None
                
                if status in ['under_review', 'approved', 'rejected']:
                    processing_date = created_date + timedelta(days=random.randint(1, 10))
                
                if status == 'approved':
                    approval_date = processing_date + timedelta(days=random.randint(1, 15))
                elif status == 'rejected':
                    rejection_date = processing_date + timedelta(days=random.randint(1, 7))
                
                mutation = Mutation(
                    mutation_number=f'MUT-2025-{existing_mut_count + mutations_created + 1:05d}',
                    property_id=property_obj.id,
                    requester_id=requester.id,
                    mutation_type=mutation_type,
                    description=f'Request for {mutation_type} mutation of property {property_obj.ulpin}',
                    reason=f'{mutation_type.capitalize()} transaction - ownership transfer',
                    previous_owners=f'{requester.full_name} (Previous)',
                    new_owners=f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}' if mutation_type in ['sale', 'gift'] else requester.full_name,
                    status=status,
                    processed_by=random.choice(officers).id if status != 'pending' else None,
                    processing_date=processing_date,
                    approval_date=approval_date,
                    rejection_date=rejection_date,
                    rejection_reason='Incomplete documents or verification failed' if status == 'rejected' else None,
                    mutation_fee=Decimal(str(round(random.uniform(1000, 15000), 2))),
                    payment_status=random.choice(['paid', 'pending']) if status in ['approved', 'under_review'] else 'pending',
                    priority=random.choices(['low', 'normal', 'high'], weights=[20, 70, 10])[0],
                    escalated=random.choice([False, False, False, False, True]),
                    created_at=created_date
                )
                db.session.add(mutation)
                mutations_created += 1
                
                # Commit in batches
                if mutations_created % 100 == 0:
                    db.session.commit()
                    print(f"  [+] Created {mutations_created} mutations...")
                    
            except Exception as e:
                print(f"Error creating mutation for property {property_obj.id}: {str(e)}")
                db.session.rollback()
                continue
        
        db.session.commit()
        print(f"  [+] Total mutations created: {mutations_created}")
        
        # Add payments
        print(f"\n[2/4] Adding payment records...")
        
        # Get all mutations
        all_mutations = Mutation.query.all()
        existing_payment_mut_ids = {p.property_id for p in Payment.query.filter_by(payment_type='mutation_fee').all()}
        
        payment_counter = 0
        for mutation in all_mutations:
            try:
                # Skip if payment already exists
                if mutation.property_id in existing_payment_mut_ids:
                    continue
                
                if random.random() < 0.75:  # 75% have payment records
                    payment_counter += 1
                    payment_status = 'completed' if mutation.payment_status == 'paid' else random.choice(PAYMENT_STATUSES)
                    payment_date = mutation.created_at + timedelta(days=random.randint(0, 7))
                    
                    payment = Payment(
                        payment_reference=f'PAY-2025-{30000 + payment_counter:06d}',
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
                
                if payment_counter % 100 == 0 and payment_counter > 0:
                    db.session.commit()
                    print(f"  [+] Created {payment_counter} payments...")
                    
            except Exception as e:
                print(f"Error creating payment for mutation {mutation.id}: {str(e)}")
                db.session.rollback()
                continue
        
        db.session.commit()
        print(f"  [+] Total payments created: {payment_counter}")
        
        # Add notifications
        print(f"\n[3/4] Adding notifications for mutation updates...")
        
        notification_counter = 0
        recent_mutations = Mutation.query.filter(Mutation.status.in_(['under_review', 'approved', 'rejected'])).limit(500).all()
        
        for mutation in recent_mutations:
            try:
                if mutation.status == 'approved':
                    title = 'Mutation Request Approved'
                    message = f'Your mutation request {mutation.mutation_number} has been approved.'
                elif mutation.status == 'rejected':
                    title = 'Mutation Request Rejected'
                    message = f'Your mutation request {mutation.mutation_number} has been rejected.'
                else:
                    title = 'Mutation Under Review'
                    message = f'Your mutation request {mutation.mutation_number} is under review.'
                
                notification = Notification(
                    user_id=mutation.requester_id,
                    title=title,
                    message=message,
                    notification_type='mutation',
                    is_read=random.choice([True, False]),
                    priority='normal',
                    created_at=mutation.processing_date if mutation.processing_date else mutation.created_at
                )
                db.session.add(notification)
                notification_counter += 1
                
            except Exception as e:
                print(f"Error creating notification: {str(e)}")
                continue
        
        db.session.commit()
        print(f"  [+] Total notifications created: {notification_counter}")
        
        # Final stats
        print(f"\n[4/4] Generating final statistics...")
        
        total_users = User.query.count()
        total_citizens = User.query.filter_by(role='citizen').count()
        total_properties = Property.query.count()
        total_mutations = Mutation.query.count()
        total_payments = Payment.query.count()
        
        print("\n" + "="*80)
        print("DATABASE UPDATE COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        print(f"\n📊 FINAL DATABASE STATISTICS:")
        print(f"  • Total Users: {total_users}")
        print(f"    - Citizens: {total_citizens}")
        print(f"  • Total Properties: {total_properties}")
        print(f"  • Total Mutation Requests: {total_mutations}")
        print(f"    - Pending: {Mutation.query.filter_by(status='pending').count()}")
        print(f"    - Under Review: {Mutation.query.filter_by(status='under_review').count()}")
        print(f"    - Approved: {Mutation.query.filter_by(status='approved').count()}")
        print(f"    - Rejected: {Mutation.query.filter_by(status='rejected').count()}")
        print(f"  • Total Payments: {total_payments}")
        print(f"    - Completed: {Payment.query.filter_by(status='completed').count()}")
        print(f"    - Pending: {Payment.query.filter_by(status='pending').count()}")
        
        print(f"\n✅ Database now has {total_citizens}+ users with {total_properties}+ properties!")
        print(f"✅ {total_mutations}+ mutation requests created!")
        print(f"✅ All data is accessible through dashboards!")
        print("="*80)

if __name__ == '__main__':
    try:
        add_mutations_payments()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Operation cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
