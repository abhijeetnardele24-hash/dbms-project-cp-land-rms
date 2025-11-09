"""
Advanced search routes with multi-field filtering and autocomplete.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from app.models.property import Property
from app.models.mutation import Mutation
from app.models.user import User
from app.models.payment import Payment
from datetime import datetime

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route('/')
@login_required
def index():
    """Advanced search page."""
    return render_template('search/index.html')


@bp.route('/properties')
@login_required
def search_properties():
    """
    Search properties with multiple filters.
    Query params: q, district, property_type, min_area, max_area, min_value, max_value
    """
    query = request.args.get('q', '').strip()
    district = request.args.get('district', '').strip()
    property_type = request.args.get('property_type', '').strip()
    min_area = request.args.get('min_area', type=int)
    max_area = request.args.get('max_area', type=int)
    min_value = request.args.get('min_value', type=float)
    max_value = request.args.get('max_value', type=float)
    
    # Base query
    properties = Property.query
    
    # Text search across multiple fields
    if query:
        search_filter = or_(
            Property.ulpin.like(f'%{query}%'),
            Property.locality.like(f'%{query}%'),
            Property.district.like(f'%{query}%'),
            Property.pincode.like(f'%{query}%')
        )
        properties = properties.filter(search_filter)
    
    # Filter by district
    if district:
        properties = properties.filter(Property.district == district)
    
    # Filter by property type
    if property_type:
        properties = properties.filter(Property.property_type == property_type)
    
    # Filter by area range
    if min_area:
        properties = properties.filter(Property.area_sqft >= min_area)
    if max_area:
        properties = properties.filter(Property.area_sqft <= max_area)
    
    # Filter by value range
    if min_value:
        properties = properties.filter(Property.market_value >= min_value)
    if max_value:
        properties = properties.filter(Property.market_value <= max_value)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    properties = properties.paginate(page=page, per_page=per_page, error_out=False)
    
    # For AJAX requests, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'results': [{
                'id': p.id,
                'ulpin': p.ulpin,
                'district': p.district,
                'locality': p.locality,
                'property_type': p.property_type,
                'area_sqft': p.area_sqft,
                'market_value': float(p.market_value),
                'owner': p.owner.full_name if p.owner else 'N/A'
            } for p in properties.items],
            'total': properties.total,
            'pages': properties.pages,
            'current_page': properties.page
        })
    
    return render_template('search/properties.html', 
                         properties=properties,
                         query=query,
                         filters={'district': district, 'property_type': property_type})


@bp.route('/mutations')
@login_required
def search_mutations():
    """
    Search mutations with multiple filters.
    Query params: q, status, mutation_type, date_from, date_to
    """
    query = request.args.get('q', '').strip()
    status = request.args.get('status', '').strip()
    mutation_type = request.args.get('mutation_type', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    
    # Base query
    mutations = Mutation.query
    
    # Text search
    if query:
        search_filter = or_(
            Mutation.mutation_number.like(f'%{query}%'),
            Mutation.mutation_certificate_number.like(f'%{query}%')
        )
        mutations = mutations.filter(search_filter)
    
    # Filter by status
    if status:
        mutations = mutations.filter(Mutation.status == status)
    
    # Filter by mutation type
    if mutation_type:
        mutations = mutations.filter(Mutation.mutation_type == mutation_type)
    
    # Filter by date range
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            mutations = mutations.filter(Mutation.created_at >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            mutations = mutations.filter(Mutation.created_at <= date_to_obj)
        except ValueError:
            pass
    
    # Order by date
    mutations = mutations.order_by(Mutation.created_at.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    mutations = mutations.paginate(page=page, per_page=per_page, error_out=False)
    
    # For AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'results': [{
                'id': m.id,
                'mutation_number': m.mutation_number,
                'certificate_number': m.mutation_certificate_number,
                'mutation_type': m.mutation_type,
                'status': m.status,
                'property_ulpin': m.property.ulpin,
                'created_at': m.created_at.strftime('%Y-%m-%d')
            } for m in mutations.items],
            'total': mutations.total,
            'pages': mutations.pages,
            'current_page': mutations.page
        })
    
    return render_template('search/mutations.html', 
                         mutations=mutations,
                         query=query,
                         filters={'status': status, 'mutation_type': mutation_type})


@bp.route('/users')
@login_required
def search_users():
    """
    Search users with multiple filters.
    Query params: q, role, is_active
    """
    # Only admin can search users
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    query = request.args.get('q', '').strip()
    role = request.args.get('role', '').strip()
    is_active = request.args.get('is_active', '').strip()
    
    # Base query
    users = User.query
    
    # Text search
    if query:
        search_filter = or_(
            User.full_name.like(f'%{query}%'),
            User.email.like(f'%{query}%'),
            User.phone.like(f'%{query}%')
        )
        users = users.filter(search_filter)
    
    # Filter by role
    if role:
        users = users.filter(User.role == role)
    
    # Filter by active status
    if is_active == 'true':
        users = users.filter(User.is_active == True)
    elif is_active == 'false':
        users = users.filter(User.is_active == False)
    
    # Order by name
    users = users.order_by(User.full_name)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    users = users.paginate(page=page, per_page=per_page, error_out=False)
    
    # For AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'results': [{
                'id': u.id,
                'full_name': u.full_name,
                'email': u.email,
                'phone': u.phone,
                'role': u.role,
                'is_active': u.is_active
            } for u in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': users.page
        })
    
    return render_template('search/users.html', 
                         users=users,
                         query=query,
                         filters={'role': role, 'is_active': is_active})


@bp.route('/autocomplete/properties')
@login_required
def autocomplete_properties():
    """Autocomplete endpoint for property search."""
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify([])
    
    properties = Property.query.filter(
        or_(
            Property.ulpin.like(f'%{query}%'),
            Property.locality.like(f'%{query}%'),
            Property.district.like(f'%{query}%')
        )
    ).limit(10).all()
    
    return jsonify([{
        'id': p.id,
        'ulpin': p.ulpin,
        'label': f"{p.ulpin} - {p.locality}, {p.district}",
        'value': p.ulpin
    } for p in properties])


@bp.route('/autocomplete/districts')
@login_required
def autocomplete_districts():
    """Get unique districts for autocomplete."""
    from sqlalchemy import func
    
    districts = Property.query.with_entities(Property.district).distinct().all()
    
    return jsonify([d[0] for d in districts if d[0]])


@bp.route('/autocomplete/localities')
@login_required
def autocomplete_localities():
    """Get unique localities for autocomplete."""
    from sqlalchemy import func
    district = request.args.get('district', '').strip()
    
    query = Property.query.with_entities(Property.locality).distinct()
    
    if district:
        query = query.filter(Property.district == district)
    
    localities = query.all()
    
    return jsonify([l[0] for l in localities if l[0]])
