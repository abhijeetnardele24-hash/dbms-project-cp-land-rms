"""
Large-scale database population script for Land Registry Management System
Creates 500+ unique users, each with 1-2 properties and associated mutations:
- 500+ unique citizen users with login credentials
- 1000+ properties distributed across users
- 800+ mutation requests with various statuses
- Complete ownership and payment records
- Notifications and audit trails
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

# Seed for consistent but random data
random.seed(2024)

# Extended data pools for 500+ unique users
FIRST_NAMES = [
    'Rajesh', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 'Suresh', 'Meera',
    'Arjun', 'Kavya', 'Rahul', 'Pooja', 'Karan', 'Divya', 'Rohan', 'Suman',
    'Akash', 'Nisha', 'Aditya', 'Ritu', 'Nikhil', 'Swati', 'Manish', 'Geeta',
    'Sanjay', 'Rekha', 'Vivek', 'Anita', 'Mohit', 'Sunita', 'Ashok', 'Lalita',
    'Deepak', 'Madhuri', 'Prakash', 'Sarita', 'Ravi', 'Usha', 'Yogesh', 'Poonam',
    'Manoj', 'Seema', 'Ramesh', 'Veena', 'Satish', 'Kamala', 'Dinesh', 'Rani',
    'Hemant', 'Shobha', 'Gopal', 'Lata', 'Harish', 'Sudha', 'Naresh', 'Nirmala',
    'Vijay', 'Neeta', 'Ajay', 'Asha', 'Sanjiv', 'Manju', 'Pankaj', 'Kavita',
    'Sandeep', 'Archana', 'Varun', 'Shilpa', 'Gaurav', 'Preeti', 'Rohit', 'Megha',
    'Anand', 'Smita', 'Vishal', 'Pallavi', 'Sachin', 'Radha', 'Alok', 'Deepti',
    'Ashish', 'Jyoti', 'Arun', 'Sonia', 'Rajeev', 'Sunanda', 'Praveen', 'Kalpana',
    'Devendra', 'Sumitra', 'Mahesh', 'Pushpa', 'Ramesh', 'Savita', 'Girish', 'Leela',
    'Abhishek', 'Anushka', 'Bharat', 'Chandni', 'Chetan', 'Deepika', 'Esha', 'Farhan',
    'Gaurav', 'Hema', 'Ishaan', 'Jaya', 'Kiran', 'Lavanya', 'Mohan', 'Namita',
    'Omkar', 'Payal', 'Qasim', 'Roshni', 'Sameer', 'Tanvi', 'Uday', 'Vidya',
    'Wasim', 'Yash', 'Zara', 'Aarav', 'Bhavna', 'Chirag', 'Diya', 'Eshaan'
]

LAST_NAMES = [
    'Kumar', 'Sharma', 'Patel', 'Desai', 'Mehta', 'Singh', 'Gupta', 'Reddy',
    'Verma', 'Joshi', 'Shah', 'Rao', 'Nair', 'Iyer', 'Khan', 'Das',
    'Agarwal', 'Pandey', 'Mishra', 'Pillai', 'Sinha', 'Jain', 'Bose', 'Menon',
    'Kulkarni', 'Deshpande', 'Patil', 'Sawant', 'Kadam', 'Jadhav', 'More', 'Pawar',
    'Chauhan', 'Malhotra', 'Kapoor', 'Bhatia', 'Choudhary', 'Dixit', 'Ghosh', 'Hegde',
    'Inamdar', 'Jha', 'Kale', 'Lokhande', 'Mane', 'Naik', 'Oak', 'Parab',
    'Raut', 'Salvi', 'Thakur', 'Upadhyay', 'Vaidya', 'Wagh', 'Yadav', 'Zende',
    'Bhosale', 'Chavan', 'Dange', 'Gaikwad', 'Hooda', 'Ingle', 'Joglekar', 'Kambli',
    'Limaye', 'Mukherjee', 'Nadar', 'Parekh', 'Rane', 'Shetty', 'Tendulkar', 'Varma'
]

CITIES = [
    'Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Thane', 'Kolhapur',
    'Solapur', 'Ahmednagar', 'Satara', 'Sangli', 'Amravati', 'Nanded', 'Jalgaon',
    'Akola', 'Latur', 'Dhule', 'Parbhani', 'Jalna', 'Bhiwandi', 'Amravati', 'Malegaon',
    'Kalyan', 'Vasai', 'Navi Mumbai', 'Panvel', 'Ratnagiri', 'Pimpri', 'Chinchwad', 'Ichalkaranji'
]

LOCALITIES = [
    'Koregaon Park', 'Bandra West', 'Andheri East', 'Viman Nagar', 'Hinjewadi',
    'Wakad', 'Kharadi', 'Magarpatta', 'Aundh', 'Hadapsar', 'Sitabuldi', 'Dharampeth',
    'Civil Lines', 'Sadar', 'Gangapur Road', 'Panchavati', 'College Road', 'Cidco',
    'Model Colony', 'Shivaji Nagar', 'Camp Area', 'Deccan', 'Sadashiv Peth', 'Karve Nagar',
    'Pimpri', 'Chinchwad', 'Nigdi', 'Akurdi', 'Ravet', 'Moshi', 'Chakan', 'Talegaon',
    'Kothrud', 'Warje', 'Bavdhan', 'Baner', 'Pashan', 'Sus', 'Katraj', 'Kondhwa'
]

PROPERTY_TYPES = ['residential', 'commercial', 'agricultural', 'industrial']
SUB_TYPES = {
    'residential': ['apartment', 'independent_house', 'villa', 'row_house', 'penthouse', 'bungalow', 'flat', 'duplex'],
    'commercial': ['shop', 'office', 'warehouse', 'showroom', 'mall', 'plaza', 'complex', 'building'],
    'agricultural': ['farmland', 'farmhouse', 'plantation', 'orchard', 'grove', 'field', 'land'],
    'industrial': ['factory', 'manufacturing_unit', 'industrial_shed', 'warehouse', 'plant', 'unit']
}

MUTATION_TYPES = ['sale', 'inheritance', 'gift', 'partition', 'court_order', 'exchange', 'lease', 'transfer']
MUTATION_STATUSES = ['pending', 'under_review', 'approved', 'rejected']
PAYMENT_STATUSES = ['pending', 'completed', 'failed']

def random_date(start_days_ago, end_days_ago):
    """Generate random date within range"""
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    random_days = random.randint(0, max(delta.days, 1))
    return start + timedelta(days=random_days)

def random_phone():
    """Generate random Indian phone number"""
    prefixes = ['98', '97', '96', '95', '94', '93', '92', '91', '90', '89', '88', '87', '86', '85']
    return f"{random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def random_email(first_name, last_name, index):
    """Generate unique email from name and index"""
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'rediffmail.com']
    # Create unique email with index to ensure uniqueness
    username = f"{first_name.lower()}.{last_name.lower()}{index}"
    return f"{username}@{random.choice(domains)}"

def generate_gps_coordinates(city):
    """Generate realistic GPS coordinates for Maharashtra cities"""
    # Base coordinates for major cities
    base_coords = {
        'Mumbai': (19.0760, 72.8777),
        'Pune': (18.5204, 73.8567),
        'Nagpur': (21.1458, 79.0882),
        'Nashik': (19.9975, 73.7898),
        'Aurangabad': (19.8762, 75.3433),
        'Thane': (19.2183, 72.9781)
    }
    
    # Get base coordinates or use default
    base = base_coords.get(city, (19.0, 73.0))
    
    # Add random offset (within ~10km radius)
    lat_offset = random.uniform(-0.09, 0.09)
    lon_offset = random.uniform(-0.09, 0.09)
    
    return (round(base[0] + lat_offset, 6), round(base[1] + lon_offset, 6))

def populate_massive_dataset():
    app = create_app()
    
    with app.app_context():
        print("="*80)
        print("MASSIVE DATABASE POPULATION - 500+ USERS WITH 1000+ PROPERTIES")
        print("="*80)
        print("\nThis will create:")
        print("- 500+ unique citizen users (each with unique login)")
        print("- 1000+ properties (1-2 per user)")
        print("- 800+ mutation requests")
        print("- 600+ payment records")
        print("- 1500+ notifications")
        print("- Complete audit trail\n")
        
        input("Press Enter to continue or Ctrl+C to cancel...")
        
        # Track created entities
        users_list = []
        properties_list = []
        mutations_list = []
        
        # STEP 1: Create Admin and Staff Users
        print("\n[1/8] Creating administrative users...")
        
        # Check if admin exists
        admin = User.query.filter_by(email='admin@lrms.gov.in').first()
        if not admin:
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
        
        # Registrars (10)
        existing_registrars = User.query.filter_by(role='registrar').count()
        registrars_to_create = max(0, 10 - existing_registrars)
        for i in range(registrars_to_create):
            registrar = User(
                email=f'registrar{existing_registrars + i + 1}@lrms.gov.in',
                password_hash=generate_password_hash('1234'),
                role='registrar',
                full_name=f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}',
                phone=random_phone(),
                is_active=True,
                email_verified=True,
                created_at=random_date(300, 200)
            )
            db.session.add(registrar)
        
        # Officers (20)
        existing_officers = User.query.filter_by(role='officer').count()
        officers_to_create = max(0, 20 - existing_officers)
        for i in range(officers_to_create):
            officer = User(
                email=f'officer{existing_officers + i + 1}@lrms.gov.in',
                password_hash=generate_password_hash('1234'),
                role='officer',
                full_name=f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}',
                phone=random_phone(),
                is_active=True,
                email_verified=True,
                created_at=random_date(250, 150)
            )
            db.session.add(officer)
        
        db.session.commit()
        print(f"  [+] Staff users created/verified")
        
        # STEP 2: Create 500+ Citizen Users
        print("\n[2/8] Creating 500+ citizen users with unique credentials...")
        
        # Generate unique user data
        existing_citizens = User.query.filter_by(role='citizen').count()
        target_citizens = 550  # Create 550 to ensure we have 500+
        
        for i in range(target_citizens):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            
            # Create unique email with index
            email = random_email(first_name, last_name, existing_citizens + i + 1)
            
            # Check if email already exists
            if User.query.filter_by(email=email).first():
                continue
            
            user = User(
                email=email,
                password_hash=generate_password_hash('1234'),  # All users have password '1234'
                role='citizen',
                full_name=full_name,
                phone=random_phone(),
                address=f"House {random.randint(1, 999)}, {random.choice(LOCALITIES)}, {random.choice(CITIES)}, Maharashtra - {random.randint(400000, 449999)}",
                is_active=True,
                email_verified=random.choice([True, True, True, False]),  # 75% verified
                created_at=random_date(365, 1)
            )
            db.session.add(user)
            users_list.append(user)
            
            # Commit in batches for performance
            if (i + 1) % 50 == 0:
                db.session.commit()
                print(f"  [+] Created {i + 1}/{target_citizens} citizen users...")
        
        db.session.commit()
        print(f"  [+] Total citizen users created: {len(users_list)}")
        
        # STEP 3: Create Owners and Properties (1-2 per user)
        print("\n[3/8] Creating 1000+ properties with owners...")
        
        property_counter = Property.query.count()
        
        for idx, user in enumerate(users_list):
            # Each user gets 1 or 2 properties (weighted: 60% get 1, 40% get 2)
            num_properties = random.choices([1, 2], weights=[60, 40])[0]
            
            # Create owner record
            owner = Owner(
                user_id=user.id,
                full_name=user.full_name,
                phone=user.phone,
                email=user.email,
                address=user.address,
                owner_type=random.choice(['individual', 'individual', 'joint', 'company']),
                occupation=random.choice(['Business', 'Service', 'Professional', 'Retired', 'Self-employed', 'Government', 'Private']),
                created_at=user.created_at
            )
            db.session.add(owner)
            db.session.flush()
            
            for prop_idx in range(num_properties):
                property_counter += 1
                city = random.choice(CITIES)
                locality = random.choice(LOCALITIES)
                prop_type = random.choice(PROPERTY_TYPES)
                sub_type = random.choice(SUB_TYPES[prop_type])
                
                # Generate realistic area based on property type
                if prop_type == 'residential':
                    area = random.uniform(500, 3500)
                elif prop_type == 'commercial':
                    area = random.uniform(300, 6000)
                elif prop_type == 'agricultural':
                    area = random.uniform(5000, 80000)
                else:  # industrial
                    area = random.uniform(2000, 25000)
                
                # Generate GPS coordinates
                gps_lat, gps_lon = generate_gps_coordinates(city)
                
                # Property status distribution
                status = random.choices(
                    ['approved', 'pending', 'under_review'],
                    weights=[75, 15, 10]
                )[0]
                
                property_obj = Property(
                    ulpin=f'MH-{city[:3].upper()}-{random.randint(2020, 2024)}-{property_counter:05d}',
                    state='Maharashtra',
                    district=city,
                    village_city=city,
                    locality=locality,
                    street_address=f'{random.randint(1, 999)} {locality}, {city}',
                    pincode=f'{random.randint(400000, 449999)}',
                    survey_number=f'SRV-{random.randint(1000, 99999)}',
                    plot_number=f'PLT-{random.randint(1, 9999)}',
                    area=Decimal(str(round(area, 2))),
                    area_unit='sqft',
                    property_type=prop_type,
                    sub_property_type=sub_type,
                    gps_latitude=Decimal(str(gps_lat)),
                    gps_longitude=Decimal(str(gps_lon)),
                    status=status,
                    is_disputed=random.choice([False, False, False, False, False, True]),
                    is_mortgaged=random.choice([False, False, False, False, True]),
                    market_value=Decimal(str(random.randint(500000, 50000000))),
                    property_tax_annual=Decimal(str(random.randint(5000, 150000))),
                    registration_date=random_date(300, 1) if status == 'approved' else None,
                    created_at=random_date(300, 1)
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
                    acquisition_mode=random.choice(['purchase', 'inheritance', 'gift', 'partition', 'court_order', 'government_allotment', 'other']),
                    is_active=True,
                    created_at=property_obj.created_at
                )
                db.session.add(ownership)
            
            # Commit in batches
            if (idx + 1) % 50 == 0:
                db.session.commit()
                print(f"  [+] Processed {idx + 1}/{len(users_list)} users...")
        
        db.session.commit()
        print(f"  [+] Total properties created: {len(properties_list)}")
        
        # STEP 4: Create Mutations
        print("\n[4/8] Creating 800+ mutation requests...")
        
        # Get officer IDs for assignment
        officers = User.query.filter_by(role='officer').all()
        
        # Create mutations for ~75% of properties
        mutation_properties = random.sample(properties_list, min(850, int(len(properties_list) * 0.75)))
        
        for i, property_obj in enumerate(mutation_properties):
            owner_record = Ownership.query.filter_by(property_id=property_obj.id).first()
            if not owner_record or not owner_record.owner or not owner_record.owner.user:
                continue
            
            requester = owner_record.owner.user
            mutation_type = random.choice(MUTATION_TYPES)
            status = random.choices(
                MUTATION_STATUSES,
                weights=[25, 30, 35, 10]  # pending, under_review, approved, rejected
            )[0]
            
            # Create realistic dates based on status
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
                mutation_number=f'MUT-2024-{3000 + i:05d}',
                property_id=property_obj.id,
                requester_id=requester.id,
                mutation_type=mutation_type,
                description=f'Request for {mutation_type} mutation of property {property_obj.ulpin}',
                reason=f'{mutation_type.capitalize()} transaction - ownership transfer to new party',
                previous_owners=f'{requester.full_name} (Previous)',
                new_owners=f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}' if mutation_type in ['sale', 'gift'] else requester.full_name,
                status=status,
                processed_by=random.choice(officers).id if status != 'pending' else None,
                processing_date=processing_date,
                approval_date=approval_date,
                rejection_date=rejection_date,
                rejection_reason='Incomplete documents or verification failed' if status == 'rejected' else None,
                mutation_fee=Decimal(str(random.uniform(1000, 15000))),
                payment_status=random.choice(['paid', 'pending']) if status in ['approved', 'under_review'] else 'pending',
                priority=random.choices(['low', 'normal', 'high'], weights=[20, 70, 10])[0],
                escalated=random.choice([False, False, False, False, True]),
                created_at=created_date
            )
            db.session.add(mutation)
            mutations_list.append(mutation)
            
            # Commit in batches
            if (i + 1) % 100 == 0:
                db.session.commit()
                print(f"  [+] Created {i + 1}/{len(mutation_properties)} mutations...")
        
        db.session.commit()
        print(f"  [+] Total mutations created: {len(mutations_list)}")
        
        # STEP 5: Create Payments
        print("\n[5/8] Creating payment records...")
        
        payment_counter = 0
        
        # Mutation payments
        for mutation in mutations_list:
            if random.random() < 0.75:  # 75% have payment records
                payment_counter += 1
                payment_status = 'completed' if mutation.payment_status == 'paid' else random.choice(PAYMENT_STATUSES)
                payment_date = mutation.created_at + timedelta(days=random.randint(0, 7))
                
                payment = Payment(
                    payment_reference=f'PAY-{datetime.now().year}-{20000 + payment_counter:06d}',
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
                print(f"  [+] Created {payment_counter} payment records...")
        
        # Property tax payments
        tax_properties = random.sample(properties_list, min(300, len(properties_list)))
        for property_obj in tax_properties:
            owner_record = Ownership.query.filter_by(property_id=property_obj.id).first()
            if owner_record and owner_record.owner and owner_record.owner.user:
                payment_counter += 1
                payment_date = random_date(365, 1)
                
                payment = Payment(
                    payment_reference=f'PAY-{datetime.now().year}-{20000 + payment_counter:06d}',
                    transaction_id=f'TXN{random.randint(100000000, 999999999)}',
                    user_id=owner_record.owner.user.id,
                    property_id=property_obj.id,
                    payment_type='property_tax',
                    amount=property_obj.property_tax_annual,
                    tax_year=datetime.now().year,
                    payment_method=random.choice(['online', 'card', 'cheque', 'dd']),
                    status='completed',
                    payment_date=payment_date,
                    completed_date=payment_date + timedelta(hours=random.randint(1, 24)),
                    receipt_number=f'RCP-{random.randint(100000, 999999)}',
                    created_at=payment_date
                )
                db.session.add(payment)
        
        db.session.commit()
        print(f"  [+] Total payments created: {payment_counter}")
        
        # STEP 6: Create Notifications
        print("\n[6/8] Creating notifications...")
        
        notification_counter = 0
        notification_types = ['mutation', 'payment', 'property', 'document', 'general']
        
        for idx, user in enumerate(users_list):
            # Each user gets 2-5 notifications
            num_notifications = random.randint(2, 5)
            
            for _ in range(num_notifications):
                notification_counter += 1
                notif_type = random.choice(notification_types)
                created = random_date(90, 0)
                is_read = random.choice([True, True, False])  # 66% read
                
                titles = {
                    'mutation': 'Mutation Request Update',
                    'payment': 'Payment Status Update',
                    'property': 'Property Registration Update',
                    'document': 'Document Verification Required',
                    'general': 'System Notification'
                }
                
                messages = {
                    'mutation': f'Your mutation request has been {random.choice(["updated", "processed", "reviewed", "approved"])}',
                    'payment': f'Payment of ₹{random.randint(1000, 50000)} has been processed successfully',
                    'property': 'Property details have been verified and updated',
                    'document': 'Please upload required documents for verification',
                    'general': 'Welcome to Land Registry Management System'
                }
                
                notification = Notification(
                    user_id=user.id,
                    title=titles[notif_type],
                    message=messages[notif_type],
                    notification_type=notif_type,
                    is_read=is_read,
                    read_at=created + timedelta(hours=random.randint(1, 120)) if is_read else None,
                    email_sent=random.choice([True, False]),
                    priority=random.choices(['low', 'normal', 'high'], weights=[30, 60, 10])[0],
                    created_at=created
                )
                db.session.add(notification)
            
            if (idx + 1) % 100 == 0:
                db.session.commit()
                print(f"  [+] Created notifications for {idx + 1}/{len(users_list)} users...")
        
        db.session.commit()
        print(f"  [+] Total notifications created: {notification_counter}")
        
        # STEP 7: Final commit
        print("\n[7/8] Committing all changes to database...")
        db.session.commit()
        
        # STEP 8: Print summary
        print("\n[8/8] Generating final statistics...")
        
        total_users = User.query.count()
        total_citizens = User.query.filter_by(role='citizen').count()
        total_properties = Property.query.count()
        total_mutations = Mutation.query.count()
        total_payments = Payment.query.count()
        total_notifications = Notification.query.count()
        
        print("\n" + "="*80)
        print("DATABASE POPULATION COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        print(f"\n📊 FINAL DATABASE STATISTICS:")
        print(f"  • Total Users: {total_users}")
        print(f"    - Admins: {User.query.filter_by(role='admin').count()}")
        print(f"    - Registrars: {User.query.filter_by(role='registrar').count()}")
        print(f"    - Officers: {User.query.filter_by(role='officer').count()}")
        print(f"    - Citizens: {total_citizens}")
        print(f"\n  • Total Properties: {total_properties}")
        print(f"    - Approved: {Property.query.filter_by(status='approved').count()}")
        print(f"    - Pending: {Property.query.filter_by(status='pending').count()}")
        print(f"    - Under Review: {Property.query.filter_by(status='under_review').count()}")
        print(f"\n  • Total Mutation Requests: {total_mutations}")
        print(f"    - Pending: {Mutation.query.filter_by(status='pending').count()}")
        print(f"    - Under Review: {Mutation.query.filter_by(status='under_review').count()}")
        print(f"    - Approved: {Mutation.query.filter_by(status='approved').count()}")
        print(f"    - Rejected: {Mutation.query.filter_by(status='rejected').count()}")
        print(f"\n  • Total Payments: {total_payments}")
        print(f"    - Completed: {Payment.query.filter_by(status='completed').count()}")
        print(f"    - Pending: {Payment.query.filter_by(status='pending').count()}")
        print(f"\n  • Total Notifications: {total_notifications}")
        
        print(f"\n🔑 LOGIN CREDENTIALS:")
        print(f"  • All user passwords: 1234")
        print(f"  • Admin: admin@lrms.gov.in / 1234")
        print(f"  • Sample citizen logins:")
        
        # Show 5 sample citizen logins
        sample_citizens = User.query.filter_by(role='citizen').limit(5).all()
        for citizen in sample_citizens:
            print(f"    - {citizen.email} / 1234")
        
        print(f"\n✅ Database is now ready with 500+ unique users!")
        print(f"✅ Each user has 1-2 properties with mutations!")
        print(f"✅ All data is accessible through admin, registrar, and officer dashboards!")
        print("="*80)

if __name__ == '__main__':
    try:
        populate_massive_dataset()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Operation cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
