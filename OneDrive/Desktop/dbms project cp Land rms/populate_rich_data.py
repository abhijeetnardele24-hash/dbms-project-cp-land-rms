"""
Populate database with rich, realistic data for demo purposes.
Creates 10 users with 30 properties total, including mutations and payments.
"""

import os
import sys
from datetime import datetime, timedelta, date
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db
from app.models.user import User
from app.models.property import Property
from app.models.owner import Owner
from app.models.ownership import Ownership
from app.models.mutation import Mutation
from app.models.payment import Payment
from app.models.notification import Notification
from werkzeug.security import generate_password_hash

# Create Flask app
app = create_app('development')

# Sample data
DISTRICTS = ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Thane', 'Kolhapur']
CITIES = {
    'Mumbai': ['Andheri', 'Borivali', 'Bandra', 'Dadar', 'Kurla'],
    'Pune': ['Kothrud', 'Shivajinagar', 'Hadapsar', 'Wakad', 'Hinjewadi'],
    'Nagpur': ['Dharampeth', 'Sitabuldi', 'Sadar', 'Wardhaman Nagar'],
    'Nashik': ['Nashik Road', 'Satpur', 'College Road', 'Panchavati'],
    'Aurangabad': ['Cidco', 'Town Center', 'Beed Bypass'],
    'Thane': ['Ghodbunder Road', 'Kolshet', 'Majiwada'],
    'Kolhapur': ['Tarabai Park', 'Shahupuri', 'Rajarampuri']
}

PROPERTY_TYPES = ['land', 'residential', 'commercial', 'agricultural', 'industrial']
STATUSES = ['approved', 'pending', 'under_review']
MUTATION_TYPES = ['sale', 'inheritance', 'gift', 'partition']

# User data
USERS_DATA = [
    {'name': 'Rajesh Kumar', 'email': 'rajesh.kumar@example.com', 'phone': '9876543210'},
    {'name': 'Priya Sharma', 'email': 'priya.sharma@example.com', 'phone': '9876543211'},
    {'name': 'Amit Patel', 'email': 'amit.patel@example.com', 'phone': '9876543212'},
    {'name': 'Sneha Desai', 'email': 'sneha.desai@example.com', 'phone': '9876543213'},
    {'name': 'Vikram Singh', 'email': 'vikram.singh@example.com', 'phone': '9876543214'},
    {'name': 'Anita Rao', 'email': 'anita.rao@example.com', 'phone': '9876543215'},
    {'name': 'Suresh Kulkarni', 'email': 'suresh.kulkarni@example.com', 'phone': '9876543216'},
    {'name': 'Meera Joshi', 'email': 'meera.joshi@example.com', 'phone': '9876543217'},
    {'name': 'Anil Mehta', 'email': 'anil.mehta@example.com', 'phone': '9876543218'},
    {'name': 'Kavita Nair', 'email': 'kavita.nair@example.com', 'phone': '9876543219'},
]

def generate_ulpin(district, index):
    """Generate realistic ULPIN"""
    return f"MH{district[:3].upper()}{datetime.now().year}{index:06d}"

def generate_survey_number(district, index):
    """Generate survey number"""
    return f"SRV/{district[:3].upper()}/{datetime.now().year}/{index:04d}"

def random_date_in_past(days_back):
    """Generate random date in the past"""
    return date.today() - timedelta(days=random.randint(1, days_back))

def populate_data():
    """Populate database with comprehensive data"""
    
    with app.app_context():
        print("🚀 Starting data population...")
        
        # Check if users already exist
        print("⚠️  Checking for existing users...")
        existing_count = 0
        for user_data in USERS_DATA:
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                existing_count += 1
        
        if existing_count > 0:
            print(f"⚠️  Found {existing_count} existing users. Skipping deletion to preserve data integrity.")
            print("ℹ️  Script will create only new users that don't exist.")
        
        # Create users (skip existing)
        print("\n👥 Creating users...")
        users = []
        new_users_count = 0
        for user_data in USERS_DATA:
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                users.append(existing_user)
            else:
                user = User(
                    full_name=user_data['name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    password_hash=generate_password_hash('password'),  # All users have password 'password'
                    role='citizen',
                    is_active=True
                )
                db.session.add(user)
                users.append(user)
                new_users_count += 1
        
        db.session.commit()
        print(f"✅ Created {new_users_count} new users, {len(users) - new_users_count} existing users loaded")
        
        # Create owners (skip existing)
        print("\n👤 Creating owner records...")
        owners = []
        new_owners_count = 0
        for user in users:
            existing_owner = Owner.query.filter_by(user_id=user.id).first()
            if existing_owner:
                owners.append(existing_owner)
            else:
                owner = Owner(
                    user_id=user.id,
                    full_name=user.full_name,
                    email=user.email,
                    phone=user.phone,
                    owner_type='individual'
                )
                db.session.add(owner)
                owners.append(owner)
                new_owners_count += 1
        
        db.session.commit()
        print(f"✅ Created {new_owners_count} new owners, {len(owners) - new_owners_count} existing loaded")
        
        # Create 30 properties (skip existing)
        print("\n🏠 Creating 30 properties...")
        properties = []
        property_counter = 1
        new_properties_count = 0
        
        for i, owner in enumerate(owners):
            # Each owner gets 2-4 properties
            num_properties = random.choice([2, 3, 3, 4])
            
            for j in range(num_properties):
                if property_counter > 30:
                    break
                
                district = random.choice(DISTRICTS)
                city = random.choice(CITIES[district])
                prop_type = random.choice(PROPERTY_TYPES)
                status = random.choice(STATUSES)
                ulpin = generate_ulpin(district, property_counter)
                
                # Check if property already exists
                existing_property = Property.query.filter_by(ulpin=ulpin).first()
                if existing_property:
                    properties.append(existing_property)
                    property_counter += 1
                    continue
                
                # Create property
                property_obj = Property(
                    ulpin=ulpin,
                    survey_number=generate_survey_number(district, property_counter),
                    property_type=prop_type,
                    sub_property_type='flat' if prop_type == 'residential' else 'plot',
                    state='Maharashtra',
                    district=district,
                    taluka=city,
                    village_city=city,
                    locality=f'{city} Area {random.randint(1, 5)}',
                    pincode=f'{random.randint(400000, 499999)}',
                    
                    # Area details
                    area=random.uniform(100, 5000),
                    area_unit=random.choice(['sqm', 'sqft', 'acres']),
                    
                    # GPS
                    latitude=random.uniform(18.5, 21.0),
                    longitude=random.uniform(72.8, 79.1),
                    
                    # Valuation
                    market_value=random.uniform(500000, 10000000),
                    registered_value=random.uniform(400000, 9000000),
                    
                    # Status
                    status=status,
                    
                    # Timestamps
                    created_at=datetime.now() - timedelta(days=random.randint(30, 365)),
                    updated_at=datetime.now()
                )
                
                db.session.add(property_obj)
                properties.append(property_obj)
                new_properties_count += 1
                property_counter += 1
        
        db.session.commit()
        print(f"✅ Created {new_properties_count} new properties, {len(properties) - new_properties_count} existing loaded")
        
        # Create ownerships (skip existing)
        print("\n🤝 Creating ownership records...")
        ownerships = []
        new_ownerships_count = 0
        for i, property_obj in enumerate(properties):
            owner = owners[i // 3]  # Distribute properties among owners
            
            # Check if ownership already exists
            existing_ownership = Ownership.query.filter_by(property_id=property_obj.id, owner_id=owner.id, is_active=True).first()
            if existing_ownership:
                ownerships.append(existing_ownership)
                continue
            
            ownership = Ownership(
                property_id=property_obj.id,
                owner_id=owner.id,
                ownership_percentage=100.0,
                ownership_type='sole',
                acquisition_date=property_obj.created_at.date(),
                acquisition_mode='purchase',
                is_active=True
            )
            db.session.add(ownership)
            ownerships.append(ownership)
            new_ownerships_count += 1
        
        db.session.commit()
        print(f"✅ Created {new_ownerships_count} new ownerships, {len(ownerships) - new_ownerships_count} existing loaded")
        
        # Create mutations (for 40% of properties, skip existing)
        print("\n🔄 Creating mutations...")
        mutations = []
        mutation_counter = 1
        new_mutations_count = 0
        
        for property_obj in random.sample(properties, min(int(len(properties) * 0.4), len(properties))):
            ownership = Ownership.query.filter_by(property_id=property_obj.id).first()
            if ownership:
                # Check if mutations already exist for this property
                existing_mutations_count = Mutation.query.filter_by(property_id=property_obj.id).count()
                if existing_mutations_count > 0:
                    continue
                
                mutation_type = random.choice(MUTATION_TYPES)
                mutation_status = random.choice(['approved', 'pending', 'pending', 'rejected'])
                
                mutation = Mutation(
                    property_id=property_obj.id,
                    requester_id=ownership.owner.user_id,
                    mutation_type=mutation_type,
                    mutation_number=f"MUT{datetime.now().year}{mutation_counter:08d}",
                    previous_owners=ownership.owner.full_name,
                    new_owners=random.choice(USERS_DATA)['name'],
                    description=f"{mutation_type.title()} of property",
                    reason=f"Property {mutation_type}",
                    mutation_fee=random.uniform(500, 5000),
                    status=mutation_status,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 180))
                )
                
                if mutation_status == 'approved':
                    mutation.approval_date = mutation.created_at + timedelta(days=random.randint(5, 30))
                    mutation.mutation_certificate_number = f"CERT{datetime.now().year}{mutation_counter:06d}"
                
                db.session.add(mutation)
                mutations.append(mutation)
                mutation_counter += 1
                new_mutations_count += 1
        
        db.session.commit()
        print(f"✅ Created {new_mutations_count} new mutations")
        
        # Create payments (2-5 per property, skip if property already has payments)
        print("\n💰 Creating payments...")
        payments = []
        payment_counter = 1
        new_payments_count = 0
        
        for property_obj in properties:
            ownership = Ownership.query.filter_by(property_id=property_obj.id).first()
            if ownership:
                # Check if payments already exist for this property
                existing_payments_count = Payment.query.filter_by(property_id=property_obj.id).count()
                if existing_payments_count > 0:
                    continue
                
                num_payments = random.randint(2, 5)
                
                for k in range(num_payments):
                    payment_type = random.choice(['property_tax', 'registration_fee', 'mutation_fee', 'stamp_duty'])
                    amount = random.uniform(500, 50000)
                    payment_status = random.choice(['completed', 'completed', 'completed', 'pending'])
                    
                    payment = Payment(
                        user_id=ownership.owner.user_id,
                        property_id=property_obj.id,
                        payment_type=payment_type,
                        amount=amount,
                        payment_reference=f"PAY{datetime.now().year}{payment_counter:08d}",
                        receipt_number=f"REC{datetime.now().year}{datetime.now().month:02d}{payment_counter:06d}",
                        payment_method=random.choice(['online', 'upi', 'card', 'cash']),
                        status=payment_status,
                        payment_date=datetime.now() - timedelta(days=random.randint(1, 365)),
                        tax_year=random.randint(2023, 2025)
                    )
                    
                    if payment_status == 'completed':
                        payment.completed_date = payment.payment_date
                        payment.receipt_issued_date = payment.payment_date
                        payment.transaction_id = f"TXN{random.randint(100000000000, 999999999999)}"
                    
                    db.session.add(payment)
                    payments.append(payment)
                    payment_counter += 1
                    new_payments_count += 1
        
        db.session.commit()
        print(f"✅ Created {new_payments_count} new payments")
        
        # Create notifications (skip users who already have notifications)
        print("\n🔔 Creating notifications...")
        notifications = []
        new_notifications_count = 0
        
        for user in users:
            # Check if user already has notifications
            existing_notifications_count = Notification.query.filter_by(user_id=user.id).count()
            if existing_notifications_count > 0:
                continue
            
            # Create 3-5 notifications per user
            for k in range(random.randint(3, 5)):
                notif_types = [
                    ('Property Approved', 'Your property registration has been approved', 'success'),
                    ('Payment Received', 'Your payment has been received successfully', 'info'),
                    ('Mutation Pending', 'Your mutation request is pending review', 'warning'),
                    ('Document Required', 'Additional documents required for verification', 'warning'),
                    ('Tax Due', 'Property tax payment is due', 'danger'),
                ]
                
                notif_data = random.choice(notif_types)
                
                notification = Notification(
                    user_id=user.id,
                    title=notif_data[0],
                    message=notif_data[1],
                    notification_type=notif_data[2],
                    is_read=random.choice([True, False, False]),
                    created_at=datetime.now() - timedelta(days=random.randint(1, 60))
                )
                
                db.session.add(notification)
                notifications.append(notification)
                new_notifications_count += 1
        
        db.session.commit()
        print(f"✅ Created {new_notifications_count} new notifications")
        
        # Print summary
        print("\n" + "="*60)
        print("✅ DATA POPULATION COMPLETE!")
        print("="*60)
        print(f"👥 Users Created: {len(users)}")
        print(f"🏠 Properties Created: {len(properties)}")
        print(f"🤝 Ownerships Created: {len(ownerships)}")
        print(f"🔄 Mutations Created: {len(mutations)}")
        print(f"💰 Payments Created: {len(payments)}")
        print(f"🔔 Notifications Created: {len(notifications)}")
        print("="*60)
        
        print("\n📊 USER CREDENTIALS:")
        print("-" * 60)
        for user_data in USERS_DATA:
            print(f"📧 {user_data['email']}")
        print("\n🔑 Password for all users: password")
        print("\n💾 MySQL Connection:")
        print("   Host: localhost")
        print("   Username: root")
        print("   Password: 1234")
        print("   Database: land_registry_db")
        print("="*60)
        
        print("\n🎉 You can now:")
        print("   1. Login with any user email and password 'password'")
        print("   2. View properties in MySQL Workbench")
        print("   3. See mutations, payments, and notifications")
        print("   4. Test admin/officer dashboards with rich data")
        print("\n✨ Happy Testing! ✨\n")

if __name__ == '__main__':
    populate_data()
