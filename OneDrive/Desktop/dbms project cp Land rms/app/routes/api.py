"""
API routes for RESTful endpoints.
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.property import Property
from app.models.mutation import Mutation
from app.models.payment import Payment

bp = Blueprint('api', __name__)


@bp.route('/properties', methods=['GET'])
@login_required
def get_properties():
    """Get list of properties."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    properties = Property.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'properties': [p.to_dict() for p in properties.items],
        'total': properties.total,
        'pages': properties.pages,
        'current_page': page
    })


@bp.route('/properties/<int:property_id>', methods=['GET'])
@login_required
def get_property(property_id):
    """Get specific property details."""
    property_obj = Property.query.get_or_404(property_id)
    return jsonify(property_obj.to_dict())


@bp.route('/mutations', methods=['GET'])
@login_required
def get_mutations():
    """Get list of mutations."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    mutations = Mutation.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'mutations': [m.to_dict() for m in mutations.items],
        'total': mutations.total,
        'pages': mutations.pages,
        'current_page': page
    })


@bp.route('/payments', methods=['GET'])
@login_required
def get_payments():
    """Get list of payments."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    payments = Payment.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'payments': [p.to_dict() for p in payments.items],
        'total': payments.total,
        'pages': payments.pages,
        'current_page': page
    })


@bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get system statistics."""
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    stats = {
        'total_users': User.query.count(),
        'total_properties': Property.query.count(),
        'total_mutations': Mutation.query.count(),
        'total_payments': Payment.query.count(),
        'pending_registrations': Property.query.filter_by(status='pending').count(),
        'pending_mutations': Mutation.query.filter_by(status='pending').count()
    }
    
    return jsonify(stats)
