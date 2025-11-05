"""
Registrar routes for property registration review and approval.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.models import db
from app.models.property import Property
from app.models.mutation import Mutation
from app.models.audit_log import AuditLog
from app.models.user import User
from app.utils.decorators import registrar_required
from app.utils.notification_utils import notify_property_status_change
from app.forms.property_forms import PropertyApprovalForm
from sqlalchemy import func, or_

bp = Blueprint('registrar', __name__)


@bp.route('/dashboard')
@login_required
@registrar_required
def dashboard():
    """Enhanced Registrar dashboard with comprehensive statistics."""
    from app.models.mutation import Mutation
    from app.models.user import User
    from sqlalchemy import func, and_, or_
    
    # Property Statistics
    pending_registrations = Property.query.filter_by(status='pending').count()
    under_review = Property.query.filter_by(status='under_review').count()
    approved_properties = Property.query.filter_by(status='approved').count()
    rejected_properties = Property.query.filter_by(status='rejected').count()
    my_approvals = Property.query.filter_by(approved_by=current_user.id).count()
    total_properties = Property.query.count()
    
    # Mutation Statistics
    pending_mutations = Mutation.query.filter(
        Mutation.status.in_(['pending', 'under_review', 'documents_verified'])
    ).count()
    approved_mutations = Mutation.query.filter_by(status='approved').count()
    rejected_mutations = Mutation.query.filter_by(status='rejected').count()
    
    # Recent Activities - Properties
    recent_properties = Property.query.order_by(Property.created_at.desc()).limit(5).all()
    
    # Recent Activities - Mutations
    recent_mutations = Mutation.query.order_by(Mutation.created_at.desc()).limit(5).all()
    
    # Properties by type
    property_by_type = db.session.query(
        Property.property_type, func.count(Property.id).label('count')
    ).group_by(Property.property_type).all()
    
    # Properties by status
    property_by_status = db.session.query(
        Property.status, func.count(Property.id).label('count')
    ).group_by(Property.status).all()
    
    # Recent approvals by current registrar
    my_recent_approvals = Property.query.filter_by(
        approved_by=current_user.id
    ).order_by(Property.approval_date.desc()).limit(5).all()
    
    # Users statistics
    total_citizens = User.query.filter_by(role='citizen').count()
    total_officers = User.query.filter_by(role='officer').count()
    
    return render_template('registrar/dashboard.html',
                         pending_registrations=pending_registrations,
                         under_review=under_review,
                         approved_properties=approved_properties,
                         rejected_properties=rejected_properties,
                         my_approvals=my_approvals,
                         total_properties=total_properties,
                         pending_mutations=pending_mutations,
                         approved_mutations=approved_mutations,
                         rejected_mutations=rejected_mutations,
                         recent_properties=recent_properties,
                         recent_mutations=recent_mutations,
                         property_by_type=property_by_type,
                         property_by_status=property_by_status,
                         my_recent_approvals=my_recent_approvals,
                         total_citizens=total_citizens,
                         total_officers=total_officers)


@bp.route('/pending-registrations')
@login_required
@registrar_required
def pending_registrations():
    """View pending property registrations."""
    page = request.args.get('page', 1, type=int)
    
    properties_pagination = Property.query.filter(
        Property.status.in_(['pending', 'under_review', 'documents_verified'])
    ).order_by(Property.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('registrar/pending_registrations.html', 
                         properties=properties_pagination,
                         now=datetime.utcnow())


@bp.route('/property/<int:property_id>')
@login_required
@registrar_required
def view_property(property_id):
    """View property details."""
    property_obj = Property.query.get_or_404(property_id)
    form = PropertyApprovalForm()
    
    return render_template('registrar/property_detail.html', 
                         property=property_obj, form=form)


@bp.route('/property/<int:property_id>/process', methods=['POST'])
@login_required
@registrar_required
def process_property(property_id):
    """Approve or reject property registration."""
    property_obj = Property.query.get_or_404(property_id)
    form = PropertyApprovalForm()
    
    if form.validate_on_submit():
        action = form.action.data
        comments = form.comments.data
        
        if action == 'approve':
            property_obj.status = 'approved'
            property_obj.approved_by = current_user.id
            property_obj.approval_date = datetime.utcnow()
            property_obj.registration_date = datetime.utcnow()
            
            # Generate ULPIN if not exists
            if not property_obj.ulpin:
                property_obj.generate_ulpin()
            
            # Log action
            AuditLog.log_action(
                user_id=current_user.id,
                action='approve_property',
                action_type='approve',
                entity_type='property',
                entity_id=property_obj.id,
                description=f'Registrar approved property: {property_obj.ulpin}',
                status='success'
            )
            
            # Notify property owner (get first owner)
            owners = property_obj.get_current_owners()
            if owners and owners[0].user_id:
                notify_property_status_change(property_obj.id, 'approved', owners[0].user_id)
            
            flash('Property registration approved successfully!', 'success')
            
        elif action == 'reject':
            property_obj.status = 'rejected'
            property_obj.rejection_reason = comments
            
            # Log action
            AuditLog.log_action(
                user_id=current_user.id,
                action='reject_property',
                action_type='reject',
                entity_type='property',
                entity_id=property_obj.id,
                description=f'Registrar rejected property registration',
                status='success'
            )
            
            # Notify property owner
            owners = property_obj.get_current_owners()
            if owners and owners[0].user_id:
                notify_property_status_change(property_obj.id, 'rejected', owners[0].user_id)
            
            flash('Property registration rejected.', 'warning')
            
        elif action == 'request_info':
            property_obj.status = 'under_review'
            property_obj.remarks = comments
            
            flash('Additional information requested from applicant.', 'info')
        
        db.session.commit()
        
        return redirect(url_for('registrar.pending_registrations'))
    
    return redirect(url_for('registrar.view_property', property_id=property_id))


@bp.route('/my-approvals')
@login_required
@registrar_required
def my_approvals():
    """View properties approved by current registrar."""
    page = request.args.get('page', 1, type=int)
    
    properties_pagination = Property.query.filter_by(
        approved_by=current_user.id
    ).order_by(Property.approval_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('registrar/my_approvals.html', 
                         properties=properties_pagination)


@bp.route('/search')
@login_required
@registrar_required
def search():
    """Enhanced search with filters."""
    query = request.args.get('q', '')
    status = request.args.get('status', '')
    property_type = request.args.get('property_type', '')
    district = request.args.get('district', '')
    page = request.args.get('page', 1, type=int)
    
    # Build base query
    base_query = Property.query
    
    # Apply text search
    if query:
        search_filter = f'%{query}%'
        base_query = base_query.filter(
            (Property.ulpin.like(search_filter)) |
            (Property.village_city.like(search_filter)) |
            (Property.district.like(search_filter)) |
            (Property.survey_number.like(search_filter))
        )
    
    # Apply filters
    if status:
        base_query = base_query.filter_by(status=status)
    if property_type:
        base_query = base_query.filter_by(property_type=property_type)
    if district:
        base_query = base_query.filter_by(district=district)
    
    properties_pagination = base_query.order_by(
        Property.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    
    # Get unique districts for filter dropdown
    districts = db.session.query(Property.district).distinct().all()
    districts = [d[0] for d in districts if d[0]]
    
    return render_template('registrar/search.html', 
                         properties=properties_pagination, 
                         query=query,
                         status=status,
                         property_type=property_type,
                         district=district,
                         districts=districts)


@bp.route('/all-properties')
@login_required
@registrar_required
def all_properties():
    """Comprehensive properties view for registrar with filters and pagination."""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    property_type = request.args.get('property_type', '')
    district = request.args.get('district', '')

    base_query = Property.query
    if status:
        base_query = base_query.filter_by(status=status)
    if property_type:
        base_query = base_query.filter_by(property_type=property_type)
    if district:
        base_query = base_query.filter_by(district=district)

    properties_pagination = base_query.order_by(Property.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    districts = db.session.query(Property.district).distinct().all()
    districts = [d[0] for d in districts if d[0]]

    return render_template('registrar/all_properties.html',
                           properties=properties_pagination,
                           status=status,
                           property_type=property_type,
                           district=district,
                           districts=districts)


@bp.route('/mutations')
@login_required
@registrar_required
def list_mutations():
    """Registrar view of all mutation requests for oversight."""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    base_query = Mutation.query
    if status:
        base_query = base_query.filter_by(status=status)

    mutations_pagination = base_query.order_by(Mutation.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('registrar/mutations.html',
                           mutations=mutations_pagination,
                           status=status)


@bp.route('/reports/summary')
@login_required
@registrar_required
def reports_summary():
    """Provide JSON summary for charts/analytics on dashboard."""
    total_properties = Property.query.count()
    approved_properties = Property.query.filter_by(status='approved').count()
    pending_properties = Property.query.filter_by(status='pending').count()
    under_review = Property.query.filter_by(status='under_review').count()

    total_mutations = Mutation.query.count()
    approved_mutations = Mutation.query.filter_by(status='approved').count()
    pending_mutations = Mutation.query.filter(
        Mutation.status.in_(['pending', 'under_review', 'documents_verified'])
    ).count()

    return jsonify({
        'properties': {
            'total': total_properties,
            'approved': approved_properties,
            'pending': pending_properties,
            'under_review': under_review,
        },
        'mutations': {
            'total': total_mutations,
            'approved': approved_mutations,
            'pending': pending_mutations,
        }
    })
