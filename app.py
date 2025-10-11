from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db
from models.user_account import UserAccount
from models.parcel import Parcel
from models.ownership import Ownership
from models.mutation import Mutation
from models.tax_assessment import TaxAssessment
from routes.auth_routes import auth_bp
from routes.owner_routes import owner_bp
from routes.parcel_routes import parcel_bp
from routes.mutation_routes import mutation_bp
from routes.tax_routes import tax_bp
from routes.tax_routes_new import tax_new_bp
from routes.tax_working import tax_working_bp
from routes.tax_simple import tax_simple_bp
from routes.admin_routes import admin_bp
from routes.document_routes import document_bp
from utils.audit import setup_audit_listeners
from utils.decorators import role_required
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return UserAccount.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(owner_bp)
    from routes.parcel_routes import parcel_bp
    app.register_blueprint(parcel_bp)
    from routes.document_routes import document_bp
    app.register_blueprint(document_bp)
    app.register_blueprint(mutation_bp)
    app.register_blueprint(tax_bp)
    app.register_blueprint(tax_new_bp)
    app.register_blueprint(tax_working_bp)
    app.register_blueprint(tax_simple_bp)
    from routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)
    
    from routes.tenant_routes import tenant_bp
    app.register_blueprint(tenant_bp)
    
    # Main routes
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth.login'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Dashboard statistics
        total_parcels = Parcel.query.count()
        total_owners = db.session.query(Ownership.owner_id).distinct().count()
        pending_mutations = Mutation.query.filter_by(status='Pending').count()
        
        # Recent parcels
        recent_parcels = Parcel.query.order_by(Parcel.created_at.desc()).limit(5).all()
        
        # Tax collection summary for current year
        current_year = datetime.now().year
        current_year_taxes = TaxAssessment.query.filter_by(assessment_year=current_year).all()
        total_tax_due = sum(tax.tax_due for tax in current_year_taxes)
        total_tax_collected = sum(tax.amount_paid or 0 for tax in current_year_taxes)
        
        # Recent mutations
        recent_mutations = Mutation.query.order_by(Mutation.created_at.desc()).limit(5).all()
        
        dashboard_data = {
            'total_parcels': total_parcels,
            'total_owners': total_owners,
            'pending_mutations': pending_mutations,
            'recent_parcels': recent_parcels,
            'total_tax_due': total_tax_due,
            'total_tax_collected': total_tax_collected,
            'collection_rate': (total_tax_collected / total_tax_due * 100) if total_tax_due > 0 else 0,
            'recent_mutations': recent_mutations
        }
        
        return render_template('dashboard.html', data=dashboard_data)
    
    # Setup audit listeners - temporarily disabled to fix session issues
    # setup_audit_listeners()
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin_user = UserAccount.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = UserAccount(
                username='admin',
                role='Admin',
                is_active=True
            )
            admin_user.set_password('admin123')  # Change this in production
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created: username='admin', password='admin123'")
        
        # Create sample registrar and approver users
        registrar_user = UserAccount.query.filter_by(username='registrar').first()
        if not registrar_user:
            registrar_user = UserAccount(
                username='registrar',
                role='Registrar',
                is_active=True
            )
            registrar_user.set_password('registrar123')
            db.session.add(registrar_user)
            db.session.commit()
            print("Default registrar user created: username='registrar', password='registrar123'")
        
        approver_user = UserAccount.query.filter_by(username='approver').first()
        if not approver_user:
            approver_user = UserAccount(
                username='approver',
                role='Approver',
                is_active=True
            )
            approver_user.set_password('approver123')
            db.session.add(approver_user)
            db.session.commit()
            print("Default approver user created: username='approver', password='approver123'")
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5007)
