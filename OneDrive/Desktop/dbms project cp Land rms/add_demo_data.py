"""
Add Demo Data - Create 4 diverse properties and mutation requests
This will help demonstrate the project with realistic data
"""

import sys
from datetime import datetime, date, timedelta
from app import create_app
from app.models import db
from app.models.property import Property
from app.models.owner import Owner
from app.models.ownership import Ownership
from app.models.mutation import Mutation
from app.models.user import User

def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def add_demo_properties():
    """Add 4 diverse demo properties"""
    
    print_section("ADDING DEMO PROPERTIES FOR PROJECT DEMONSTRATION")
    
    app = create_app('development')
    
    with app.app_context():
        try:
            # Get citizen user
            citizen = User.query.filter_by(role='citizen').first()
            if not citizen:
                print("\nERROR: No citizen user found")
                return False
            
            # Get or create owner
            owner = Owner.query.filter_by(user_id=citizen.id).first()
            if not owner:
                owner = Owner(
                    user_id=citizen.id,
                    full_name=citizen.full_name,
                    phone=citizen.phone,
                    email=citizen.email,
                    owner_type='individual'
                )
                db.session.add(owner)
                db.session.flush()
            
            print(f"\nOwner: {owner.full_name} (ID: {owner.id})")
            
            # Count existing properties
            count_before = Property.query.count()
            print(f"Properties before: {count_before}")
            
            # Property 1: Luxury Apartment in Mumbai
            print("\n1. Adding Luxury Apartment in Mumbai...")
            prop1 = Property(
                state="Maharashtra",
                district="Mumbai",
                taluka="Mumbai City",
                village_city="Worli",
                locality="Worli Sea Face",
                sub_locality="Tower A",
                street_address="456 Skyline Towers, Worli Sea Face",
                landmark="Near Worli Sea Link",
                pincode="400018",
                ward_number="Ward 10",
                zone="Zone C",
                gram_panchayat="Mumbai Municipal Corporation",
                
                latitude=19.0176,
                longitude=72.8203,
                altitude=15.0,
                
                survey_number="S789/12",
                plot_number="P-890",
                block_number="A-10",
                khasra_number="K-456",
                area=2500.0,
                area_unit="sqft",
                length=60.0,
                width=42.0,
                road_frontage=30.0,
                frontage_direction="West",
                plot_shape="rectangular",
                terrain_type="flat",
                built_up_area=2300.0,
                carpet_area=2100.0,
                
                north_boundary="Apartment 1001",
                south_boundary="Apartment 1003",
                east_boundary="Corridor",
                west_boundary="Sea View",
                
                property_type="residential",
                sub_property_type="Luxury Apartment",
                current_land_use="Residential",
                zoning_classification="High-rise Residential",
                property_nature="urban",
                property_age_years=3,
                property_condition="excellent",
                occupancy_status="owner-occupied",
                
                number_of_floors=15,
                floor_number=10,
                number_of_bedrooms=4,
                number_of_bathrooms=4,
                number_of_kitchens=1,
                number_of_balconies=2,
                parking_spaces=3,
                construction_type="RCC",
                flooring_type="Italian Marble",
                year_of_construction=2021,
                
                water_source="municipal",
                water_supply_hours_per_day=24,
                
                electricity_connection_type="residential",
                electricity_load_kw=10.0,
                electricity_meter_number="MUM456789",
                
                road_access="direct",
                road_type="paved",
                road_width_ft=60.0,
                distance_from_main_road_m=20.0,
                
                has_compound_wall=True,
                has_gate=True,
                has_security=True,
                
                market_value=45000000.0,
                registered_value=42000000.0,
                stamp_duty_paid=2100000.0,
                registration_charges_paid=100000.0,
                
                has_encumbrance=False,
                legal_disputes="None",
                
                description="Stunning 4BHK luxury apartment with sea view in Worli. Premium amenities including gym, pool, and concierge service.",
                special_features="Sea view, modular kitchen, smart home automation, club house access",
                
                status='pending',
                created_at=datetime.utcnow() - timedelta(days=2)
            )
            db.session.add(prop1)
            db.session.flush()
            
            ownership1 = Ownership(
                property_id=prop1.id,
                owner_id=owner.id,
                ownership_percentage=100.0,
                ownership_type='sole',
                acquisition_date=date.today() - timedelta(days=100),
                acquisition_mode='purchase',
                is_active=True
            )
            db.session.add(ownership1)
            print(f"   Created Property ID: {prop1.id}")
            
            # Property 2: Agricultural Land in Nashik
            print("\n2. Adding Agricultural Farm in Nashik...")
            prop2 = Property(
                state="Maharashtra",
                district="Nashik",
                taluka="Igatpuri",
                village_city="Kasara",
                locality="Kasara Ghat",
                street_address="Survey No. 25/3, Kasara Village",
                landmark="Near Kasara Railway Station",
                pincode="422403",
                gram_panchayat="Kasara Gram Panchayat",
                
                latitude=19.6531,
                longitude=73.4762,
                altitude=650.0,
                
                survey_number="S25/3",
                plot_number="P-25",
                khasra_number="K-25/3",
                area=5.0,
                area_unit="acre",
                length=200.0,
                width=108.0,
                
                north_boundary="Mango Orchard",
                south_boundary="Village Road",
                east_boundary="Agricultural Land",
                west_boundary="River Stream",
                
                property_type="agricultural",
                sub_property_type="Farm Land",
                current_land_use="Agriculture",
                zoning_classification="Agricultural Zone",
                property_nature="rural",
                property_condition="good",
                
                soil_type="black",
                soil_quality="excellent",
                irrigation_type="Drip irrigation and well",
                current_crop="Grapes",
                tree_count=150,
                
                water_source="well",
                has_borewell=True,
                borewell_depth_ft=250.0,
                has_open_well=True,
                well_depth_ft=40.0,
                
                has_electricity=True,
                electricity_connection_type="agricultural",
                electricity_load_kw=7.5,
                
                road_access="through common path",
                road_type="unpaved",
                road_width_ft=15.0,
                distance_from_main_road_m=500.0,
                
                has_compound_wall=True,
                
                market_value=15000000.0,
                registered_value=14000000.0,
                stamp_duty_paid=700000.0,
                registration_charges_paid=50000.0,
                
                has_encumbrance=False,
                legal_disputes="None",
                
                description="5-acre agricultural farm with grape vineyard. Well-irrigated with drip system and natural water source.",
                special_features="Grape vineyard, mango orchard, natural water stream, farm house",
                
                status='pending',
                created_at=datetime.utcnow() - timedelta(days=5)
            )
            db.session.add(prop2)
            db.session.flush()
            
            ownership2 = Ownership(
                property_id=prop2.id,
                owner_id=owner.id,
                ownership_percentage=100.0,
                ownership_type='sole',
                acquisition_date=date.today() - timedelta(days=200),
                acquisition_mode='inheritance',
                is_active=True
            )
            db.session.add(ownership2)
            print(f"   Created Property ID: {prop2.id}")
            
            # Property 3: Commercial Shop in Pune
            print("\n3. Adding Commercial Shop in Pune...")
            prop3 = Property(
                state="Maharashtra",
                district="Pune",
                taluka="Haveli",
                village_city="Deccan",
                locality="FC Road",
                street_address="Shop No. 12, Shivaji Market, FC Road",
                landmark="Near Goodluck Cafe",
                pincode="411004",
                ward_number="Ward 8",
                zone="Commercial Zone",
                gram_panchayat="Pune Municipal Corporation",
                
                latitude=18.5196,
                longitude=73.8454,
                
                survey_number="S456/78",
                plot_number="Shop-12",
                area=600.0,
                area_unit="sqft",
                length=30.0,
                width=20.0,
                built_up_area=600.0,
                carpet_area=550.0,
                
                north_boundary="Shop 11",
                south_boundary="Shop 13",
                east_boundary="Market Corridor",
                west_boundary="Road",
                
                property_type="commercial",
                sub_property_type="Retail Shop",
                current_land_use="Commercial",
                zoning_classification="Commercial Zone",
                property_nature="urban",
                property_age_years=10,
                property_condition="good",
                occupancy_status="rented",
                
                number_of_floors=1,
                construction_type="RCC",
                flooring_type="Vitrified tiles",
                year_of_construction=2014,
                
                water_source="municipal",
                water_supply_hours_per_day=12,
                
                electricity_connection_type="commercial",
                electricity_load_kw=15.0,
                electricity_meter_number="PUN789456",
                
                road_access="direct",
                road_type="paved",
                road_width_ft=40.0,
                distance_from_main_road_m=0.0,
                
                has_security=True,
                
                market_value=18000000.0,
                registered_value=17000000.0,
                current_rental_value=80000.0,
                stamp_duty_paid=850000.0,
                registration_charges_paid=65000.0,
                
                has_encumbrance=False,
                legal_disputes="None",
                
                description="Prime commercial shop on busy FC Road. High footfall area, perfect for retail business.",
                special_features="Corner location, AC installed, high ceiling, parking nearby",
                
                status='pending',
                created_at=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add(prop3)
            db.session.flush()
            
            ownership3 = Ownership(
                property_id=prop3.id,
                owner_id=owner.id,
                ownership_percentage=100.0,
                ownership_type='sole',
                acquisition_date=date.today() - timedelta(days=150),
                acquisition_mode='purchase',
                is_active=True
            )
            db.session.add(ownership3)
            print(f"   Created Property ID: {prop3.id}")
            
            # Property 4: Residential Plot in Nagpur
            print("\n4. Adding Residential Plot in Nagpur...")
            prop4 = Property(
                state="Maharashtra",
                district="Nagpur",
                taluka="Nagpur",
                village_city="Laxmi Nagar",
                locality="Gandhibagh",
                street_address="Plot No. 45, Sector 7, Laxmi Nagar",
                landmark="Near Laxmi Narayan Temple",
                pincode="440010",
                ward_number="Ward 12",
                zone="Residential Zone",
                gram_panchayat="Nagpur Municipal Corporation",
                
                latitude=21.1458,
                longitude=79.0882,
                
                survey_number="S234/56",
                plot_number="P-45",
                block_number="Sector-7",
                area=1500.0,
                area_unit="sqft",
                length=50.0,
                width=30.0,
                road_frontage=30.0,
                frontage_direction="North",
                plot_shape="rectangular",
                terrain_type="flat",
                
                north_boundary="Road 30ft",
                south_boundary="Plot 46",
                east_boundary="Plot 44",
                west_boundary="Park",
                
                property_type="residential",
                sub_property_type="Residential Plot",
                current_land_use="Vacant land",
                zoning_classification="Residential Zone",
                property_nature="urban",
                property_condition="new",
                
                soil_type="red",
                soil_quality="good",
                
                has_electricity=True,
                electricity_connection_type="residential",
                
                road_access="direct",
                road_type="paved",
                road_width_ft=30.0,
                distance_from_main_road_m=0.0,
                
                has_compound_wall=False,
                
                market_value=6000000.0,
                registered_value=5800000.0,
                stamp_duty_paid=290000.0,
                registration_charges_paid=35000.0,
                
                has_encumbrance=False,
                legal_disputes="None",
                
                description="Well-located residential plot in developed area. Ready for construction with all approvals.",
                special_features="Corner plot, park facing, all utilities available, clear title",
                
                status='pending',
                created_at=datetime.utcnow() - timedelta(hours=12)
            )
            db.session.add(prop4)
            db.session.flush()
            
            ownership4 = Ownership(
                property_id=prop4.id,
                owner_id=owner.id,
                ownership_percentage=100.0,
                ownership_type='sole',
                acquisition_date=date.today() - timedelta(days=50),
                acquisition_mode='purchase',
                is_active=True
            )
            db.session.add(ownership4)
            print(f"   Created Property ID: {prop4.id}")
            
            # Commit all properties
            db.session.commit()
            
            print_section("ADDING MUTATION REQUESTS")
            
            # Get an approved property for mutation
            approved_prop = Property.query.filter_by(status='approved').first()
            
            if approved_prop:
                print(f"\n1. Creating Sale Mutation for Property ID: {approved_prop.id}")
                mutation1 = Mutation(
                    property_id=approved_prop.id,
                    requester_id=citizen.id,
                    mutation_type='sale',
                    description='Sale of property to new buyer',
                    reason='Selling property due to relocation',
                    previous_owners=owner.full_name,
                    new_owners='Amit Sharma',
                    status='pending',
                    mutation_fee=2000.0,
                    created_at=datetime.utcnow() - timedelta(days=3)
                )
                db.session.add(mutation1)
                db.session.flush()
                mutation1.generate_mutation_number()
                print(f"   Created Mutation: {mutation1.mutation_number}")
                
                print(f"\n2. Creating Inheritance Mutation for Property ID: {approved_prop.id}")
                mutation2 = Mutation(
                    property_id=approved_prop.id,
                    requester_id=citizen.id,
                    mutation_type='inheritance',
                    description='Transfer of property through inheritance',
                    reason='Property inherited from father',
                    previous_owners='Late Ramesh Kumar',
                    new_owners=owner.full_name,
                    status='pending',
                    mutation_fee=1500.0,
                    created_at=datetime.utcnow() - timedelta(days=7)
                )
                db.session.add(mutation2)
                db.session.flush()
                mutation2.generate_mutation_number()
                print(f"   Created Mutation: {mutation2.mutation_number}")
            
            db.session.commit()
            
            # Final count
            count_after = Property.query.count()
            mutations_count = Mutation.query.count()
            
            print_section("DEMO DATA ADDED SUCCESSFULLY")
            print(f"\nProperties added: {count_after - count_before}")
            print(f"Total properties now: {count_after}")
            print(f"Total mutations now: {mutations_count}")
            
            print("\n" + "="*80)
            print("SUMMARY OF ADDED PROPERTIES:")
            print("="*80)
            print("\n1. Luxury Apartment - Worli, Mumbai")
            print("   - 4BHK, Sea view, Rs. 4.5 Cr")
            print("   - Status: Pending")
            
            print("\n2. Agricultural Farm - Kasara, Nashik")
            print("   - 5 acres, Grape vineyard, Rs. 1.5 Cr")
            print("   - Status: Pending")
            
            print("\n3. Commercial Shop - FC Road, Pune")
            print("   - 600 sqft retail space, Rs. 1.8 Cr")
            print("   - Status: Pending")
            
            print("\n4. Residential Plot - Laxmi Nagar, Nagpur")
            print("   - 1500 sqft corner plot, Rs. 60 Lac")
            print("   - Status: Pending")
            
            print("\n" + "="*80)
            print("DEMONSTRATION STEPS:")
            print("="*80)
            print("\n1. Login as REGISTRAR to approve pending properties")
            print("2. Properties will get ULPIN numbers automatically")
            print("3. Login as OFFICER to review mutation requests")
            print("4. Login as CITIZEN to make payments")
            print("5. View all data in Admin dashboard")
            print("6. Check database in MySQL Workbench (password: 1234)")
            
            print("\n" + "="*80)
            print("Your project is now ready for impressive demonstration!")
            print("="*80 + "\n")
            
            return True
            
        except Exception as e:
            print(f"\nERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = add_demo_properties()
    sys.exit(0 if success else 1)
