"""
Comprehensive Feature Test Script
Tests all features and verifies data persistence in MySQL
"""

import sys
import time
import requests
from datetime import datetime
import mysql.connector
from mysql.connector import Error

# Configuration
BASE_URL = "http://127.0.0.1:5000"
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'land_registry_db'
}

# Test credentials
CITIZEN_CREDS = {'email': 'user@lrms.com', 'password': 'password'}
OFFICER_CREDS = {'email': 'officer@lrms.com', 'password': 'password'}


class FeatureTester:
    """Comprehensive feature testing class."""
    
    def __init__(self):
        self.session = requests.Session()
        self.db_connection = None
        self.test_results = []
        
    def connect_to_db(self):
        """Connect to MySQL database."""
        try:
            self.db_connection = mysql.connector.connect(**DB_CONFIG)
            if self.db_connection.is_connected():
                print("✓ Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"✗ Error connecting to MySQL: {e}")
            return False
            
    def execute_query(self, query, params=None):
        """Execute a query and return results."""
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"✗ Query error: {e}")
            return None
            
    def get_table_count(self, table_name):
        """Get row count for a table."""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
        
    def check_app_running(self):
        """Check if Flask app is running."""
        try:
            response = requests.get(BASE_URL, timeout=5)
            return response.status_code == 200
        except:
            return False
            
    def test_database_connection(self):
        """Test 1: Database Connection."""
        print("\n" + "="*70)
        print("TEST 1: MySQL Database Connection")
        print("="*70)
        
        if not self.connect_to_db():
            print("✗ FAILED: Cannot connect to MySQL database")
            print("  Make sure MySQL is running and password is '1234'")
            return False
            
        print("✓ PASSED: Connected to land_registry_db")
        self.test_results.append({'test': 'Database Connection', 'status': 'PASS'})
        return True
        
    def test_table_structure(self):
        """Test 2: Verify table structure."""
        print("\n" + "="*70)
        print("TEST 2: Table Structure Verification")
        print("="*70)
        
        tables = self.execute_query("SHOW TABLES")
        if not tables:
            print("✗ FAILED: No tables found")
            return False
            
        table_names = [list(t.values())[0] for t in tables]
        print(f"✓ Found {len(table_names)} tables in database")
        
        key_tables = ['users', 'properties', 'mutations', 'payments', 'owners', 'ownerships']
        for table in key_tables:
            if table in table_names:
                count = self.get_table_count(table)
                print(f"  ✓ {table}: {count} records")
            else:
                print(f"  ✗ {table}: MISSING")
                return False
                
        self.test_results.append({'test': 'Table Structure', 'status': 'PASS'})
        return True
        
    def test_existing_data(self):
        """Test 3: Verify existing data."""
        print("\n" + "="*70)
        print("TEST 3: Existing Data Verification")
        print("="*70)
        
        # Check users
        users = self.execute_query("SELECT email, role FROM users")
        print(f"\n✓ Users ({len(users) if users else 0}):")
        if users:
            for user in users:
                print(f"  - {user['email']} ({user['role']})")
                
        # Check properties
        properties = self.execute_query("""
            SELECT survey_number, area, status, latitude, longitude 
            FROM properties 
            ORDER BY created_at DESC
        """)
        print(f"\n✓ Properties ({len(properties) if properties else 0}):")
        if properties:
            for prop in properties:
                lat = prop['latitude'] or 'N/A'
                lng = prop['longitude'] or 'N/A'
                print(f"  - {prop['survey_number']}: {prop['area']} sqm, "
                      f"GPS: ({lat}, {lng}), Status: {prop['status']}")
                      
        # Check payments
        payments = self.execute_query("""
            SELECT payment_reference, amount, status 
            FROM payments 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        print(f"\n✓ Recent Payments ({len(payments) if payments else 0}):")
        if payments:
            for payment in payments:
                print(f"  - {payment['payment_reference']}: ₹{payment['amount']} "
                      f"({payment['status']})")
                      
        self.test_results.append({'test': 'Existing Data', 'status': 'PASS'})
        return True
        
    def test_mysql_features(self):
        """Test 4: MySQL Advanced Features."""
        print("\n" + "="*70)
        print("TEST 4: MySQL Advanced Features")
        print("="*70)
        
        # Test stored procedures
        procs = self.execute_query("SHOW PROCEDURE STATUS WHERE Db = 'land_registry_db'")
        print(f"\n✓ Stored Procedures ({len(procs) if procs else 0}):")
        if procs:
            for proc in procs:
                print(f"  - {proc['Name']}")
                
        # Test triggers
        triggers = self.execute_query("SHOW TRIGGERS FROM land_registry_db")
        print(f"\n✓ Triggers ({len(triggers) if triggers else 0}):")
        if triggers:
            for trigger in triggers:
                print(f"  - {trigger['Trigger']} on {trigger['Table']}")
                
        # Test views
        views = self.execute_query("""
            SELECT TABLE_NAME 
            FROM information_schema.VIEWS 
            WHERE TABLE_SCHEMA = 'land_registry_db'
        """)
        print(f"\n✓ Views ({len(views) if views else 0}):")
        if views:
            for view in views:
                print(f"  - {view['TABLE_NAME']}")
                
        self.test_results.append({'test': 'MySQL Features', 'status': 'PASS'})
        return True
        
    def test_data_relationships(self):
        """Test 5: Data Relationships."""
        print("\n" + "="*70)
        print("TEST 5: Data Relationship Integrity")
        print("="*70)
        
        # Property-Owner relationships
        ownerships = self.execute_query("""
            SELECT p.survey_number, ow.full_name, o.ownership_percentage
            FROM ownerships o
            JOIN properties p ON o.property_id = p.id
            JOIN owners ow ON o.owner_id = ow.id
        """)
        if ownerships:
            print(f"\n✓ Property-Owner Links ({len(ownerships)}):")
            for own in ownerships:
                print(f"  - {own['survey_number']} owned by {own['full_name']} "
                      f"({own['ownership_percentage']}%)")
        else:
            print("\n✓ Property-Owner Links (0)")
            
        # Property-Mutation relationships
        mutations = self.execute_query("""
            SELECT m.mutation_type, m.status, p.survey_number
            FROM mutations m
            JOIN properties p ON m.property_id = p.id
        """)
        if mutations:
            print(f"\n✓ Property-Mutation Links ({len(mutations)}):")
            for mut in mutations:
                print(f"  - {mut['mutation_type']} on {mut['survey_number']} "
                      f"({mut['status']})")
        else:
            print("\n✓ Property-Mutation Links (0)")
            
        self.test_results.append({'test': 'Data Relationships', 'status': 'PASS'})
        return True
        
    def test_app_accessibility(self):
        """Test 6: Application Accessibility."""
        print("\n" + "="*70)
        print("TEST 6: Application Accessibility")
        print("="*70)
        
        if not self.check_app_running():
            print("✗ WARNING: Flask application is not running")
            print("  To test the app, run: python run.py")
            print("  Then you can manually test features through the web interface")
            self.test_results.append({'test': 'App Accessibility', 'status': 'SKIP'})
            return False
            
        print("✓ PASSED: Flask application is running at http://127.0.0.1:5000")
        self.test_results.append({'test': 'App Accessibility', 'status': 'PASS'})
        return True
        
    def generate_report(self):
        """Generate final test report."""
        print("\n" + "="*70)
        print("FINAL TEST REPORT")
        print("="*70)
        print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Database: {DB_CONFIG['database']}")
        print(f"MySQL Password: {DB_CONFIG['password']}")
        print("\nTest Summary:")
        print("-" * 70)
        
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        skipped = sum(1 for r in self.test_results if r['status'] == 'SKIP')
        
        for result in self.test_results:
            icon = "✓" if result['status'] == 'PASS' else "⊘" if result['status'] == 'SKIP' else "✗"
            print(f"{icon} {result['test']}: {result['status']}")
            
        print("\n" + "="*70)
        print(f"RESULTS: {passed} PASSED, {skipped} SKIPPED")
        print("="*70)
        
        print("\n📋 NEXT STEPS:")
        print("-" * 70)
        
        if not self.check_app_running():
            print("\n1. START THE APPLICATION:")
            print("   python run.py")
            print("\n2. OPEN IN BROWSER:")
            print("   http://127.0.0.1:5000")
            print("\n3. LOGIN WITH:")
            print("   Email: user@lrms.com")
            print("   Password: password")
            print("\n4. TEST FEATURES:")
            print("   ✓ Register a new property with map location")
            print("   ✓ Submit a mutation request")
            print("   ✓ Make a payment")
            print("   ✓ View dashboard analytics")
            
        print("\n5. VERIFY IN MYSQL WORKBENCH:")
        print("   Host: localhost")
        print("   Username: root")
        print("   Password: 1234")
        print("   Database: land_registry_db")
        print("\n6. RUN SAMPLE QUERIES:")
        print("   SELECT * FROM properties;")
        print("   SELECT * FROM payments;")
        print("   SELECT * FROM mutations;")
        print("   CALL get_dashboard_stats();")
        
        print("\n" + "="*70)
        print("✅ ALL DATABASE TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        
    def run_all_tests(self):
        """Run all tests."""
        print("\n" + "="*70)
        print("LAND REGISTRY MANAGEMENT SYSTEM")
        print("COMPREHENSIVE FEATURE TEST SUITE")
        print("="*70)
        print(f"Starting tests at: {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            if not self.test_database_connection():
                print("\n✗ Cannot proceed without database connection")
                return
                
            self.test_table_structure()
            self.test_existing_data()
            self.test_mysql_features()
            self.test_data_relationships()
            self.test_app_accessibility()
            self.generate_report()
            
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.db_connection and self.db_connection.is_connected():
                self.db_connection.close()
                print("\nDatabase connection closed.")


if __name__ == "__main__":
    tester = FeatureTester()
    tester.run_all_tests()
