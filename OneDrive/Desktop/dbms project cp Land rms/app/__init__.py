"""
Flask application factory for Land Registry Management System.
Initializes all extensions and registers blueprints.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import config


# Initialize extensions
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()


def create_app(config_name='default'):
    """
    Application factory pattern.
    Creates and configures the Flask application.
    
    Args:
        config_name: Configuration environment name (development, testing, production)
    
    Returns:
        Configured Flask application instance
    """
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions with app
    from app.models import db
    db.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Role-based redirect after login
    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import flash, redirect, url_for, request
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login', next=request.url))
    
    # Register blueprints
    from app.routes import auth, admin, registrar, officer, citizen, api, download, public, search
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(registrar.bp, url_prefix='/registrar')
    app.register_blueprint(officer.bp, url_prefix='/officer')
    app.register_blueprint(citizen.bp, url_prefix='/citizen')
    app.register_blueprint(api.bp, url_prefix='/api/v1')
    app.register_blueprint(download.bp)
    app.register_blueprint(public.bp)  # Public verification routes (no login required)
    app.register_blueprint(search.bp)  # Advanced search routes
    
    # Register main routes
    from app.routes import main
    app.register_blueprint(main.bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        from app.models import db
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        from flask import render_template
        return render_template('errors/403.html'), 403
    
    # Context processors
    @app.context_processor
    def inject_globals():
        """Inject global variables into all templates."""
        from flask_login import current_user
        
        unread_notifications_count = 0
        recent_notifications = []
        if current_user.is_authenticated:
            from app.models.notification import Notification
            unread_notifications_count = Notification.query.filter_by(
                user_id=current_user.id,
                is_read=False
            ).count()
            
            # Get recent 5 notifications for dropdown
            recent_notifications = Notification.query.filter_by(
                user_id=current_user.id
            ).order_by(Notification.created_at.desc()).limit(5).all()
        
        return {
            'app_name': app.config.get('APP_NAME', 'LRMS'),
            'app_version': app.config.get('APP_VERSION', '1.0.0'),
            'unread_notifications_count': unread_notifications_count,
            'recent_notifications': recent_notifications
        }
    
    # Logging configuration
    if not app.debug and not app.testing:
        # Ensure logs directory exists
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Set up file handler
        file_handler = RotatingFileHandler(
            os.path.join(logs_dir, 'lrms.log'),
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Land Registry Management System startup')
    
    return app
