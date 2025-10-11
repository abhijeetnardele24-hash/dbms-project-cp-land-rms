"""
Admin routes for Government Property Management Portal
Includes analytics, audit logs, user management, and system overview
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from utils.decorators import admin_required, role_required
from models import db
from models.user_account import UserAccount
from models.owner import Owner
from models.parcel import Parcel
from models.ownership import Ownership
from models.mutation import Mutation
from models.tax_assessment import TaxAssessment
from models.audit_log import AuditLog
from models.location import Location
from sqlalchemy import func, text
from datetime import datetime, timedelta
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard with comprehensive analytics"""
    
    # Basic statistics
    total_parcels = Parcel.query.count()
    total_owners = Owner.query.count()
    total_users = UserAccount.query.count()
    pending_mutations = Mutation.query.filter_by(status='Pending').count()
    
    # Location-wise statistics
    location_stats = db.session.query(
        Location.district,
        func.count(Parcel.parcel_id).label('parcel_count')
    ).join(Parcel).group_by(Location.district).all()
    
    # Land category distribution
    category_stats = db.session.query(
        Parcel.land_category,
        func.count(Parcel.parcel_id).label('count'),
        func.sum(Parcel.total_area).label('total_area')
    ).group_by(Parcel.land_category).all()
    
    # Tax collection statistics
    current_year = datetime.now().year
    tax_stats = db.session.query(
        func.sum(TaxAssessment.tax_due).label('total_due'),
        func.sum(TaxAssessment.amount_paid).label('total_collected'),
        func.count(TaxAssessment.tax_id).label('total_assessments')
    ).filter_by(assessment_year=current_year).first()
    
    # Recent activities
    recent_mutations = Mutation.query.order_by(Mutation.created_at.desc()).limit(5).all()
    recent_audit_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
    
    # Monthly mutation trends (last 12 months)
    mutation_trends = []
    for i in range(12):
        month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end - timedelta(days=month_end.day)
        
        count = Mutation.query.filter(
            Mutation.created_at >= month_start,
            Mutation.created_at <= month_end
        ).count()
        
        mutation_trends.append({
            'month': month_start.strftime('%b %Y'),
            'count': count
        })
    
    mutation_trends.reverse()
    
    dashboard_data = {
        'total_parcels': total_parcels,
        'total_owners': total_owners,
        'total_users': total_users,
        'pending_mutations': pending_mutations,
        'location_stats': location_stats,
        'category_stats': category_stats,
        'tax_stats': tax_stats,
        'recent_mutations': recent_mutations,
        'recent_audit_logs': recent_audit_logs,
        'mutation_trends': mutation_trends
    }
    
    return render_template('admin/dashboard.html', data=dashboard_data)

@admin_bp.route('/users')
@admin_required
def manage_users():
    """User management page"""
    page = request.args.get('page', 1, type=int)
    users = UserAccount.query.paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create new user"""
    if request.method == 'POST':
        try:
            user = UserAccount(
                username=request.form.get('username'),
                role=request.form.get('role'),
                is_active=True
            )
            user.set_password(request.form.get('password'))
            
            db.session.add(user)
            db.session.commit()
            
            flash('User created successfully!', 'success')
            return redirect(url_for('admin.manage_users'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'error')
    
    return render_template('admin/user_form.html', user=None)

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit existing user"""
    user = UserAccount.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            user.username = request.form.get('username')
            user.role = request.form.get('role')
            user.is_active = request.form.get('is_active') == 'on'
            
            # Update password if provided
            new_password = request.form.get('password')
            if new_password:
                user.set_password(new_password)
            
            db.session.commit()
            
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.manage_users'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
    
    return render_template('admin/user_form.html', user=user)

@admin_bp.route('/audit-logs')
@admin_required
def audit_logs():
    """View audit logs with filtering"""
    page = request.args.get('page', 1, type=int)
    table_filter = request.args.get('table', '')
    action_filter = request.args.get('action', '')
    user_filter = request.args.get('user', '')
    
    query = AuditLog.query
    
    if table_filter:
        query = query.filter_by(table_name=table_filter)
    
    if action_filter:
        query = query.filter_by(action=action_filter)
    
    if user_filter:
        query = query.filter_by(user_id=user_filter)
    
    audit_logs = query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    # Get filter options
    tables = db.session.query(AuditLog.table_name).distinct().all()
    actions = db.session.query(AuditLog.action).distinct().all()
    users = UserAccount.query.all()
    
    return render_template('admin/audit_logs.html', 
                         audit_logs=audit_logs,
                         tables=[t[0] for t in tables],
                         actions=[a[0] for a in actions],
                         users=users,
                         filters={
                             'table': table_filter,
                             'action': action_filter,
                             'user': user_filter
                         })

@admin_bp.route('/analytics')
@admin_required
def analytics():
    """Advanced analytics page"""
    
    # Parcel analytics
    parcel_analytics = {
        'total_area': db.session.query(func.sum(Parcel.total_area)).scalar() or 0,
        'avg_area': db.session.query(func.avg(Parcel.total_area)).scalar() or 0,
        'category_distribution': db.session.query(
            Parcel.land_category,
            func.count(Parcel.parcel_id),
            func.sum(Parcel.total_area)
        ).group_by(Parcel.land_category).all()
    }
    
    # Ownership analytics
    ownership_analytics = {
        'total_ownerships': Ownership.query.filter_by(date_to=None).count(),
        'joint_ownerships': Ownership.query.filter_by(
            ownership_type='Joint', date_to=None
        ).count(),
        'avg_share': db.session.query(func.avg(Ownership.share_fraction)).filter_by(
            date_to=None
        ).scalar() or 0
    }
    
    # Mutation analytics
    mutation_analytics = {
        'total_mutations': Mutation.query.count(),
        'approved_mutations': Mutation.query.filter_by(status='Approved').count(),
        'pending_mutations': Mutation.query.filter_by(status='Pending').count(),
        'rejected_mutations': Mutation.query.filter_by(status='Rejected').count(),
        'type_distribution': db.session.query(
            Mutation.mutation_type,
            func.count(Mutation.mutation_id)
        ).group_by(Mutation.mutation_type).all()
    }
    
    # Tax analytics
    tax_analytics = {
        'total_due': db.session.query(func.sum(TaxAssessment.tax_due)).scalar() or 0,
        'total_collected': db.session.query(func.sum(TaxAssessment.amount_paid)).scalar() or 0,
        'yearly_collection': db.session.query(
            TaxAssessment.assessment_year,
            func.sum(TaxAssessment.tax_due),
            func.sum(TaxAssessment.amount_paid)
        ).group_by(TaxAssessment.assessment_year).order_by(TaxAssessment.assessment_year.desc()).all()
    }
    
    analytics_data = {
        'parcel': parcel_analytics,
        'ownership': ownership_analytics,
        'mutation': mutation_analytics,
        'tax': tax_analytics
    }
    
    return render_template('admin/analytics.html', data=analytics_data)

@admin_bp.route('/system-info')
@admin_required
def system_info():
    """System information and health check"""
    
    # Database statistics
    db_stats = {}
    tables = ['owner', 'parcel', 'ownership', 'mutation', 'tax_assessment', 'audit_log', 'user_account']
    
    for table in tables:
        try:
            result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            db_stats[table] = result
        except Exception as e:
            db_stats[table] = f"Error: {str(e)}"
    
    # Recent activity summary
    activity_summary = {
        'recent_logins': UserAccount.query.filter(
            UserAccount.last_login >= datetime.now() - timedelta(days=7)
        ).count(),
        'recent_mutations': Mutation.query.filter(
            Mutation.created_at >= datetime.now() - timedelta(days=7)
        ).count(),
        'recent_tax_payments': TaxAssessment.query.filter(
            TaxAssessment.paid_on >= datetime.now() - timedelta(days=7)
        ).count() if TaxAssessment.query.filter(TaxAssessment.paid_on.isnot(None)).first() else 0
    }
    
    system_data = {
        'db_stats': db_stats,
        'activity_summary': activity_summary,
        'current_time': datetime.now(),
        'app_version': '1.0.0',
        'database_type': 'MySQL'
    }
    
    return render_template('admin/system_info.html', data=system_data)

@admin_bp.route('/api/analytics/charts')
@admin_required
def analytics_charts_api():
    """API endpoint for chart data"""
    chart_type = request.args.get('type', 'mutations')
    
    if chart_type == 'mutations':
        # Monthly mutation data for last 12 months
        data = []
        for i in range(12):
            month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end - timedelta(days=month_end.day)
            
            count = Mutation.query.filter(
                Mutation.created_at >= month_start,
                Mutation.created_at <= month_end
            ).count()
            
            data.append({
                'month': month_start.strftime('%b %Y'),
                'count': count
            })
        
        data.reverse()
        return jsonify(data)
    
    elif chart_type == 'land_categories':
        # Land category distribution
        categories = db.session.query(
            Parcel.land_category,
            func.count(Parcel.parcel_id).label('count')
        ).group_by(Parcel.land_category).all()
        
        return jsonify([{
            'category': cat[0],
            'count': cat[1]
        } for cat in categories])
    
    elif chart_type == 'tax_collection':
        # Yearly tax collection
        years = db.session.query(
            TaxAssessment.assessment_year,
            func.sum(TaxAssessment.tax_due).label('due'),
            func.sum(TaxAssessment.amount_paid).label('collected')
        ).group_by(TaxAssessment.assessment_year).order_by(TaxAssessment.assessment_year).all()
        
        return jsonify([{
            'year': year[0],
            'due': float(year[1] or 0),
            'collected': float(year[2] or 0)
        } for year in years])
    
    return jsonify({'error': 'Invalid chart type'})
