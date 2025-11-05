"""
Fix Trigger Issue - Remove problematic after_property_insert trigger
This trigger was causing OperationalError when submitting property registration
"""

import pymysql
import sys

def fix_trigger():
    """Drop the problematic trigger"""
    
    print("="*80)
    print("  FIXING PROPERTY REGISTRATION TRIGGER ISSUE")
    print("="*80)
    
    try:
        # Connect to MySQL
        print("\n1. Connecting to MySQL database...")
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            database='land_registry_db',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("   ✓ Connected successfully!")
        
        with connection.cursor() as cursor:
            # Drop the problematic trigger
            print("\n2. Dropping after_property_insert trigger...")
            cursor.execute("DROP TRIGGER IF EXISTS after_property_insert")
            print("   ✓ Trigger removed successfully!")
            
            # Show remaining triggers
            print("\n3. Checking remaining triggers on properties table...")
            cursor.execute("SHOW TRIGGERS WHERE `Table` = 'properties'")
            triggers = cursor.fetchall()
            
            if triggers:
                print(f"   Found {len(triggers)} triggers:")
                for trigger in triggers:
                    print(f"   - {trigger['Trigger']}: {trigger['Event']} {trigger['Timing']}")
            else:
                print("   No triggers found on properties table")
        
        connection.commit()
        connection.close()
        
        print("\n" + "="*80)
        print("  ✓ FIX APPLIED SUCCESSFULLY!")
        print("="*80)
        print("\nYou can now:")
        print("1. Restart the Flask application: python run.py")
        print("2. Register new properties without errors")
        print("3. ULPIN will be auto-generated when registrar approves the property")
        print("\n" + "="*80)
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\nPlease ensure:")
        print("1. MySQL server is running")
        print("2. Database 'land_registry_db' exists")
        print("3. Password is '1234'")
        return False

if __name__ == '__main__':
    success = fix_trigger()
    sys.exit(0 if success else 1)
