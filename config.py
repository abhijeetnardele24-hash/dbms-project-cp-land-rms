import os
from urllib.parse import quote_plus

class Config:
    # Database Configuration
    # Use SQLite for development
    SQLALCHEMY_DATABASE_URI = "sqlite:///lrms.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Engine options for MySQL; for SQLite, use defaults
    if 'sqlite' not in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'connect_args': {
                'connect_timeout': 60,
                'read_timeout': 60,
                'write_timeout': 60
            }
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}
    
    # Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or "your_secret_key_here_change_in_production"
    
    # Upload Configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Application Configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
