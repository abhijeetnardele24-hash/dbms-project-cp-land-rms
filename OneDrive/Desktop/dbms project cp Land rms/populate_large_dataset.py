"""
Large-scale database population script for Land Registry Management System
Creates realistic data to demonstrate SQL capabilities and real-world usage:
- 50+ users across all roles
- 100+ properties with diverse characteristics
- 150+ mutation requests with various statuses
- 80+ payments with different statuses
- 200+ notifications
- Complete audit trail and timestamps
"""

from app import create_app
from app.models import (
    db, User, Owner, Property, Ownership, Mutation, 
    Payment, Notification, Document
)
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, date
import random
from decimal import Decimal

# Seed for reproducible data
random.seed(42)

# Sample data pools
FIRST_NAMES = [
    'Rajesh', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 'Suresh', 'Meera',
    'Arjun', 'Kavya', 'Rahul', 'Pooja', 'Karan', 'Divya', 'Rohan', 'Suman',
    'Akash', 'Nisha', 'Aditya', 'Ritu', 'Nikhil', 'Swati', 'Manish', 'Geeta',
    'Sanjay', 'Rekha', 'Vivek', 'Anita', 'Mohit', 'Sunita', 'Ashok', 'Lalita',
    'Deepak', 'Madhuri', 'Prakash', 'Sarita', 'Ravi', 'Usha', 'Yogesh', 'Poonam',
    'Manoj', 'Seema', 'Ramesh', 'Veena', 'Satish', 'Kamala', 'Dinesh', 'Rani',
    'Hemant', 'Shobha', 'Gopal', 'Lata', 'Harish', 'Sudha', 'Naresh', 'Nirmala'
]

LAST_NAMES = [
    'Kumar', 'Sharma', 'Patel', 'Desai', 'Mehta', 'Singh', 'Gupta', 'Reddy',
    'Verma', 'Joshi', 'Shah', 'Rao', 'Nair', 'Iyer', 'Khan', 'Das',
    'Agarwal', 'Pandey', 'Mishra', 'Pillai', 'Sinha', 'Jain', 'Bose', 'Menon',
    'Kulkarni', 'Deshpande', 'Patil', 'Sawant', 'Kadam', 'Jadhav', 'More', 'Pawar'
]

CITIES = [
    'Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Thane', 'Kolhapur',
    'Solapur', 'Ahmednagar', 'Satara', 'Sangli', 'Amravati', 'Nanded', 'Jalgaon'
]

LOCALITIES = [
    'Koregaon Park', 'Bandra West', 'Andheri East', 'Viman Nagar', 'Hinjewadi',
    'Wakad', 'Kharadi', 'Magarpatta', 'Aundh', 'Hadapsar', 'Sitabuldi', 'Dharampeth',
    'Civil Lines', 'Sadar', 'Gangapur Road', 'Panchavati', 'College Road', 'Cidco'
]

PROPERTY_TYPES = ['residential', 'commercial', 'agricultural', 'industrial']
SUB_TYPES = {
    'residential': ['apartment', 'independent_house', 'villa', 'row_house', 'penthouse'],
    'commercial': ['shop', 'office', 'warehouse', 'showroom', 'mall'],
    'agricultural': ['farmland', 'farmhouse', 'plantation', 'orchard'],
    'industrial': ['factory', 'manufacturing_unit', 'industrial_shed', 'warehouse']
}

MUTATION_TYPES = ['sale', 'inheritance', 'gift', 'partition', 'court_order', 'exchange']
MUTATION_STATUSES = ['pending', 'under_review', 'approved', 'rejected', 'on_hold']
PAYMENT_STATUSES = ['pending', 'completed', 'failed', 'refunded']

def random_date(start_days_ago, end_days_ago):
    """Generate random date within range"""
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def random_phone():
    """Generate random Indian phone number"""
    return f"98{random.randint(10000000, 99999999)}"

def random_email(name):
    """Generate email from name"""
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com']
    return f"{name.lower().replace(' ', '.')}.{random.randint(100, 999)}@{random.choice(domains)}"

def populate_large_dataset():
    app = create_app()
    
    with app.app_context():
        print("="*70)
        print("LARGE-SCALE DATABASE POPULATION")
        print("="*70)
        print("\nThis will create:")
        print("- 50+ users (citizens, officers, registrars)")
        print("- 100+ properties with complete details")
        print("- 150+ mutation requests")
        print("- 80+ payment records")
        print("- 200+ notifications")
        print("- Complete audit trail\n")
        
        # Track created entities
        users_list = []
        owners_list = []
        properties_list = []
        mutations_list = []
        
        # STEP 1: Create Admin and Staff Users
        print("\n[1/7] Creating administrative users...")
        
        # Admin
        admin = User(
            email='admin@lrms.gov.in',
            password_hash=generate_password_hash('1234'),
            role='admin',
            full_name='System Administrator',
            phone='9876543200',
            is_active=True,
            email_verified=True,
            created_at=random_date(365, 300)
        )
        db.session.add(admin)
        
        # Registrars (5)
        for i in range(5):
            registrar = User(
                email=f'registrar{i+1}@lrms.gov.in',
                password_hash=generate_password_hash('1234'),
                role='registrar',
                full_name=f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}',
                phone=random_phone(),
                is_active=True,
                email_verified=True,
                created_at=random_date(300, 200)
            )
            db.session.add(registrar)
        
        # Officers (10)
        for i in range(10):
            officer = User(
                email=f'officer{i+1}@lrms.gov.in',
                password_hash=generate_password_hash('1234'),
                role='officer',
                full_name=f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}',
                phone=random_phone(),
                is_active=True,
                email_verified=True,
                created_at=random_date(250, 150)
            )
            db.session.add(officer)
        
        db.session.flush()
        print(f"  [+] Created 1 admin, 5 registrars, 10 officers")
        
        # STEP 2: Create Citizen Users
        print("\n[2/7] Creating citizen users...")
        
        for i in range(60):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            
            user = User(
                email=random_email(full_name),
                password_hash=generate_password_hash('1234'),
                role='citizen',
                full_name=full_name,
                phone=random_phone(),
                address=f"House {random.randint(1, 999)}, {random.choice(LOCALITIES)}, {random.choice(CITIES)}, Maharashtra",
                is_active=True,
                email_verified=random.choice([True, True, True, False]),  # 75% verified
                created_at=random_date(200, 1)
            )
            db.session.add(user)
            users_list.append(user)
        
        db.session.flush()
        print(f"  [+] Created 60 citizen users")
        
        # STEP 3: Create Owners and Properties
        print("\n[3/7] Creating properties with owners...")
        
        property_counter = 0
        for user in users_list[:55]:  # 55 users will have properties
            # Some users have multiple properties
            num_properties = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
            
            # Create owner record
            owner = Owner(
                user_id=user.id,
                full_name=user.full_name,
                phone=user.phone,
                email=user.email,
                address=user.address,
                owner_type=random.choice(['individual', 'joint', 'company']),
                occupation=random.choice(['Business', 'Service', 'Professional', 'Retired', 'Self-employed']),
                created_at=user.created_at
            )
            db.session.add(owner)
            db.session.flush()
            owners_list.append(owner)
            
            for _ in range(num_properties):
                property_counter += 1
                city = random.choice(CITIES)
                locality = random.choice(LOCALITIES)
                prop_type = random.choice(PROPERTY_TYPES)
                sub_type = random.choice(SUB_TYPES[prop_type])
                
                # Generate realistic area based on property type
                if prop_type == 'residential':
                    area = random.uniform(500, 3000)
                elif prop_type == 'commercial':
                    area = random.uniform(300, 5000)
                elif prop_type == 'agricultural':
                    area = random.uniform(5000, 50000)
                else:  # industrial
                    area = random.uniform(2000, 20000)
                
                property_obj = Property(
                    ulpin=f'MH-{city[:3].upper()}-{random.randint(2020, 2024)}-{property_counter:04d}',
                    state='Maharashtra',
                    district=city,
                    village_city=city,
                    locality=locality,
                    street_address=f'{random.randint(1, 500)} {locality}',
                    pincode=f'{random.randint(400000, 449999)}',
                    survey_number=f'SRV-{random.randint(100, 9999)}',
                    plot_number=f'PLT-{random.randint(1, 999)}',
                    area=Decimal(str(round(area, 2))),
                    area_unit='sqft',
                    property_type=prop_type,
                    sub_property_type=sub_type,
                    status=random.choice(['approved', 'approved', 'approved', 'pending', 'under_review']),
                    is_disputed=random.choice([False, False, False, False, True]),
                    is_mortgaged=random.choice([False, False, False, True]),
                    market_value=Decimal(str(random.randint(500000, 50000000))),
                    property_tax_annual=Decimal(str(random.randint(5000, 100000))),
                    registration_date=random_date(200, 1),
                    created_at=random_date(200, 1)
                )
                db.session.add(property_obj)
                db.session.flush()
                properties_list.append(property_obj)
                
                # Create ownership
                ownership = Ownership(
                    property_id=property_obj.id,
                    owner_id=owner.id,
                    ownership_percentage=Decimal('100.00'),
                    ownership_type='sole',
                    acquisition_date=property_obj.registration_date.date() if property_obj.registration_date else date.today(),
                    acquisition_mode=random.choice(['purchase', 'inheritance', 'gift', 'allotment']),
                    is_active=True,
                    created_at=property_obj.created_at
                )
                db.session.add(ownership)
        
        db.session.flush()
        print(f"  [+] Created {len(properties_list)} properties with ownership records")
        
        # STEP 4: Create Mutations
        print("\n[4/7] Creating mutation requests...")
        
        # Get officer IDs for assignment
        officers = User.query.filter_by(role='officer').all()
        
        for i, property_obj in enumerate(properties_list[:120]):  # 120 mutation requests
            owner = Ownership.query.filter_by(property_id=property_obj.id).first()
            if not owner or not owner.owner:
                continue
            
            requester = owner.owner.user
            mutation_type = random.choice(MUTATION_TYPES)
            status = random.choice(MUTATION_STATUSES)
            
            # Create realistic dates based on status
            created_date = random_date(180, 1)
            processing_date = None
            approval_date = None
            rejection_date = None
            
            if status in ['under_review', 'approved', 'rejected']:
                processing_date = created_date + timedelta(days=random.randint(1, 7))
            
            if status == 'approved':
                approval_date = processing_date + timedelta(days=random.randint(1, 10))
            elif status == 'rejected':
                rejection_date = processing_date + timedelta(days=random.randint(1, 5))
            
            mutation = Mutation(
                mutation_number=f'MUT-2024-{2000 + i}',
                property_id=property_obj.id,
                requester_id=requester.id,
                mutation_type=mutation_type,
                description=f'Request for {mutation_type} mutation of property {property_obj.ulpin}',
                reason=f'{mutation_type.capitalize()} transaction - property ownership transfer',
                previous_owners='Previous Owner(s)',
                new_owners=requester.full_name,
                status=status,
                processed_by=random.choice(officers).id if status != 'pending' else None,
                processing_date=processing_date,
                approval_date=approval_date,
                rejection_date=rejection_date,
                rejection_reason='Incomplete documents' if status == 'rejected' else None,
                mutation_fee=Decimal(str(random.uniform(1000, 10000))),
                payment_status=random.choice(['completed', 'pending']) if status in ['approved', 'under_review'] else 'pending',
                priority=random.choice(['low', 'normal', 'normal', 'normal', 'high']),
                escalated=random.choice([False, False, False, True]),
                created_at=created_date
            )
            db.session.add(mutation)
            mutations_list.append(mutation)
        
        db.session.flush()
        print(f"  [+] Created {len(mutations_list)} mutation requests")
        
        # STEP 5: Create Payments
        print("\n[5/7] Creating payment records...")
        
        payment_counter = 0
        for mutation in mutations_list:
            if random.random() < 0.7:  # 70% of mutations have payment records
                payment_counter += 1
                payment_status = 'completed' if mutation.payment_status == 'completed' else random.choice(PAYMENT_STATUSES)
                payment_date = mutation.created_at + timedelta(days=random.randint(0, 5))
                
                payment = Payment(
                    payment_reference=f'PAY-{datetime.now().year}-{10000 + payment_counter}',
                    transaction_id=f'TXN{random.randint(100000000, 999999999)}',
                    user_id=mutation.requester_id,
                    property_id=mutation.property_id,
                    payment_type='mutation_fee',
                    amount=mutation.mutation_fee,
                    payment_method=random.choice(['online', 'card', 'upi', 'netbanking', 'cash']),
                    status=payment_status,
                    payment_date=payment_date,
                    completed_date=payment_date + timedelta(hours=random.randint(1, 24)) if payment_status == 'completed' else None,
                    receipt_number=f'RCP-{random.randint(100000, 999999)}' if payment_status == 'completed' else None,
                    created_at=payment_date
                )
                db.session.add(payment)
        
        # Add property tax payments
        for property_obj in random.sample(properties_list, min(50, len(properties_list))):
            owner = Ownership.query.filter_by(property_id=property_obj.id).first()
            if owner and owner.owner and owner.owner.user:
                payment_counter += 1
                payment_date = random_date(365, 1)
                
                payment = Payment(
                    payment_reference=f'PAY-{datetime.now().year}-{10000 + payment_counter}',
                    transaction_id=f'TXN{random.randint(100000000, 999999999)}',
                    user_id=owner.owner.user.id,
                    property_id=property_obj.id,
                    payment_type='property_tax',
                    amount=property_obj.property_tax_annual,
                    tax_year=datetime.now().year,
                    payment_method=random.choice(['online', 'card', 'upi', 'netbanking']),
                    status='completed',
                    payment_date=payment_date,
                    completed_date=payment_date + timedelta(hours=random.randint(1, 24)),
                    receipt_number=f'RCP-{random.randint(100000, 999999)}',
                    created_at=payment_date
                )
                db.session.add(payment)
        
        db.session.flush()
        print(f"  [+] Created {payment_counter} payment records")
        
        # STEP 6: Create Notifications
        print("\n[6/7] Creating notifications...")
        
        notification_counter = 0
        notification_types = ['mutation', 'payment', 'property', 'document', 'general']
        
        for user in users_list:
            # Each user gets 3-8 notifications
            num_notifications = random.randint(3, 8)
            
            for _ in range(num_notifications):
                notification_counter += 1
                notif_type = random.choice(notification_types)
                created = random_date(60, 0)
                is_read = random.choice([True, True, False])  # 66% read
                
                titles = {
                    'mutation': 'Mutation Request Update',
                    'payment': 'Payment Status Update',
                    'property': 'Property Registration Update',
                    'document': 'Document Verification Required',
                    'general': 'System Notification'
                }
                
                messages = {
                    'mutation': 'Your mutation request has been updated',
                    'payment': 'Payment has been processed successfully',
                    'property': 'Property details have been verified',
                    'document': 'Please upload required documents',
                    'general': 'Welcome to Land Registry Management System'
                }
                
                notification = Notification(
                    user_id=user.id,
                    title=titles[notif_type],
                    message=messages[notif_type],
                    notification_type=notif_type,
                    is_read=is_read,
                    read_at=created + timedelta(hours=random.randint(1, 72)) if is_read else None,
                    email_sent=random.choice([True, False]),
                    priority=random.choice(['low', 'normal', 'normal', 'high']),
                    created_at=created
                )
                db.session.add(notification)
        
        db.session.flush()
        print(f"  [+] Created {notification_counter} notifications")
        
        # STEP 7: Commit all changes
        print("\n[7/7] Committing all changes to database...")
        db.session.commit()
        
        # Print summary
        print("\n" + "="*70)
        print("DATABASE POPULATION COMPLETED SUCCESSFULLY!")
        print("="*70)
        
        total_users = User.query.count()
        total_properties = Property.query.count()
        total_mutations = Mutation.query.count()
        total_payments = Payment.query.count()
        total_notifications = Notification.query.count()
        
        print(f"\nFINAL DATABASE STATISTICS:")
        print(f"  • Total Users: {total_users}")
        print(f"    - Admins: {User.query.filter_by(role='admin').count()}")
        print(f"    - Registrars: {User.query.filter_by(role='registrar').count()}")
        print(f"    - Officers: {User.query.filter_by(role='officer').count()}")
        print(f"    - Citizens: {User.query.filter_by(role='citizen').count()}")
        print(f"  • Total Properties: {total_properties}")
        print(f"  • Total Mutation Requests: {total_mutations}")
        print(f"    - Pending: {Mutation.query.filter_by(status='pending').count()}")
        print(f"    - Under Review: {Mutation.query.filter_by(status='under_review').count()}")
        print(f"    - Approved: {Mutation.query.filter_by(status='approved').count()}")
        print(f"    - Rejected: {Mutation.query.filter_by(status='rejected').count()}")
        print(f"  • Total Payments: {total_payments}")
        print(f"    - Completed: {Payment.query.filter_by(status='completed').count()}")
        print(f"    - Pending: {Payment.query.filter_by(status='pending').count()}")
        print(f"  • Total Notifications: {total_notifications}")
        
        print(f"\nALL USERS PASSWORD: 1234")
        print(f"\nDatabase is now ready for demonstration with realistic data!")
        print("="*70)

if __name__ == '__main__':
    try:
        populate_large_dataset()
    except Exception as e:
        print(f"\n[ERROR] Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
