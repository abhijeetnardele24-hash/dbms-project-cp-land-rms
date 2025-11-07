"""Check property ownership data"""
from dotenv import load_dotenv
load_dotenv(override=True)

from app import create_app
from app.models import Property, Owner, Ownership, User

app = create_app()

with app.app_context():
    # Get total properties
    total_props = Property.query.count()
    approved_props = Property.query.filter_by(status='approved').count()
    
    print(f"✅ Total Properties: {total_props}")
    print(f"✅ Approved Properties: {approved_props}")
    
    # Get all users with citizen role
    citizens = User.query.filter_by(role='citizen').all()
    print(f"\n📊 Total Citizens: {len(citizens)}")
    
    # Check ownership records
    total_ownerships = Ownership.query.count()
    active_ownerships = Ownership.query.filter_by(is_active=True).count()
    print(f"\n🏠 Total Ownerships: {total_ownerships}")
    print(f"🏠 Active Ownerships: {active_ownerships}")
    
    # Check a sample citizen
    sample_citizen = citizens[0] if citizens else None
    if sample_citizen:
        print(f"\n👤 Sample Citizen: {sample_citizen.email}")
        owner = Owner.query.filter_by(user_id=sample_citizen.id).first()
        if owner:
            ownerships = owner.ownerships.filter_by(is_active=True).all()
            print(f"   - Has Owner record: Yes")
            print(f"   - Active Ownerships: {len(ownerships)}")
            for ownership in ownerships[:5]:
                prop = ownership.property
                print(f"     • {prop.ulpin} - {prop.village_city} - Status: {prop.status}")
        else:
            print(f"   - Has Owner record: No")
