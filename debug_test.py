#!/usr/bin/env python3
"""
Debug script to test LRMS components individually
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    print("Testing imports...")
    try:
        from flask import Flask
        print("✓ Flask import successful")
        
        from config import Config
        print("✓ Config import successful")
        
        from models import db
        print("✓ Database import successful")
        
        from models.tax_assessment import TaxAssessment
        print("✓ TaxAssessment model import successful")
        
        from models.parcel import Parcel
        print("✓ Parcel model import successful")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    print("\nTesting database connection...")
    try:
        from flask import Flask
        from config import Config
        from models import db
        
        app = Flask(__name__)
        app.config.from_object(Config)
        db.init_app(app)
        
        with app.app_context():
            # Test basic connection
            result = db.engine.execute(db.text("SELECT 1")).scalar()
            print(f"✓ Database connection successful: {result}")
            
            # Test table existence
            result = db.engine.execute(db.text("SHOW TABLES LIKE 'tax_assessment'")).fetchone()
            if result:
                print("✓ tax_assessment table exists")
            else:
                print("✗ tax_assessment table missing")
                
            result = db.engine.execute(db.text("SHOW TABLES LIKE 'parcel'")).fetchone()
            if result:
                print("✓ parcel table exists")
            else:
                print("✗ parcel table missing")
                
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_queries():
    print("\nTesting model queries...")
    try:
        from flask import Flask
        from config import Config
        from models import db
        from models.parcel import Parcel
        from models.tax_assessment import TaxAssessment
        
        app = Flask(__name__)
        app.config.from_object(Config)
        db.init_app(app)
        
        with app.app_context():
            # Test Parcel query
            parcels = Parcel.query.all()
            print(f"✓ Parcel query successful: {len(parcels)} parcels found")
            
            # Test TaxAssessment query
            assessments = TaxAssessment.query.all()
            print(f"✓ TaxAssessment query successful: {len(assessments)} assessments found")
            
            return True
    except Exception as e:
        print(f"✗ Model query failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tax_creation():
    print("\nTesting tax assessment creation...")
    try:
        from flask import Flask
        from config import Config
        from models import db
        from models.parcel import Parcel
        from models.tax_assessment import TaxAssessment
        
        app = Flask(__name__)
        app.config.from_object(Config)
        db.init_app(app)
        
        with app.app_context():
            # Get first parcel
            parcel = Parcel.query.first()
            if not parcel:
                print("✗ No parcels found for testing")
                return False
                
            print(f"✓ Using parcel: {parcel.survey_no}")
            
            # Create test assessment
            test_assessment = TaxAssessment(
                parcel_id=parcel.parcel_id,
                assessment_year=2025,
                land_value=100000.00,
                building_value=50000.00,
                total_assessed_value=150000.00,
                tax_due=1500.00,
                status='Unpaid'
            )
            
            db.session.add(test_assessment)
            db.session.commit()
            
            print(f"✓ Tax assessment created successfully: ID {test_assessment.tax_id}")
            
            # Clean up - delete the test assessment
            db.session.delete(test_assessment)
            db.session.commit()
            print("✓ Test assessment cleaned up")
            
            return True
    except Exception as e:
        print(f"✗ Tax creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("LRMS Debug Test")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_database_connection()
    success &= test_model_queries()
    success &= test_tax_creation()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed! The issue is likely in the web interface.")
    else:
        print("✗ Some tests failed. Check the errors above.")
