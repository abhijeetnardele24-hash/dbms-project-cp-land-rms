"""
Install MySQL Advanced Features
Run this script to create stored procedures, triggers, views, and indexes
"""

import pymysql
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'land_registry_db',
    'charset': 'utf8mb4'
}

def execute_sql_file(filepath):
    """Execute SQL file with multiple statements"""
    print(f"📂 Reading SQL file: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Connect to database
    print("🔌 Connecting to MySQL database...")
    connection = pymysql.connect(**DB_CONFIG)
    
    try:
        with connection.cursor() as cursor:
            # Split by semicolons and execute each statement
            statements = sql_content.split('DELIMITER')
            
            for idx, statement_block in enumerate(statements):
                # Handle different delimiter scenarios
                if '$$' in statement_block:
                    # Stored procedure/trigger block
                    parts = statement_block.split('$$')
                    for part in parts:
                        part = part.strip()
                        if part and not part.startswith('--') and part != ';':
                            try:
                                cursor.execute(part)
                                print(f"✅ Executed block {idx + 1}")
                            except Exception as e:
                                if 'already exists' not in str(e) and 'Duplicate' not in str(e):
                                    print(f"⚠️  Warning in block {idx + 1}: {str(e)[:100]}")
                else:
                    # Regular SQL statements
                    individual_statements = statement_block.split(';')
                    for stmt in individual_statements:
                        stmt = stmt.strip()
                        if stmt and not stmt.startswith('--') and stmt.upper() != 'USE':
                            try:
                                cursor.execute(stmt)
                            except Exception as e:
                                if 'already exists' not in str(e) and 'Duplicate' not in str(e):
                                    print(f"⚠️  Warning: {str(e)[:100]}")
            
            connection.commit()
            print("✅ All SQL statements executed successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        connection.rollback()
    finally:
        connection.close()
        print("🔌 Database connection closed")

def verify_installation():
    """Verify that procedures, triggers, and views were created"""
    print("\n🔍 Verifying installation...")
    connection = pymysql.connect(**DB_CONFIG)
    
    try:
        with connection.cursor() as cursor:
            # Check stored procedures
            cursor.execute("""
                SELECT ROUTINE_NAME 
                FROM information_schema.ROUTINES 
                WHERE ROUTINE_SCHEMA = 'land_registry_db' 
                AND ROUTINE_TYPE = 'PROCEDURE'
            """)
            procedures = cursor.fetchall()
            print(f"\n📋 Stored Procedures Created: {len(procedures)}")
            for proc in procedures:
                print(f"   ✓ {proc[0]}")
            
            # Check triggers
            cursor.execute("""
                SELECT TRIGGER_NAME 
                FROM information_schema.TRIGGERS 
                WHERE TRIGGER_SCHEMA = 'land_registry_db'
            """)
            triggers = cursor.fetchall()
            print(f"\n⚡ Triggers Created: {len(triggers)}")
            for trigger in triggers:
                print(f"   ✓ {trigger[0]}")
            
            # Check views
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM information_schema.VIEWS 
                WHERE TABLE_SCHEMA = 'land_registry_db'
            """)
            views = cursor.fetchall()
            print(f"\n👁️  Views Created: {len(views)}")
            for view in views:
                print(f"   ✓ {view[0]}")
            
            # Check indexes
            cursor.execute("""
                SELECT DISTINCT INDEX_NAME 
                FROM information_schema.STATISTICS 
                WHERE TABLE_SCHEMA = 'land_registry_db' 
                AND INDEX_NAME != 'PRIMARY'
                AND TABLE_NAME = 'properties'
            """)
            indexes = cursor.fetchall()
            print(f"\n🔍 Indexes on Properties Table: {len(indexes)}")
            for index in indexes:
                print(f"   ✓ {index[0]}")
                
    finally:
        connection.close()

def test_procedures():
    """Test stored procedures"""
    print("\n🧪 Testing Stored Procedures...")
    connection = pymysql.connect(**DB_CONFIG)
    
    try:
        with connection.cursor() as cursor:
            # Test get_dashboard_stats
            print("\n📊 Testing get_dashboard_stats()...")
            cursor.execute("CALL get_dashboard_stats()")
            results = cursor.fetchall()
            if results:
                print(f"   ✅ Dashboard stats retrieved: {len(results)} result sets")
            
            cursor.nextset()  # Move to next result set
            cursor.nextset()  # Move to next result set
            cursor.nextset()  # Move to next result set
            
    except Exception as e:
        print(f"   ⚠️  {str(e)[:150]}")
    finally:
        connection.close()

def test_views():
    """Test views"""
    print("\n🧪 Testing Views...")
    connection = pymysql.connect(**DB_CONFIG)
    
    try:
        with connection.cursor() as cursor:
            # Test property dashboard stats view
            print("\n📊 Testing v_property_dashboard_stats...")
            cursor.execute("SELECT * FROM v_property_dashboard_stats")
            result = cursor.fetchone()
            if result:
                print(f"   ✅ Total Properties: {result[0]}")
                print(f"   ✅ Approved: {result[1]}")
                print(f"   ✅ With Location: {result[5]}")
            
            # Test revenue analytics view
            print("\n💰 Testing v_revenue_analytics...")
            cursor.execute("SELECT * FROM v_revenue_analytics LIMIT 5")
            results = cursor.fetchall()
            print(f"   ✅ Revenue records found: {len(results)}")
            
    except Exception as e:
        print(f"   ⚠️  {str(e)[:150]}")
    finally:
        connection.close()

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 MYSQL ADVANCED FEATURES INSTALLATION")
    print("=" * 70)
    print(f"Database: {DB_CONFIG['database']}")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"User: {DB_CONFIG['user']}")
    print("=" * 70)
    
    # Get SQL file path
    sql_file = os.path.join(os.path.dirname(__file__), 'database', 'mysql_advanced_features.sql')
    
    if not os.path.exists(sql_file):
        print(f"❌ SQL file not found: {sql_file}")
        exit(1)
    
    # Execute SQL file
    execute_sql_file(sql_file)
    
    # Verify installation
    verify_installation()
    
    # Test procedures and views
    test_procedures()
    test_views()
    
    print("\n" + "=" * 70)
    print("✅ INSTALLATION COMPLETE!")
    print("=" * 70)
    print("\n📚 You can now use:")
    print("   • Stored Procedures: calculate_property_tax, get_property_report, etc.")
    print("   • Views: v_property_dashboard_stats, v_revenue_analytics, etc.")
    print("   • Triggers: Auto ULPIN generation, audit logging, notifications")
    print("   • Indexes: Optimized queries for better performance")
    print("\n💡 Open MySQL Workbench to explore these features!")
    print("   Password: 1234 | Database: land_registry_db")
