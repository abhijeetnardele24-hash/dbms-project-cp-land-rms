"""
Script to populate the database with test data:
- 5 new citizen users
- 5 properties (one for each user)
- 5 mutation requests (for officer review)
"""

from app import create_app
from app.models import db, User, Owner, Property, Ownership, Mutation
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import random

def populate_test_data():
    app = create_app()
    
    with app.app_context():
        print("Starting database population...")
        
        # Test data for 5 users
        users_data = [
            {
                'email': 'rajesh.kumar@example.com',
                'full_name': 'Rajesh Kumar',
                'phone': '9876543210',
                'address': 'Plot 101, Sector 15, Pune, Maharashtra',
                'property': {
                    'ulpin': 'MH-PUNE-2024-001',
                    'state': 'Maharashtra',
                    'district': 'Pune',
                    'village_city': 'Pune City',
                    'locality': 'Koregaon Park',
                    'street_address': 'Lane 5, Koregaon Park',
                    'pincode': '411001',
                    'survey_number': 'SRV-101',
                    'plot_number': 'PLT-101',
                    'area': 1200.00,
                    'area_unit': 'sqft',
                    'property_type': 'residential',
                    'sub_property_type': 'apartment',
                    'mutation_type': 'sale',
                    'mutation_reason': 'Purchased property from previous owner'
                }
            },
            {
                'email': 'priya.sharma@example.com',
                'full_name': 'Priya Sharma',
                'phone': '9876543211',
                'address': 'House 202, Green Avenue, Mumbai, Maharashtra',
                'property': {
                    'ulpin': 'MH-MUM-2024-002',
                    'state': 'Maharashtra',
                    'district': 'Mumbai',
                    'village_city': 'Mumbai',
                    'locality': 'Bandra West',
                    'street_address': '15th Road, Bandra West',
                    'pincode': '400050',
                    'survey_number': 'SRV-202',
                    'plot_number': 'PLT-202',
                    'area': 850.00,
                    'area_unit': 'sqft',
                    'property_type': 'residential',
                    'sub_property_type': 'independent_house',
                    'mutation_type': 'inheritance',
                    'mutation_reason': 'Inherited property from father'
                }
            },
            {
                'email': 'amit.patel@example.com',
                'full_name': 'Amit Patel',
                'phone': '9876543212',
                'address': 'Shop 303, Market Complex, Nagpur, Maharashtra',
                'property': {
                    'ulpin': 'MH-NAG-2024-003',
                    'state': 'Maharashtra',
                    'district': 'Nagpur',
                    'village_city': 'Nagpur',
                    'locality': 'Sitabuldi',
                    'street_address': 'Central Avenue, Sitabuldi',
                    'pincode': '440012',
                    'survey_number': 'SRV-303',
                    'plot_number': 'PLT-303',
                    'area': 500.00,
                    'area_unit': 'sqft',
                    'property_type': 'commercial',
                    'sub_property_type': 'shop',
                    'mutation_type': 'sale',
                    'mutation_reason': 'Purchased commercial property for business'
                }
            },
            {
                'email': 'sneha.desai@example.com',
                'full_name': 'Sneha Desai',
                'phone': '9876543213',
                'address': 'Villa 404, Palm Grove, Nashik, Maharashtra',
                'property': {
                    'ulpin': 'MH-NASH-2024-004',
                    'state': 'Maharashtra',
                    'district': 'Nashik',
                    'village_city': 'Nashik',
                    'locality': 'Gangapur Road',
                    'street_address': 'Palm Grove Society',
                    'pincode': '422013',
                    'survey_number': 'SRV-404',
                    'plot_number': 'PLT-404',
                    'area': 2500.00,
                    'area_unit': 'sqft',
                    'property_type': 'residential',
                    'sub_property_type': 'villa',
                    'mutation_type': 'gift',
                    'mutation_reason': 'Received as gift from parents'
                }
            },
            {
                'email': 'vikram.mehta@example.com',
                'full_name': 'Vikram Mehta',
                'phone': '9876543214',
                'address': 'Farmhouse 505, Rural Area, Aurangabad, Maharashtra',
                'property': {
                    'ulpin': 'MH-AUR-2024-005',
                    'state': 'Maharashtra',
                    'district': 'Aurangabad',
                    'village_city': 'Aurangabad Rural',
                    'locality': 'Paithan Road',
                    'street_address': 'Village Ganpur',
                    'pincode': '431001',
                    'survey_number': 'SRV-505',
                    'plot_number': 'PLT-505',
                    'area': 5000.00,
                    'area_unit': 'sqft',
                    'property_type': 'agricultural',
                    'sub_property_type': 'farmhouse',
                    'mutation_type': 'partition',
                    'mutation_reason': 'Family property partition'
                }
            }
        ]
        
        # Create users, properties, and mutation requests
        for idx, user_data in enumerate(users_data, 1):
            print(f"\nCreating user {idx}: {user_data['full_name']}")
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                print(f"  - User already exists, skipping...")
                continue
            
            # Create user
            user = User(
                email=user_data['email'],
                password_hash=generate_password_hash('1234'),
                role='citizen',
                full_name=user_data['full_name'],
                phone=user_data['phone'],
                address=user_data['address'],
                is_active=True,
                email_verified=True,
                created_at=datetime.utcnow()
            )
            db.session.add(user)
            db.session.flush()  # Get user.id
            
            print(f"  - Created user with ID: {user.id}")
            
            # Create owner record
            owner = Owner(
                user_id=user.id,
                full_name=user_data['full_name'],
                phone=user_data['phone'],
                email=user_data['email'],
                address=user_data['address'],
                owner_type='individual',
                created_at=datetime.utcnow()
            )
            db.session.add(owner)
            db.session.flush()  # Get owner.id
            
            print(f"  - Created owner with ID: {owner.id}")
            
            # Create property
            prop_data = user_data['property']
            property_obj = Property(
                ulpin=prop_data['ulpin'],
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
                sub_property_type=prop_data['sub_property_type'],
                status='approved',  # Approved so it can have mutations
                registration_date=datetime.utcnow(),
                created_at=datetime.utcnow()
            )
            db.session.add(property_obj)
            db.session.flush()  # Get property_obj.id
            
            print(f"  - Created property with ID: {property_obj.id} (ULPIN: {prop_data['ulpin']})")
            
            # Create ownership
            ownership = Ownership(
                property_id=property_obj.id,
                owner_id=owner.id,
                ownership_percentage=100.00,
                ownership_type='sole',
                acquisition_date=date.today(),
                acquisition_mode='purchase',
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.session.add(ownership)
            
            print(f"  - Created ownership record")
            
            # Create mutation request
            mutation_number = f'MUT-2024-{1000 + idx}'
            mutation = Mutation(
                mutation_number=mutation_number,
                property_id=property_obj.id,
                requester_id=user.id,
                mutation_type=prop_data['mutation_type'],
                description=f"Request for {prop_data['mutation_type']} mutation of property {prop_data['ulpin']}",
                reason=prop_data['mutation_reason'],
                previous_owners='Previous Owner Name',
                new_owners=user_data['full_name'],
                status='pending',
                mutation_fee=random.uniform(1000, 5000),
                payment_status='pending',
                priority='normal'
            )
            db.session.add(mutation)
            
            print(f"  - Created mutation request: {mutation_number}")
        
        # Commit all changes
        db.session.commit()
        print("\n" + "="*50)
        print("Database population completed successfully!")
        print("="*50)
        print("\nTest Users Created (Password: 1234):")
        print("-" * 50)
        for user_data in users_data:
            print(f"Email: {user_data['email']}")
            print(f"Name: {user_data['full_name']}")
            print(f"ULPIN: {user_data['property']['ulpin']}")
            print()

if __name__ == '__main__':
    try:
        populate_test_data()
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
