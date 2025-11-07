"""
Script to add more approved properties with ownership for citizen users
"""

import os
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

load_dotenv(override=True)

from app import create_app
from app.models import db, Property, Owner, Ownership, User

app = create_app()

def add_properties():
    with app.app_context():
        # Get all citizen users
        citizens = User.query.filter_by(role='citizen').all()
        
        if not citizens:
            print("No citizen users found!")
            return
        
        print(f"Found {len(citizens)} citizen users")
        
        # Ensure each citizen has at least 5-10 approved properties
        properties_added = 0
        ownerships_added = 0
        
        districts = ['Mumbai', 'Pune', 'Nashik', 'Nagpur', 'Thane', 'Aurangabad']
        villages = ['Bandra', 'Worli', 'Kasara', 'Deccan', 'Laxmi Nagar', 'Kandivali', 
                   'Andheri', 'Borivali', 'Dadar', 'Parel', 'Khar', 'Santacruz']
        
        for citizen in citizens:
            # Get or create owner record
            owner = Owner.query.filter_by(user_id=citizen.id).first()
            if not owner:
                owner = Owner(
                    user_id=citizen.id,
                    full_name=citizen.full_name,
                    aadhar_number=f"{random.randint(100000000000, 999999999999)}",
                    pan_number=f"ABCDE{random.randint(1000, 9999)}F",
                    email=citizen.email,
                    phone=citizen.phone or f"+91{random.randint(9000000000, 9999999999)}",
                    address=citizen.address or "Sample Address"
                )
                db.session.add(owner)
                db.session.flush()
            
            # Count current active approved properties
            current_approved = sum(1 for o in owner.ownerships.filter_by(is_active=True).all() 
                                  if o.property.status == 'approved')
            
            # Add properties to reach at least 8 approved properties per user
            target_approved = 8
            properties_needed = max(0, target_approved - current_approved)
            
            if properties_needed > 0:
                print(f"\n👤 {citizen.email} - Adding {properties_needed} approved properties")
                
                for i in range(properties_needed):
                    try:
                        # Create property
                        district = random.choice(districts)
                        village = random.choice(villages)
                        
                        property_obj = Property(
                            state='Maharashtra',
                            district=district,
                            village_city=village,
                            area=random.uniform(100, 5000),
                            area_unit='sqft',
                            property_type='residential',
                            status='approved',
                            latitude=random.uniform(18.0, 21.0),
                            longitude=random.uniform(72.0, 75.0),
                            survey_number=f"SRV/{datetime.now().year}/{random.randint(1000, 9999)}",
                            created_at=datetime.now() - timedelta(days=random.randint(30, 365))
                        )
                        
                        db.session.add(property_obj)
                        db.session.flush()
                        
                        # Generate ULPIN
                        state_code = district[:2].upper()
                        dist_code = village[:4].upper().replace(' ', '')
                        year = datetime.now().year
                        property_obj.ulpin = f"{state_code}{dist_code}{year}{property_obj.id:09d}"
                        
                        # Create ownership
                        ownership = Ownership(
                            property_id=property_obj.id,
                            owner_id=owner.id,
                            ownership_percentage=100.0,
                            ownership_type='sole',
                            is_active=True,
                            start_date=property_obj.created_at
                        )
                        
                        db.session.add(ownership)
                        properties_added += 1
                        ownerships_added += 1
                        
                        print(f"  ✅ Added: {property_obj.ulpin} - {village}")
                        
                    except Exception as e:
                        print(f"  ❌ Error: {str(e)}")
                        db.session.rollback()
                
                db.session.commit()
        
        print(f"\n✅ Added {properties_added} properties")
        print(f"✅ Created {ownerships_added} ownerships")
        
        # Summary
        print("\n📊 Final Summary:")
        for citizen in citizens[:5]:  # Show first 5
            owner = Owner.query.filter_by(user_id=citizen.id).first()
            if owner:
                approved_count = sum(1 for o in owner.ownerships.filter_by(is_active=True).all() 
                                    if o.property.status == 'approved')
                print(f"  {citizen.email}: {approved_count} approved properties")

if __name__ == '__main__':
    add_properties()
