"""
Seed data script for Land Registry Management System.
Populates database with test users and sample data for demonstration.
"""

from datetime import datetime, timedelta, date
from app import create_app
from app.models import (
    db, User, Property, Owner, Ownership, Mutation,
    Payment, Notification, AuditLog, TaxAssessment,
    LandCategory, UsageType, DocumentType
)

# Create Flask app
app = create_app('development')


def create_users():
    """Create test users for all four roles."""
    print("Creating users...")
    
    users_data = [
        {
            'email': 'admin@lrms.com',
            'password': 'password123',
            'role': 'admin',
            'full_name': 'System Administrator',
            'phone': '9876543210',
            'address': 'Admin Office, Government Building',
            'is_active': True
        },
        {
            'email': 'registrar@lrms.com',
            'password': 'password123',
            'role': 'registrar',
            'full_name': 'John Registrar',
            'phone': '9876543211',
            'address': 'Land Registry Office, District HQ',
            'is_active': True
        },
        {
            'email': 'officer@lrms.com',
            'password': 'password123',
            'role': 'officer',
            'full_name': 'Jane Officer',
            'phone': '9876543212',
            'address': 'Mutation Office, Tahsil Office',
            'is_active': True
        },
        {
            'email': 'user@lrms.com',
            'password': 'password123',
            'role': 'citizen',
            'full_name': 'Raj Kumar',
            'phone': '9876543213',
            'address': '123 Main Street, Mumbai, Maharashtra',
            'is_active': True
        },
        {
            'email': 'user2@lrms.com',
            'password': 'password123',
            'role': 'citizen',
            'full_name': 'Priya Sharma',
            'phone': '9876543214',
            'address': '456 Park Avenue, Pune, Maharashtra',
            'is_active': True
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User.query.filter_by(email=user_data['email']).first()
        if not user:
            user = User(
                email=user_data['email'],
                role=user_data['role'],
                full_name=user_data['full_name'],
                phone=user_data['phone'],
                address=user_data['address'],
                is_active=user_data['is_active']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            users.append(user)
            print(f"  Created {user_data['role']}: {user_data['email']}")
    
    db.session.commit()
    print(f"Created {len(users)} users")
    return User.query.all()


def create_master_data():
    """Create master data for categories and types."""
    print("Creating master data...")
    
    # Land Categories
    categories = [
        {'name': 'Agricultural', 'code': 'AGR', 'tax_rate': 0.005},
        {'name': 'Residential', 'code': 'RES', 'tax_rate': 0.01},
        {'name': 'Commercial', 'code': 'COM', 'tax_rate': 0.02},
        {'name': 'Industrial', 'code': 'IND', 'tax_rate': 0.015},
    ]
    
    for cat_data in categories:
        if not LandCategory.query.filter_by(code=cat_data['code']).first():
            category = LandCategory(**cat_data)
            db.session.add(category)
    
    # Usage Types
    usage_types = [
        {'name': 'Single Family Home', 'code': 'SFH'},
        {'name': 'Apartment Building', 'code': 'APT'},
        {'name': 'Office Space', 'code': 'OFF'},
        {'name': 'Retail Shop', 'code': 'RET'},
        {'name': 'Farm Land', 'code': 'FRM'},
        {'name': 'Warehouse', 'code': 'WAR'},
    ]
    
    for usage_data in usage_types:
        if not UsageType.query.filter_by(code=usage_data['code']).first():
            usage = UsageType(**usage_data)
            db.session.add(usage)
    
    # Document Types
    doc_types = [
        {'name': 'Sale Deed', 'code': 'SALE', 'is_mandatory': True},
        {'name': 'Property Tax Receipt', 'code': 'TAX', 'is_mandatory': False},
        {'name': 'Identity Proof', 'code': 'ID', 'is_mandatory': True},
        {'name': 'Address Proof', 'code': 'ADDR', 'is_mandatory': True},
        {'name': 'Survey Document', 'code': 'SURV', 'is_mandatory': False},
    ]
    
    for doc_data in doc_types:
        if not DocumentType.query.filter_by(code=doc_data['code']).first():
            doc_type = DocumentType(**doc_data)
            db.session.add(doc_type)
    
    db.session.commit()
    print("Master data created")


def create_properties_and_owners():
    """Create sample properties and owners."""
    print("Creating properties and owners...")
    
    users = User.query.filter_by(role='citizen').all()
    registrar = User.query.filter_by(role='registrar').first()
    categories = LandCategory.query.all()
    usage_types = UsageType.query.all()
    
    properties_data = [
        {
            'state': 'Maharashtra',
            'district': 'Mumbai',
            'village_city': 'Andheri',
            'locality': 'Andheri West',
            'street_address': 'Plot 123, Sector 5',
            'pincode': '400053',
            'survey_number': 'SRV/2023/001',
            'plot_number': '123',
            'area': 1200.5,
            'area_unit': 'sqft',
            'property_type': 'residential',
            'market_value': 8500000,
            'registered_value': 8000000,
            'status': 'approved',
            'owner_name': 'Raj Kumar',
            'owner_phone': '9876543213'
        },
        {
            'state': 'Maharashtra',
            'district': 'Pune',
            'village_city': 'Kothrud',
            'locality': 'Kothrud',
            'street_address': 'House 456, Lane 2',
            'pincode': '411038',
            'survey_number': 'SRV/2023/002',
            'plot_number': '456',
            'area': 2400,
            'area_unit': 'sqft',
            'property_type': 'residential',
            'market_value': 12000000,
            'registered_value': 11500000,
            'status': 'approved',
            'owner_name': 'Priya Sharma',
            'owner_phone': '9876543214'
        },
        {
            'state': 'Maharashtra',
            'district': 'Mumbai',
            'village_city': 'Bandra',
            'locality': 'Bandra East',
            'street_address': 'Shop 789, Commercial Complex',
            'pincode': '400051',
            'survey_number': 'SRV/2023/003',
            'plot_number': '789',
            'area': 800,
            'area_unit': 'sqft',
            'property_type': 'commercial',
            'market_value': 15000000,
            'registered_value': 14500000,
            'status': 'pending',
            'owner_name': 'Raj Kumar',
            'owner_phone': '9876543213'
        },
    ]
    
    properties = []
    for i, prop_data in enumerate(properties_data):
        # Create property
        property_obj = Property(
            state=prop_data['state'],
            district=prop_data['district'],
            village_city=prop_data['village_city'],
            locality=prop_data['locality'],
            street_address=prop_data['street_address'],
            pincode=prop_data['pincode'],
            survey_number=prop_data['survey_number'],
            plot_number=prop_data['plot_number'],
            area=prop_data['area'],
            area_unit=prop_data['area_unit'],
            property_type=prop_data['property_type'],
            market_value=prop_data['market_value'],
            registered_value=prop_data['registered_value'],
            status=prop_data['status'],
            land_category_id=categories[i % len(categories)].id if categories else None,
            usage_type_id=usage_types[i % len(usage_types)].id if usage_types else None,
        )
        
        if prop_data['status'] == 'approved':
            property_obj.approved_by = registrar.id if registrar else None
            property_obj.approval_date = datetime.utcnow() - timedelta(days=30)
            property_obj.registration_date = datetime.utcnow() - timedelta(days=30)
        
        db.session.add(property_obj)
        db.session.flush()  # Get property ID
        
        # Generate ULPIN
        property_obj.generate_ulpin()
        
        # Create or get owner
        owner = Owner.query.filter_by(full_name=prop_data['owner_name']).first()
        if not owner:
            user = User.query.filter_by(full_name=prop_data['owner_name']).first()
            owner = Owner(
                user_id=user.id if user else None,
                full_name=prop_data['owner_name'],
                phone=prop_data['owner_phone'],
                email=user.email if user else None,
                owner_type='individual'
            )
            db.session.add(owner)
            db.session.flush()
        
        # Create ownership
        ownership = Ownership(
            property_id=property_obj.id,
            owner_id=owner.id,
            ownership_percentage=100.0,
            ownership_type='sole',
            acquisition_date=date.today() - timedelta(days=365),
            acquisition_mode='purchase',
            is_active=True
        )
        db.session.add(ownership)
        
        # Create tax assessment for approved properties
        if prop_data['status'] == 'approved':
            tax_rate = 0.01
            annual_tax = prop_data['market_value'] * tax_rate
            
            tax_assessment = TaxAssessment(
                property_id=property_obj.id,
                assessment_year=datetime.utcnow().year,
                assessment_date=date.today(),
                assessed_value=prop_data['market_value'],
                tax_rate=tax_rate,
                annual_tax=annual_tax,
                tax_paid=0.0,
                tax_due=annual_tax,
                due_date=date.today() + timedelta(days=90),
                status='pending'
            )
            db.session.add(tax_assessment)
        
        properties.append(property_obj)
    
    db.session.commit()
    print(f"Created {len(properties)} properties with owners and assessments")
    return properties


def create_mutations():
    """Create sample mutation requests."""
    print("Creating mutation requests...")
    
    properties = Property.query.filter_by(status='approved').all()
    citizen = User.query.filter_by(role='citizen').first()
    officer = User.query.filter_by(role='officer').first()
    
    if not properties or not citizen:
        print("Skipping mutations - no approved properties or citizens")
        return []
    
    mutations_data = [
        {
            'property': properties[0],
            'mutation_type': 'sale',
            'description': 'Property sale to new buyer',
            'status': 'pending',
        },
        {
            'property': properties[1] if len(properties) > 1 else properties[0],
            'mutation_type': 'inheritance',
            'description': 'Inheritance transfer to legal heir',
            'status': 'approved',
        },
    ]
    
    mutations = []
    for mut_data in mutations_data:
        mutation = Mutation(
            property_id=mut_data['property'].id,
            requester_id=citizen.id,
            mutation_type=mut_data['mutation_type'],
            description=mut_data['description'],
            status=mut_data['status'],
            mutation_fee=500.0
        )
        db.session.add(mutation)
        db.session.flush()
        
        mutation.generate_mutation_number()
        
        if mut_data['status'] == 'approved':
            mutation.processed_by = officer.id if officer else None
            mutation.approval_date = datetime.utcnow() - timedelta(days=7)
            mutation.generate_certificate_number()
        
        mutations.append(mutation)
    
    db.session.commit()
    print(f"Created {len(mutations)} mutation requests")
    return mutations


def create_payments():
    """Create sample payments."""
    print("Creating payments...")
    
    properties = Property.query.filter_by(status='approved').all()
    citizen = User.query.filter_by(role='citizen').first()
    
    if not properties or not citizen:
        print("Skipping payments - no approved properties or citizens")
        return []
    
    payments = []
    for i, prop in enumerate(properties[:2]):  # Create payments for first 2 properties
        # Generate payment reference manually before creating the payment
        year = datetime.utcnow().year
        payment_ref = f"PAY{year}{i+1:08d}"
        
        payment = Payment(
            user_id=citizen.id,
            property_id=prop.id,
            payment_reference=payment_ref,  # Set reference before adding to session
            payment_type='property_tax',
            amount=prop.market_value * 0.01,
            tax_year=datetime.utcnow().year,
            payment_method='online',
            status='completed' if i == 0 else 'pending',
            payment_date=datetime.utcnow() - timedelta(days=15)
        )
        db.session.add(payment)
        db.session.flush()
        
        if payment.status == 'completed':
            payment.completed_date = payment.payment_date
            payment.generate_receipt_number()
            payment.receipt_issued_date = payment.completed_date
        
        payments.append(payment)
    
    db.session.commit()
    print(f"Created {len(payments)} payments")
    return payments


def create_notifications():
    """Create sample notifications."""
    print("Creating notifications...")
    
    users = User.query.filter_by(role='citizen').all()
    
    if not users:
        print("Skipping notifications - no citizen users")
        return []
    
    notifications = []
    for user in users[:2]:
        notif1 = Notification(
            user_id=user.id,
            title='Welcome to LRMS',
            message='Your account has been successfully created. You can now register properties and submit mutation requests.',
            notification_type='info',
            is_read=False
        )
        db.session.add(notif1)
        
        notif2 = Notification(
            user_id=user.id,
            title='Property Registration Update',
            message='Your property registration is under review by our registrar.',
            notification_type='info',
            is_read=False
        )
        db.session.add(notif2)
        
        notifications.extend([notif1, notif2])
    
    db.session.commit()
    print(f"Created {len(notifications)} notifications")
    return notifications


def create_audit_logs():
    """Create sample audit logs."""
    print("Creating audit logs...")
    
    users = User.query.all()
    
    logs = []
    for user in users:
        log = AuditLog(
            user_id=user.id,
            action='user_login',
            action_type='login',
            description=f'{user.full_name} logged in',
            status='success',
            created_at=datetime.utcnow() - timedelta(days=1)
        )
        db.session.add(log)
        logs.append(log)
    
    db.session.commit()
    print(f"Created {len(logs)} audit logs")
    return logs


def seed_all_data():
    """Main function to seed all data."""
    with app.app_context():
        print("\n" + "="*50)
        print("Starting database seeding...")
        print("="*50 + "\n")
        
        try:
            # Create all data
            create_master_data()
            create_users()
            create_properties_and_owners()
            create_mutations()
            create_payments()
            create_notifications()
            create_audit_logs()
            
            print("\n" + "="*50)
            print("Database seeding completed successfully!")
            print("="*50 + "\n")
            
            print("Test Accounts:")
            print("-" * 50)
            print("Admin:     admin@lrms.com / password123")
            print("Registrar: registrar@lrms.com / password123")
            print("Officer:   officer@lrms.com / password123")
            print("Citizen:   user@lrms.com / password123")
            print("-" * 50)
            
        except Exception as e:
            print(f"\nError during seeding: {str(e)}")
            db.session.rollback()
            raise


if __name__ == '__main__':
    seed_all_data()
