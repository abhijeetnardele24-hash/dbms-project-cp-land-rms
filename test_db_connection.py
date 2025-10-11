#!/usr/bin/env python3
"""
Database Connection Test Script for LRMS
Run this script to test your MySQL database connection before starting the application
"""

import sys
import os
from sqlalchemy import create_engine, text
from config import Config

def test_database_connection():
    """Test database connection and basic operations"""
    
    print("🔍 Testing LRMS Database Connection...")
    print(f"📊 Database URI: {Config.SQLALCHEMY_DATABASE_URI}")
    
    try:
        # Create engine
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        
        # Test connection
        with engine.connect() as connection:
            print("✅ Database connection successful!")
            
            # Test basic query
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("✅ Basic query test passed!")
            else:
                print("❌ Basic query test failed!")
                return False
            
            # Test database info
            if 'mysql' in Config.SQLALCHEMY_DATABASE_URI:
                result = connection.execute(text("SELECT VERSION() as version"))
                version = result.fetchone()[0]
                print(f"📋 MySQL Version: {version}")
                
                result = connection.execute(text("SELECT DATABASE() as db_name"))
                db_name = result.fetchone()[0]
                print(f"📋 Current Database: {db_name}")
            
            print("🎉 Database connection test completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure MySQL server is running")
        print("2. Check if the database 'lrms' exists")
        print("3. Verify username and password in config.py")
        print("4. Run: mysql -u root -p < setup_mysql.sql")
        return False

def main():
    """Main function"""
    success = test_database_connection()
    
    if success:
        print("\n🚀 You can now run the LRMS application:")
        print("   python app.py")
        sys.exit(0)
    else:
        print("\n⚠️  Please fix database connection issues before running the application.")
        sys.exit(1)

if __name__ == "__main__":
    main()
