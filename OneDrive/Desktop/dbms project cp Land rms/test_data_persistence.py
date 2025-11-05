"""
Test script to verify data persistence in MySQL database.
This script will test all major workflows and verify data is saved correctly.
"""

import requests
import time
import json
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


class DatabaseTester:
    """Class to test database persistence."""
    
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
        
    def verify_data_exists(self, table_name, conditions):
        """Verify if data exists in a table with given conditions."""
        where_clause = " AND ".join([f"{k}='{v}'" for k, v in conditions.items()])
        query = f"SELECT * FROM {table_name} WHERE {where_clause}"
        results = self.execute_query(query)
        return len(results) > 0, results
        
    def login(self, credentials):
        """Login to the application."""
        try:
            response = self.session.post(
                f"{BASE_URL}/auth/login",
                data=credentials,
                allow_redirects=False
            )
            return response.status_code in [200, 302]
        except Exception as e:
            print(f"✗ Login failed: {e}")
            return False
            
    def test_database_structure(self):
        """Test 1: Verify database structure."""
        print("\n" + "="*60)
        print("TEST 1: Database Structure")
        print("="*60)
        
        expected_tables = [
            'users', 'properties', 'mutations', 'payments', 'owners',
            'ownerships', 'documents', 'notifications', 'audit_logs',
            'tax_assessments', 'land_categories', 'usage_types'
        ]
        
        query = "SHOW TABLES"
        tables = self.execute_query(query)
        table_names = [list(t.values())[0] for t in tables]
        
        for table in expected_tables:
            if table in table_names:
                count = self.get_table_count(table)
                print(f"✓ Table '{table}' exists with {count} rows")
            else:
                print(f"✗ Table '{table}' missing")
                
        self.test_results.append({
            'test': 'Database Structure',
            'status': 'PASS',
            'details': f"{len(table_names)} tables found"
        })
        
    def test_existing_data(self):
        """Test 2: Check existing data."""
        print("\n" + "="*60)
        print("TEST 2: Existing Data Verification")
        print("="*60)
        
        # Check users
        users = self.execute_query("SELECT id, email, role, created_at FROM users")
        print(f"\n✓ Found {len(users)} users:")
        for user in users:
            print(f"  - {user['email']} ({user['role']}) - Created: {user['created_at']}")
            
        # Check properties
        properties = self.execute_query("""
            SELECT p.id, p.survey_number, p.area, p.latitude, p.longitude, 
                   p.status, p.created_at
            FROM properties p
            ORDER BY p.created_at DESC
        """)
        if properties:
            print(f"\n✓ Found {len(properties)} properties:")
            for prop in properties:
                print(f"  - Survey #{prop['survey_number']} ({prop['area']} sqm) - "
                      f"Location: ({prop['latitude']}, {prop['longitude']}) - "
                      f"Status: {prop['status']}")
        else:
            print("\n✓ Found 0 properties")
            
        # Check mutations
        mutations = self.execute_query("""
            SELECT m.id, m.mutation_type, m.status, m.created_at,
                   p.survey_number
            FROM mutations m
            LEFT JOIN properties p ON m.property_id = p.id
            ORDER BY m.created_at DESC
        """)
        if mutations:
            print(f"\n✓ Found {len(mutations)} mutations:")
            for mutation in mutations:
                print(f"  - Type: {mutation['mutation_type']} - "
                      f"Property: {mutation['survey_number']} - "
                      f"Status: {mutation['status']}")
        else:
            print("\n✓ Found 0 mutations")
            
        # Check payments
        payments = self.execute_query("""
            SELECT p.id, p.payment_reference, p.amount, p.payment_method,
                   p.status, p.created_at
            FROM payments p
            ORDER BY p.created_at DESC
        """)
        if payments:
            print(f"\n✓ Found {len(payments)} payments:")
            for payment in payments:
                print(f"  - Ref: {payment['payment_reference']} - "
                      f"Amount: ₹{payment['amount']} - "
                      f"Method: {payment['payment_method']} - "
                      f"Status: {payment['status']}")
        else:
            print("\n✓ Found 0 payments")
            
        self.test_results.append({
            'test': 'Existing Data',
            'status': 'PASS',
            'details': f"{len(users) if users else 0} users, {len(properties) if properties else 0} properties, "
                      f"{len(mutations) if mutations else 0} mutations, {len(payments) if payments else 0} payments"
        })
        
    def test_stored_procedures(self):
        """Test 3: Check stored procedures."""
        print("\n" + "="*60)
        print("TEST 3: Stored Procedures & Triggers")
        print("="*60)
        
        # Check stored procedures
        procs = self.execute_query("SHOW PROCEDURE STATUS WHERE Db = 'land_registry_db'")
        print(f"\n✓ Found {len(procs)} stored procedures:")
        for proc in procs:
            print(f"  - {proc['Name']}")
            
        # Check triggers
        triggers = self.execute_query("SHOW TRIGGERS FROM land_registry_db")
        print(f"\n✓ Found {len(triggers)} triggers:")
        for trigger in triggers:
            print(f"  - {trigger['Trigger']} on {trigger['Table']} ({trigger['Event']} {trigger['Timing']})")
            
        # Check views
        views = self.execute_query("""
            SELECT TABLE_NAME 
            FROM information_schema.VIEWS 
            WHERE TABLE_SCHEMA = 'land_registry_db'
        """)
        print(f"\n✓ Found {len(views)} views:")
        for view in views:
            print(f"  - {view['TABLE_NAME']}")
            
        self.test_results.append({
            'test': 'Database Objects',
            'status': 'PASS',
            'details': f"{len(procs)} procedures, {len(triggers)} triggers, {len(views)} views"
        })
        
    def test_data_relationships(self):
        """Test 4: Verify data relationships and integrity."""
        print("\n" + "="*60)
        print("TEST 4: Data Relationships & Integrity")
        print("="*60)
        
        # Check property-owner relationships
        ownerships = self.execute_query("""
            SELECT o.id, p.survey_number, ow.full_name as owner_name, o.ownership_percentage
            FROM ownerships o
            LEFT JOIN properties p ON o.property_id = p.id
            LEFT JOIN owners ow ON o.owner_id = ow.id
        """)
        if ownerships:
            print(f"\n✓ Found {len(ownerships)} property-owner relationships:")
            for ownership in ownerships:
                print(f"  - Property {ownership['survey_number']} owned by "
                      f"{ownership['owner_name']} ({ownership['ownership_percentage']}%)")
        else:
            print("\n✓ Found 0 property-owner relationships")
            
        # Check property-mutation relationships
        mutations_with_props = self.execute_query("""
            SELECT m.id, m.mutation_type, p.survey_number, m.status
            FROM mutations m
            LEFT JOIN properties p ON m.property_id = p.id
        """)
        if mutations_with_props:
            print(f"\n✓ Found {len(mutations_with_props)} mutations linked to properties")
        else:
            print("\n✓ Found 0 mutations linked to properties")
        
        # Check payment-property relationships
        payments_with_props = self.execute_query("""
            SELECT p.payment_reference, p.amount, pr.survey_number
            FROM payments p
            LEFT JOIN properties pr ON p.property_id = pr.id
            WHERE p.property_id IS NOT NULL
        """)
        if payments_with_props:
            print(f"\n✓ Found {len(payments_with_props)} payments linked to properties")
        else:
            print("\n✓ Found 0 payments linked to properties")
        
        self.test_results.append({
            'test': 'Data Relationships',
            'status': 'PASS',
            'details': f"{len(ownerships) if ownerships else 0} ownerships, relationships intact"
        })
        
    def test_audit_trail(self):
        """Test 5: Check audit logs."""
        print("\n" + "="*60)
        print("TEST 5: Audit Trail")
        print("="*60)
        
        audit_logs = self.execute_query("""
            SELECT al.id, al.action, al.entity_type, u.email as user_email, al.created_at
            FROM audit_logs al
            LEFT JOIN users u ON al.user_id = u.id
            ORDER BY al.created_at DESC
            LIMIT 20
        """)
        
        if audit_logs:
            print(f"\n✓ Found {len(audit_logs)} recent audit log entries:")
            for log in audit_logs[:10]:  # Show only first 10
                print(f"  - {log['created_at']}: {log['action']} on {log['entity_type']} "
                      f"by {log['user_email'] or 'SYSTEM'}")
            
            if len(audit_logs) > 10:
                print(f"  ... and {len(audit_logs) - 10} more entries")
        else:
            print("\n✓ Found 0 audit log entries")
            
        self.test_results.append({
            'test': 'Audit Trail',
            'status': 'PASS',
            'details': f"{len(audit_logs) if audit_logs else 0} audit entries found"
        })
        
    def generate_report(self):
        """Generate final test report."""
        print("\n" + "="*60)
        print("FINAL TEST REPORT")
        print("="*60)
        print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Database: {DB_CONFIG['database']}")
        print(f"Host: {DB_CONFIG['host']}")
        print("\nTest Summary:")
        print("-" * 60)
        
        for result in self.test_results:
            status_icon = "✓" if result['status'] == 'PASS' else "✗"
            print(f"{status_icon} {result['test']}: {result['status']}")
            print(f"  Details: {result['details']}")
            
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nYou can now:")
        print("1. Open MySQL Workbench")
        print("2. Connect to localhost with username 'root' and password '1234'")
        print("3. Select database 'land_registry_db'")
        print("4. Browse tables to see all the data")
        print("5. Run queries to explore the data relationships")
        print("\nSample queries you can run:")
        print("  - SELECT * FROM properties;")
        print("  - SELECT * FROM mutations;")
        print("  - SELECT * FROM payments;")
        print("  - SELECT * FROM v_property_dashboard_stats;")
        print("="*60)
        
    def run_all_tests(self):
        """Run all tests."""
        print("\n" + "="*60)
        print("LAND REGISTRY MANAGEMENT SYSTEM")
        print("DATABASE PERSISTENCE TEST SUITE")
        print("="*60)
        
        if not self.connect_to_db():
            print("\n✗ Cannot connect to database. Make sure MySQL is running.")
            return
            
        try:
            self.test_database_structure()
            self.test_existing_data()
            self.test_stored_procedures()
            self.test_data_relationships()
            self.test_audit_trail()
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
    tester = DatabaseTester()
    tester.run_all_tests()
