"""
Script to add more mutations to the database to reach 65 total mutations.
"""

import os
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

load_dotenv(override=True)

from app import create_app
from app.models import db, Mutation, Property, User
from sqlalchemy import func

app = create_app()

def add_mutations():
    with app.app_context():
        # Count existing mutations
        existing_count = Mutation.query.count()
        print(f"Current mutation count: {existing_count}")
        
        target_count = 65
        mutations_to_add = target_count - existing_count
        
        if mutations_to_add <= 0:
            print(f"Already have {existing_count} mutations. No need to add more.")
            return
        
        print(f"Adding {mutations_to_add} mutations to reach {target_count} total...")
        
        # Get all properties and users
        properties = Property.query.all()
        users = User.query.filter_by(role='citizen').all()
        
        if not properties:
            print("Error: No properties found in database!")
            return
        
        if not users:
            print("Error: No citizen users found in database!")
            return
        
        mutation_types = ['sale', 'inheritance', 'gift', 'partition', 'exchange', 'court_order']
        statuses = ['pending', 'under_review', 'approved', 'rejected']
        status_weights = [0.4, 0.2, 0.3, 0.1]  # More pending/approved
        
        # Get the last mutation number to continue sequence
        last_mutation = Mutation.query.order_by(Mutation.id.desc()).first()
        if last_mutation and last_mutation.mutation_number:
            # Extract number from format like MUT-2024-1005
            try:
                last_num = int(last_mutation.mutation_number.split('-')[-1])
            except:
                last_num = 1005
        else:
            last_num = 1005
        
        mutations_added = 0
        
        for i in range(mutations_to_add):
            try:
                # Generate mutation number
                mutation_num = last_num + i + 1
                mutation_number = f"MUT-2024-{mutation_num:04d}"
                
                # Random data
                property_obj = random.choice(properties)
                requester = random.choice(users)
                mutation_type = random.choice(mutation_types)
                status = random.choices(statuses, weights=status_weights)[0]
                
                # Random dates (last 6 months)
                days_ago = random.randint(1, 180)
                created_date = datetime.now() - timedelta(days=days_ago)
                
                # Create mutation
                mutation = Mutation(
                    mutation_number=mutation_number,
                    property_id=property_obj.id,
                    requester_id=requester.id,
                    mutation_type=mutation_type,
                    status=status,
                    description=f"Property transfer from Old Owner {mutation_num} to New Owner {mutation_num}",
                    reason=f"Property transfer via {mutation_type}",
                    previous_owners=f"Old Owner {mutation_num}",
                    new_owners=f"New Owner {mutation_num}",
                    mutation_fee=random.uniform(500, 5000),
                    payment_status='paid' if status == 'approved' else 'pending',
                    priority=random.choice(['low', 'normal', 'high']),
                    officer_comments=f"Sample mutation record {mutation_num}" if random.random() > 0.5 else None,
                    created_at=created_date
                )
                
                # Add approval/rejection details for completed mutations
                officers = User.query.filter_by(role='officer').all()
                if status == 'approved' and officers:
                    mutation.approval_date = created_date + timedelta(days=random.randint(5, 30))
                    mutation.processed_by = random.choice(officers).id
                    mutation.processing_date = mutation.approval_date
                    mutation.officer_comments = "Approved after verification"
                    mutation.certificate_issued_date = mutation.approval_date + timedelta(days=2)
                elif status == 'rejected' and officers:
                    mutation.rejection_date = created_date + timedelta(days=random.randint(3, 15))
                    mutation.processed_by = random.choice(officers).id
                    mutation.processing_date = mutation.rejection_date
                    mutation.rejection_reason = "Rejected due to incomplete documents"
                
                db.session.add(mutation)
                mutations_added += 1
                
                # Commit in batches of 10
                if mutations_added % 10 == 0:
                    db.session.commit()
                    print(f"Added {mutations_added}/{mutations_to_add} mutations...")
            
            except Exception as e:
                print(f"Error adding mutation {i+1}: {str(e)}")
                db.session.rollback()
        
        # Final commit
        db.session.commit()
        
        # Verify final count
        final_count = Mutation.query.count()
        print(f"\n✅ Successfully added {mutations_added} mutations!")
        print(f"📊 Total mutations in database: {final_count}")
        
        # Show breakdown by status
        print("\nMutation status breakdown:")
        for status in statuses:
            count = Mutation.query.filter_by(status=status).count()
            print(f"  - {status}: {count}")
        
        print("\n🎉 Database updated successfully!")

if __name__ == '__main__':
    add_mutations()
