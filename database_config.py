"""
Database Configuration Helper for LRMS
This file provides different database configuration options
"""

import os

class DatabaseConfig:
    """Database configuration options"""
    
    # MySQL Configuration (Default)
    MYSQL_LOCAL = "mysql+pymysql://root:password@localhost/lrms"
    MYSQL_CUSTOM = "mysql+pymysql://lrms_user:lrms_password@localhost/lrms"
    
    # SQLite Configuration (for development/testing)
    SQLITE_LOCAL = "sqlite:///lrms.db"
    
    # PostgreSQL Configuration (alternative)
    POSTGRESQL_LOCAL = "postgresql://lrms_user:lrms_password@localhost/lrms"
    
    @staticmethod
    def get_database_uri():
        """Get database URI from environment or use default MySQL"""
        return os.environ.get('DATABASE_URL') or DatabaseConfig.MYSQL_LOCAL
    
    @staticmethod
    def get_mysql_connection_string(host='localhost', user='root', password='password', database='lrms'):
        """Generate MySQL connection string with custom parameters"""
        return f"mysql+pymysql://{user}:{password}@{host}/{database}"

# Example usage in config.py:
# from database_config import DatabaseConfig
# SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_database_uri()

# Or for custom MySQL settings:
# SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_mysql_connection_string(
#     user='your_user', 
#     password='your_password', 
#     database='your_database'
# )
