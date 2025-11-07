"""
Admin routes for system management and oversight.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import func
from app.models import db
from app.models.user import User
from app.models.property import Property
from app.models.mutation import Mutation
from app.models.payment import Payment
from app.models.audit_log import AuditLog
from app.utils.decorators import admin_required
from app.forms.user_forms import UserManagementForm

bp = Blueprint('admin', __name__)


@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with system-wide statistics."""
    
    # Get statistics
    total_users = User.query.count()
    total_properties = Property.query.count()
    pending_registrations = Property.query.filter_by(status='pending').count()
    pending_mutations = Mutation.query.filter_by(status='pending').count()
    
    # Revenue statistics
    total_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.status == 'completed'
    ).scalar() or 0
    
    # Recent activities
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()
    
    # User distribution by role
    user_stats = db.session.query(
        User.role,
        func.count(User.id)
    ).group_by(User.role).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_properties=total_properties,
                         pending_registrations=pending_registrations,
                         pending_mutations=pending_mutations,
                         total_revenue=total_revenue,
                         recent_logs=recent_logs,
                         user_stats=user_stats)


@bp.route('/users')
@login_required
@admin_required
def users():
    """User management page."""
    page = request.args.get('page', 1, type=int)
    role = request.args.get('role', '')
    
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    
    users_pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('admin/users.html', users=users_pagination)


@bp.route('/user/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    """Create new user."""
    form = UserManagementForm()
    
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            full_name=form.full_name.data,
            role=form.role.data,
            phone=form.phone.data,
            address=form.address.data,
            is_active=form.is_active.data
        )
        
        if form.password.data:
            user.set_password(form.password.data)
        else:
            user.set_password('password123')  # Default password
        
        db.session.add(user)
        
        # Log action
        AuditLog.log_action(
            user_id=current_user.id,
            action='create_user',
            action_type='create',
            entity_type='user',
            entity_id=user.id,
            description=f'Admin created new user: {user.email}',
            status='success'
        )
        
        db.session.commit()
        
        flash(f'User {user.email} created successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', form=form, action='Create')


@bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edit existing user."""
    user = User.query.get_or_404(user_id)
    form = UserManagementForm(obj=user)
    
    if form.validate_on_submit():
        user.email = form.email.data
        user.full_name = form.full_name.data
        user.role = form.role.data
        user.phone = form.phone.data
        user.address = form.address.data
        user.is_active = form.is_active.data
        
        if form.password.data:
            user.set_password(form.password.data)
        
        # Log action
        AuditLog.log_action(
            user_id=current_user.id,
            action='update_user',
            action_type='update',
            entity_type='user',
            entity_id=user.id,
            description=f'Admin updated user: {user.email}',
            status='success'
        )
        
        db.session.commit()
        
        flash(f'User {user.email} updated successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', form=form, action='Edit', user=user)


@bp.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete user."""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin.users'))
    
    email = user.email
    
    # Log action before deletion
    AuditLog.log_action(
        user_id=current_user.id,
        action='delete_user',
        action_type='delete',
        entity_type='user',
        entity_id=user.id,
        description=f'Admin deleted user: {email}',
        status='success'
    )
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {email} deleted successfully!', 'success')
    return redirect(url_for('admin.users'))


@bp.route('/properties')
@login_required
@admin_required
def properties():
    """View all properties."""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = Property.query
    
    if status:
        query = query.filter_by(status=status)
    
    if search:
        query = query.filter(
            db.or_(
                Property.ulpin.like(f'%{search}%'),
                Property.district.like(f'%{search}%'),
                Property.village_city.like(f'%{search}%')
            )
        )
    
    # Increase per_page to show more properties (50 instead of 10)
    properties_pagination = query.order_by(Property.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    # Get mutation counts for each property
    property_mutations = {}
    for prop in properties_pagination.items:
        mutation_count = Mutation.query.filter_by(property_id=prop.id).count()
        mutations = Mutation.query.filter_by(property_id=prop.id).order_by(Mutation.created_at.desc()).all()
        property_mutations[prop.id] = {
            'count': mutation_count,
            'mutations': mutations
        }
    
    return render_template('admin/properties.html', 
                         properties=properties_pagination,
                         property_mutations=property_mutations)


@bp.route('/mutations')
@login_required
@admin_required
def mutations():
    """View all mutations."""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Mutation.query
    
    if status:
        query = query.filter_by(status=status)
    
    mutations_pagination = query.order_by(Mutation.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('admin/mutations.html', mutations=mutations_pagination)


@bp.route('/payments')
@login_required
@admin_required
def payments():
    """View all payments."""
    page = request.args.get('page', 1, type=int)
    
    payments_pagination = Payment.query.order_by(Payment.payment_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/payments.html', payments=payments_pagination)


@bp.route('/audit-logs')
@login_required
@admin_required
def audit_logs():
    """View audit logs."""
    page = request.args.get('page', 1, type=int)
    action_type = request.args.get('action_type', '')
    
    query = AuditLog.query
    
    if action_type:
        query = query.filter_by(action_type=action_type)
    
    logs_pagination = query.order_by(AuditLog.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/audit_logs.html', logs=logs_pagination)


@bp.route('/reports')
@login_required
@admin_required
def reports():
    """Reports and analytics page."""
    return render_template('admin/reports.html')


@bp.route('/api/analytics/dashboard')
@login_required
@admin_required
def analytics_dashboard():
    """API endpoint for dashboard analytics data."""
    try:
        # Query the real-time dashboard stats view
        result = db.session.execute(
            "SELECT * FROM vw_realtime_dashboard_stats"
        ).fetchone()
        
        if result:
            stats = {
                'total_properties': result[0] or 0,
                'approved_properties': result[1] or 0,
                'pending_properties': result[2] or 0,
                'rejected_properties': result[3] or 0,
                'total_mutations': result[4] or 0,
                'pending_mutations': result[5] or 0,
                'approved_mutations': result[6] or 0,
                'total_users': result[7] or 0,
                'citizen_users': result[8] or 0,
                'total_revenue': float(result[9]) if result[9] else 0,
                'monthly_revenue': float(result[10]) if result[10] else 0,
                'pending_payments': float(result[11]) if result[11] else 0,
                'total_property_value': float(result[12]) if result[12] else 0,
                'avg_property_value': float(result[13]) if result[13] else 0
            }
        else:
            # Fallback to direct queries
            stats = {
                'total_properties': Property.query.count(),
                'approved_properties': Property.query.filter_by(status='approved').count(),
                'pending_properties': Property.query.filter_by(status='pending').count(),
                'rejected_properties': Property.query.filter_by(status='rejected').count(),
                'total_mutations': Mutation.query.count(),
                'pending_mutations': Mutation.query.filter_by(status='pending').count(),
                'approved_mutations': Mutation.query.filter_by(status='approved').count(),
                'total_users': User.query.count(),
                'citizen_users': User.query.filter_by(role='citizen').count(),
                'total_revenue': float(db.session.query(func.sum(Payment.amount)).filter(
                    Payment.status == 'completed'
                ).scalar() or 0),
                'monthly_revenue': 0,
                'pending_payments': 0,
                'total_property_value': 0,
                'avg_property_value': 0
            }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/analytics/property-trends')
@login_required
@admin_required
def property_trends():
    """API endpoint for property registration trends."""
    try:
        # Get property counts by month for the last 12 months
        from sqlalchemy import extract, func
        from datetime import datetime, timedelta
        
        twelve_months_ago = datetime.now() - timedelta(days=365)
        
        results = db.session.query(
            func.date_format(Property.created_at, '%Y-%m').label('month'),
            func.count(Property.id).label('count')
        ).filter(
            Property.created_at >= twelve_months_ago
        ).group_by(
            func.date_format(Property.created_at, '%Y-%m')
        ).order_by('month').all()
        
        data = {
            'labels': [r[0] for r in results],
            'values': [r[1] for r in results]
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/analytics/property-status')
@login_required
@admin_required
def property_status_distribution():
    """API endpoint for property status distribution."""
    try:
        results = db.session.query(
            Property.status,
            func.count(Property.id)
        ).group_by(Property.status).all()
        
        data = {
            'labels': [r[0] for r in results],
            'values': [r[1] for r in results]
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/analytics/revenue-trends')
@login_required
@admin_required
def revenue_trends():
    """API endpoint for revenue trends."""
    try:
        # Query revenue analytics view or calculate directly
        try:
            results = db.session.execute(
                """SELECT payment_month, SUM(completed_amount) as revenue
                   FROM vw_revenue_analytics
                   GROUP BY payment_month
                   ORDER BY payment_month DESC
                   LIMIT 12"""
            ).fetchall()
            
            data = {
                'labels': [r[0] for r in reversed(results)],
                'values': [float(r[1]) if r[1] else 0 for r in reversed(results)]
            }
        except:
            # Fallback to direct query
            from datetime import datetime, timedelta
            twelve_months_ago = datetime.now() - timedelta(days=365)
            
            results = db.session.query(
                func.date_format(Payment.payment_date, '%Y-%m').label('month'),
                func.sum(Payment.amount).label('revenue')
            ).filter(
                Payment.payment_date >= twelve_months_ago,
                Payment.status == 'completed'
            ).group_by(
                func.date_format(Payment.payment_date, '%Y-%m')
            ).order_by('month').all()
            
            data = {
                'labels': [r[0] for r in results],
                'values': [float(r[1]) if r[1] else 0 for r in results]
            }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/analytics/property-types')
@login_required
@admin_required
def property_type_distribution():
    """API endpoint for property type distribution."""
    try:
        results = db.session.query(
            Property.property_type,
            func.count(Property.id)
        ).group_by(Property.property_type).all()
        
        data = {
            'labels': [r[0] if r[0] else 'Unknown' for r in results],
            'values': [r[1] for r in results]
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/analytics/geographic-distribution')
@login_required
@admin_required
def geographic_distribution():
    """API endpoint for geographic distribution of properties."""
    try:
        # Try to query the view first
        try:
            results = db.session.execute(
                """SELECT district, property_count
                   FROM vw_geographic_distribution
                   ORDER BY property_count DESC
                   LIMIT 10"""
            ).fetchall()
            
            data = {
                'labels': [r[0] for r in results],
                'values': [r[1] for r in results]
            }
        except:
            # Fallback to direct query
            results = db.session.query(
                Property.district,
                func.count(Property.id)
            ).group_by(Property.district).order_by(
                func.count(Property.id).desc()
            ).limit(10).all()
            
            data = {
                'labels': [r[0] if r[0] else 'Unknown' for r in results],
                'values': [r[1] for r in results]
            }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/analytics/user-activity')
@login_required
@admin_required
def user_activity():
    """API endpoint for user activity statistics."""
    try:
        results = db.session.query(
            User.role,
            func.count(User.id)
        ).group_by(User.role).all()
        
        data = {
            'labels': [r[0] for r in results],
            'values': [r[1] for r in results]
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/revenue')
@login_required
@admin_required
def revenue():
    """Comprehensive revenue report and analytics."""
    from datetime import datetime, timedelta
    
    # Date filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default to current year if no filters
    if not start_date:
        start_date = datetime(datetime.now().year, 1, 1)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    if not end_date:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Total revenue (completed payments)
    total_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.status == 'completed',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).scalar() or 0
    
    # Pending revenue
    pending_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.status == 'pending',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).scalar() or 0
    
    # Failed revenue
    failed_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.status == 'failed',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).scalar() or 0
    
    # Revenue by payment type
    revenue_by_type = db.session.query(
        Payment.payment_type,
        func.sum(Payment.amount).label('total'),
        func.count(Payment.id).label('count')
    ).filter(
        Payment.status == 'completed',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).group_by(Payment.payment_type).all()
    
    # Revenue by payment method
    revenue_by_method = db.session.query(
        Payment.payment_method,
        func.sum(Payment.amount).label('total'),
        func.count(Payment.id).label('count')
    ).filter(
        Payment.status == 'completed',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).group_by(Payment.payment_method).all()
    
    # Monthly revenue trend (last 12 months)
    twelve_months_ago = datetime.now() - timedelta(days=365)
    monthly_revenue = db.session.query(
        func.date_format(Payment.payment_date, '%Y-%m').label('month'),
        func.sum(Payment.amount).label('revenue'),
        func.count(Payment.id).label('count')
    ).filter(
        Payment.status == 'completed',
        Payment.payment_date >= twelve_months_ago
    ).group_by(
        func.date_format(Payment.payment_date, '%Y-%m')
    ).order_by('month').all()
    
    # Daily revenue (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    daily_revenue = db.session.query(
        func.date(Payment.payment_date).label('day'),
        func.sum(Payment.amount).label('revenue'),
        func.count(Payment.id).label('count')
    ).filter(
        Payment.status == 'completed',
        Payment.payment_date >= thirty_days_ago
    ).group_by(
        func.date(Payment.payment_date)
    ).order_by('day').all()
    
    # Top revenue-generating properties
    top_properties = db.session.query(
        Property.ulpin,
        Property.district,
        Property.locality,
        func.sum(Payment.amount).label('total_revenue'),
        func.count(Payment.id).label('payment_count')
    ).join(
        Payment, Property.id == Payment.property_id
    ).filter(
        Payment.status == 'completed',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).group_by(
        Property.id, Property.ulpin, Property.district, Property.locality
    ).order_by(
        func.sum(Payment.amount).desc()
    ).limit(10).all()
    
    # All revenue-generating properties (for detailed view)
    all_properties = db.session.query(
        Property.ulpin,
        Property.district,
        Property.locality,
        Property.property_type,
        func.sum(Payment.amount).label('total_revenue'),
        func.count(Payment.id).label('payment_count')
    ).join(
        Payment, Property.id == Payment.property_id
    ).filter(
        Payment.status == 'completed',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).group_by(
        Property.id, Property.ulpin, Property.district, Property.locality, Property.property_type
    ).order_by(
        func.sum(Payment.amount).desc()
    ).all()
    
    # Total properties count
    total_properties_count = len(all_properties)
    
    # Revenue by district
    revenue_by_district = db.session.query(
        Property.district,
        func.sum(Payment.amount).label('total'),
        func.count(Payment.id).label('count')
    ).join(
        Payment, Property.id == Payment.property_id
    ).filter(
        Payment.status == 'completed',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).group_by(Property.district).order_by(
        func.sum(Payment.amount).desc()
    ).all()
    
    # Average transaction value
    avg_transaction = db.session.query(func.avg(Payment.amount)).filter(
        Payment.status == 'completed',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).scalar() or 0
    
    # Total transactions
    total_transactions = Payment.query.filter(
        Payment.status == 'completed',
        Payment.payment_date >= start_date,
        Payment.payment_date <= end_date
    ).count()
    
    # Recent large transactions
    recent_large_transactions = Payment.query.filter(
        Payment.status == 'completed',
        Payment.amount >= 10000
    ).order_by(Payment.payment_date.desc()).limit(10).all()
    
    # Calculate growth rate (compare with previous period)
    period_days = (end_date - start_date).days
    previous_start = start_date - timedelta(days=period_days)
    previous_end = start_date
    
    previous_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.status == 'completed',
        Payment.payment_date >= previous_start,
        Payment.payment_date < previous_end
    ).scalar() or 0
    
    if previous_revenue > 0:
        growth_rate = ((total_revenue - previous_revenue) / previous_revenue) * 100
    else:
        growth_rate = 100 if total_revenue > 0 else 0
    
    return render_template('admin/revenue.html',
                         total_revenue=total_revenue,
                         pending_revenue=pending_revenue,
                         failed_revenue=failed_revenue,
                         revenue_by_type=revenue_by_type,
                         revenue_by_method=revenue_by_method,
                         monthly_revenue=monthly_revenue,
                         daily_revenue=daily_revenue,
                         top_properties=top_properties,
                         all_properties=all_properties,
                         total_properties_count=total_properties_count,
                         revenue_by_district=revenue_by_district,
                         avg_transaction=avg_transaction,
                         total_transactions=total_transactions,
                         recent_large_transactions=recent_large_transactions,
                         growth_rate=growth_rate,
                         previous_period_revenue=previous_revenue,
                         start_date=start_date,
                         end_date=end_date)


@bp.route('/settings')
@login_required
@admin_required
def settings():
    """System settings page."""
    return render_template('admin/settings.html')
