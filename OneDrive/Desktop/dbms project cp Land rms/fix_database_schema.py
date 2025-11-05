"""
Quick fix script to ensure database schema is correct
"""

import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'land_registry_db',
    'charset': 'utf8mb4'
}

def fix_payments_table():
    """Check and fix payments table schema"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("Checking payments table schema...")
        
        # Get current columns
        cursor.execute("DESCRIBE payments")
        columns = {row[0]: row for row in cursor.fetchall()}
        
        print(f"Found {len(columns)} columns in payments table")
        
        # Check if table_name column exists (it shouldn't)
        if 'table_name' in columns:
            print("⚠️  Found unexpected 'table_name' column - removing it")
            cursor.execute("ALTER TABLE payments DROP COLUMN table_name")
            connection.commit()
            print("✅ Removed table_name column")
        else:
            print("✅ No table_name column found (good)")
        
        # Verify required columns exist
        required_columns = [
            'id', 'payment_reference', 'user_id', 'property_id',
            'payment_type', 'amount', 'status', 'payment_date'
        ]
        
        missing = [col for col in required_columns if col not in columns]
        if missing:
            print(f"⚠️  Missing columns: {missing}")
        else:
            print("✅ All required columns present")
        
        cursor.close()
        connection.close()
        
        print("\n✅ Database schema check complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_payments_table()
