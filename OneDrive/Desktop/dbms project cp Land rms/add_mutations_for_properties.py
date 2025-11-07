"""
Script to add mutation data for all properties in the database.
This will create realistic mutation records (sale, inheritance, gift, etc.)
for all existing properties.
"""

import random
from datetime import datetime, timedelta
from app import create_app
from app.models import db
from app.models.property import Property
from app.models.mutation import Mutation
from app.models.user import User


def generate_indian_names():
    """Generate realistic Indian names for owners."""
    first_names = [
        'Rajesh', 'Priya', 'Amit', 'Sunita', 'Vijay', 'Meera', 'Suresh', 'Anita',
        'Ramesh', 'Kavita', 'Anil', 'Deepa', 'Sanjay', 'Rekha', 'Manoj', 'Pooja',
        'Ashok', 'Neha', 'Ravi', 'Sneha', 'Mukesh', 'Divya', 'Prakash', 'Lakshmi',
        'Dinesh', 'Savita', 'Mahesh', 'Radha', 'Kiran', 'Geeta', 'Pankaj', 'Seema',
        'Vikas', 'Nisha', 'Ajay', 'Asha', 'Arun', 'Usha', 'Naveen', 'Sarita'
    ]
    
    last_names = [
        'Sharma', 'Verma', 'Singh', 'Kumar', 'Patel', 'Gupta', 'Shah', 'Rao',
        'Reddy', 'Joshi', 'Mehta', 'Nair', 'Iyer', 'Das', 'Pandey', 'Mishra',
        'Kapoor', 'Malhotra', 'Chopra', 'Bhatia', 'Khanna', 'Saxena', 'Agarwal'
    ]
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def generate_mutation_data():
    """Generate mutation data for all properties."""
    import os
    os.environ['FLASK_APP'] = 'run.py'
    os.environ['FLASK_ENV'] = 'development'
    
    app = create_app('development')
    
    with app.app_context():
        print("Starting mutation data generation...")
        
        # Get all properties
        properties = Property.query.all()
        print(f"Found {len(properties)} properties")
        
        # Get all citizen users for requester
        citizens = User.query.filter_by(role='citizen').all()
        if not citizens:
            print("Error: No citizen users found. Please create citizen users first.")
            return
        
        # Get officer users for processing
        officers = User.query.filter(User.role.in_(['officer', 'registrar', 'admin'])).all()
        if not officers:
            print("Error: No officer users found.")
            return
        
        mutation_types = ['sale', 'inheritance', 'gift', 'partition', 'transfer']
        statuses = ['approved', 'pending', 'under_review', 'rejected']
        priorities = ['low', 'normal', 'high', 'urgent']
        
        mutations_created = 0
        
        for property in properties:
            # Determine how many mutations for this property (1-4 mutations)
            num_mutations = random.choices([1, 2, 3, 4], weights=[40, 35, 20, 5])[0]
            
            print(f"\nProcessing property ID {property.id} - ULPIN: {property.ulpin or 'Pending'}")
            print(f"  Creating {num_mutations} mutation(s)...")
            
            for i in range(num_mutations):
                mutation_type = random.choice(mutation_types)
                status = random.choices(statuses, weights=[60, 20, 10, 10])[0]
                
                # Generate dates
                days_ago = random.randint(30, 730)  # Between 30 days and 2 years ago
                created_date = datetime.now() - timedelta(days=days_ago)
                
                # Generate previous and new owners
                previous_owner = generate_indian_names()
                new_owner = generate_indian_names()
                
                # Generate transaction amount based on property type
                base_amount = random.randint(500000, 5000000)
                if mutation_type == 'sale':
                    amount = base_amount
                elif mutation_type == 'inheritance':
                    amount = 0  # No transaction amount for inheritance
                elif mutation_type == 'gift':
                    amount = random.randint(0, base_amount // 4)  # Gift tax if any
                else:
                    amount = random.randint(100000, base_amount // 2)
                
                # Create mutation description
                descriptions = {
                    'sale': f'Property sold from {previous_owner} to {new_owner}',
                    'inheritance': f'Property inherited by {new_owner} from {previous_owner}',
                    'gift': f'Property gifted by {previous_owner} to {new_owner}',
                    'partition': f'Property partition between {previous_owner} and {new_owner}',
                    'transfer': f'Property ownership transferred from {previous_owner} to {new_owner}'
                }
                
                mutation = Mutation(
                    property_id=property.id,
                    requester_id=random.choice(citizens).id,
                    mutation_type=mutation_type,
                    description=descriptions[mutation_type],
                    reason=f'{mutation_type.title()} transaction as per legal documentation',
                    previous_owners=previous_owner,
                    new_owners=new_owner,
                    status=status,
                    priority=random.choice(priorities),
                    mutation_fee=random.randint(500, 5000),
                    payment_status='paid' if status == 'approved' else random.choice(['pending', 'paid']),
                    created_at=created_date,
                    updated_at=created_date
                )
                
                # If approved, set processing details
                if status == 'approved':
                    mutation.processed_by = random.choice(officers).id
                    mutation.processing_date = created_date + timedelta(days=random.randint(5, 15))
                    mutation.approval_date = mutation.processing_date + timedelta(days=random.randint(1, 7))
                    mutation.officer_comments = f'{mutation_type.title()} documents verified and approved'
                
                # If rejected, set rejection details
                elif status == 'rejected':
                    mutation.processed_by = random.choice(officers).id
                    mutation.processing_date = created_date + timedelta(days=random.randint(3, 10))
                    mutation.rejection_date = mutation.processing_date + timedelta(days=random.randint(1, 5))
                    mutation.rejection_reason = 'Incomplete documentation or verification failed'
                
                # If under_review or pending, may have processing started
                elif status == 'under_review':
                    mutation.processed_by = random.choice(officers).id
                    mutation.processing_date = created_date + timedelta(days=random.randint(1, 5))
                    mutation.officer_comments = 'Documents under verification'
                
                db.session.add(mutation)
                mutations_created += 1
                
                # Generate mutation number after adding to session
                db.session.flush()
                mutation.generate_mutation_number()
                
                # If approved, generate certificate number
                if status == 'approved':
                    mutation.generate_certificate_number()
                    mutation.certificate_issued_date = mutation.approval_date
                
                print(f"    - Created {mutation_type} mutation (Status: {status}, ID: {mutation.id})")
        
        # Commit all changes
        db.session.commit()
        print(f"\n✓ Successfully created {mutations_created} mutations for {len(properties)} properties!")
        print(f"\nMutation Distribution:")
        
        # Show statistics
        for status in statuses:
            count = Mutation.query.filter_by(status=status).count()
            print(f"  {status.title()}: {count}")
        
        print(f"\nTotal Mutations in Database: {Mutation.query.count()}")


if __name__ == '__main__':
    try:
        generate_mutation_data()
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
