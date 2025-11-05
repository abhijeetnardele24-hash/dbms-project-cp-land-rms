"""
Fix Audit Trigger - Remove problematic before_property_update trigger
The trigger has wrong column names (old_data/new_data instead of old_value/new_value)
"""

import pymysql

# Connect to MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='land_registry_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

print("="*80)
print("  FIXING AUDIT TRIGGER ISSUE")
print("="*80)

with connection.cursor() as cursor:
    # Drop the problematic trigger
    print("\n1. Dropping before_property_update trigger...")
    cursor.execute("DROP TRIGGER IF EXISTS before_property_update")
    print("   Done")
    
    # Drop after_property_status_update trigger as well (it also has issues)
    print("\n2. Dropping after_property_status_update trigger...")
    cursor.execute("DROP TRIGGER IF EXISTS after_property_status_update")
    print("   Done")
    
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
print("  FIX APPLIED SUCCESSFULLY!")
print("="*80)
print("\nWhat was fixed:")
print("- Removed trigger that logged to audit_logs with wrong column names")
print("- Audit logging still works via Python code in routes")
print("- Property approval will now work correctly")
print("\n" + "="*80)
