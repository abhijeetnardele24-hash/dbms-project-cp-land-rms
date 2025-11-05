"""
Advanced API Endpoints for Land Registry Management System
Includes bulk operations, advanced search, and comprehensive REST API
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, and_, func
from datetime import datetime, timedelta
from app.models import db
from app.models.user import User
from app.models.property import Property
from app.models.mutation import Mutation
from app.models.payment import Payment
from app.models.owner import Owner
from app.models.ownership import Ownership
from app.utils.decorators import admin_required, api_key_required

bp = Blueprint('api_advanced', __name__, url_prefix='/api/v1')

# =====================================================
# BULK OPERATIONS
# =====================================================

@bp.route('/properties/bulk-import', methods=['POST'])
@login_required
@admin_required
def bulk_import_properties():
    """
    Bulk import properties from JSON array
    
    Expected format:
    {
        "properties": [
            {"ulpin": "...", "village_city": "...", ...},
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        properties_data = data.get('properties', [])
        
        if not properties_data:
            return jsonify({'error': 'No properties provided'}), 400
        
        imported = 0
        errors = []
        
        for idx, prop_data in enumerate(properties_data):
            try:
                property = Property(**prop_data)
                db.session.add(property)
                imported += 1
            except Exception as e:
                errors.append(f"Property {idx}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'imported': imported,
            'total': len(properties_data),
            'errors': errors
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/properties/bulk-update', methods=['PUT'])
@login_required
@admin_required
def bulk_update_properties():
    """
    Bulk update properties
    
    Expected format:
    {
        "updates": [
            {"id": 1, "status": "approved"},
            {"id": 2, "market_value": 5000000}
        ]
    }
    """
    try:
        data = request.get_json()
        updates = data.get('updates', [])
        
        updated = 0
        errors = []
        
        for update_data in updates:
            property_id = update_data.pop('id', None)
            if not property_id:
                errors.append("Missing property ID")
                continue
                
            property = Property.query.get(property_id)
            if not property:
                errors.append(f"Property {property_id} not found")
                continue
            
            for key, value in update_data.items():
                if hasattr(property, key):
                    setattr(property, key, value)
            
            updated += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'updated': updated,
            'errors': errors
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/properties/bulk-delete', methods=['DELETE'])
@login_required
@admin_required
def bulk_delete_properties():
    """
    Bulk delete properties
    
    Expected format:
    {
        "property_ids": [1, 2, 3, 4, 5]
    }
    """
    try:
        data = request.get_json()
        property_ids = data.get('property_ids', [])
        
        if not property_ids:
            return jsonify({'error': 'No property IDs provided'}), 400
        
        deleted = Property.query.filter(Property.id.in_(property_ids)).delete(synchronize_session=False)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'deleted': deleted
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# =====================================================
# ADVANCED SEARCH & FILTERING
# =====================================================

@bp.route('/search/properties', methods=['POST'])
@login_required
def advanced_property_search():
    """
    Advanced property search with multiple filters
    
    POST body:
    {
        "query": "search text",
        "filters": {
            "status": "approved",
            "property_type": "residential",
            "min_value": 100000,
            "max_value": 5000000,
            "state": "Maharashtra",
            "district": "Pune"
        },
        "sort": "market_value",
        "order": "desc",
        "page": 1,
        "per_page": 20
    }
    """
    try:
        data = request.get_json()
        
        # Base query
        query = Property.query
        
        # Text search
        search_text = data.get('query', '')
        if search_text:
            search_filter = or_(
                Property.ulpin.contains(search_text),
                Property.village_city.contains(search_text),
                Property.district.contains(search_text),
                Property.description.contains(search_text)
            )
            query = query.filter(search_filter)
        
        # Apply filters
        filters = data.get('filters', {})
        
        if filters.get('status'):
            query = query.filter(Property.status == filters['status'])
        
        if filters.get('property_type'):
            query = query.filter(Property.property_type == filters['property_type'])
        
        if filters.get('min_value'):
            query = query.filter(Property.market_value >= filters['min_value'])
        
        if filters.get('max_value'):
            query = query.filter(Property.market_value <= filters['max_value'])
        
        if filters.get('state'):
            query = query.filter(Property.state == filters['state'])
        
        if filters.get('district'):
            query = query.filter(Property.district == filters['district'])
        
        if filters.get('min_area'):
            query = query.filter(Property.area >= filters['min_area'])
        
        if filters.get('max_area'):
            query = query.filter(Property.area <= filters['max_area'])
        
        # Sorting
        sort_field = data.get('sort', 'created_at')
        sort_order = data.get('order', 'desc')
        
        if hasattr(Property, sort_field):
            order_by = getattr(Property, sort_field)
            if sort_order == 'desc':
                order_by = order_by.desc()
            query = query.order_by(order_by)
        
        # Pagination
        page = data.get('page', 1)
        per_page = min(data.get('per_page', 20), 100)  # Max 100 per page
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': [prop.to_dict() if hasattr(prop, 'to_dict') else {
                'id': prop.id,
                'ulpin': prop.ulpin,
                'village_city': prop.village_city,
                'district': prop.district,
                'state': prop.state,
                'property_type': prop.property_type,
                'market_value': float(prop.market_value) if prop.market_value else None,
                'status': prop.status
            } for prop in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/search/autocomplete', methods=['GET'])
@login_required
def autocomplete_search():
    """
    Autocomplete search for properties
    
    Query params:
    - q: search query
    - field: field to search (ulpin, village_city, district)
    - limit: max results (default 10)
    """
    try:
        search_query = request.args.get('q', '')
        field = request.args.get('field', 'village_city')
        limit = min(int(request.args.get('limit', 10)), 50)
        
        if not search_query or len(search_query) < 2:
            return jsonify({'suggestions': []}), 200
        
        # Build query based on field
        if field == 'ulpin' and hasattr(Property, 'ulpin'):
            results = Property.query.filter(
                Property.ulpin.contains(search_query)
            ).limit(limit).all()
            suggestions = [p.ulpin for p in results if p.ulpin]
            
        elif field == 'village_city':
            results = db.session.query(Property.village_city).filter(
                Property.village_city.contains(search_query)
            ).distinct().limit(limit).all()
            suggestions = [r[0] for r in results if r[0]]
            
        elif field == 'district':
            results = db.session.query(Property.district).filter(
                Property.district.contains(search_query)
            ).distinct().limit(limit).all()
            suggestions = [r[0] for r in results if r[0]]
        else:
            suggestions = []
        
        return jsonify({'suggestions': suggestions}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =====================================================
# DATA EXPORT
# =====================================================

@bp.route('/export/properties', methods=['GET'])
@login_required
@admin_required
def export_properties():
    """
    Export properties to CSV/JSON
    
    Query params:
    - format: csv or json
    - status: filter by status
    - district: filter by district
    """
    try:
        export_format = request.args.get('format', 'json')
        
        # Build query with filters
        query = Property.query
        
        if request.args.get('status'):
            query = query.filter(Property.status == request.args.get('status'))
        
        if request.args.get('district'):
            query = query.filter(Property.district == request.args.get('district'))
        
        properties = query.all()
        
        if export_format == 'csv':
            # Generate CSV
            import csv
            from io import StringIO
            
            output = StringIO()
            writer = csv.writer(output)
            
            # Header
            writer.writerow(['ID', 'ULPIN', 'Village', 'District', 'State', 'Type', 'Area', 'Value', 'Status'])
            
            # Data
            for prop in properties:
                writer.writerow([
                    prop.id,
                    prop.ulpin,
                    prop.village_city,
                    prop.district,
                    prop.state,
                    prop.property_type,
                    prop.area,
                    prop.market_value,
                    prop.status
                ])
            
            return output.getvalue(), 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename=properties_{datetime.now().strftime("%Y%m%d")}.csv'
            }
        else:
            # JSON export
            data = [{
                'id': p.id,
                'ulpin': p.ulpin,
                'village_city': p.village_city,
                'district': p.district,
                'state': p.state,
                'property_type': p.property_type,
                'area': float(p.area) if p.area else None,
                'market_value': float(p.market_value) if p.market_value else None,
                'status': p.status
            } for p in properties]
            
            return jsonify({
                'success': True,
                'count': len(data),
                'data': data
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =====================================================
# STATISTICS & AGGREGATIONS
# =====================================================

@bp.route('/stats/summary', methods=['GET'])
@login_required
def get_statistics_summary():
    """
    Get comprehensive statistics summary
    """
    try:
        stats = {
            'properties': {
                'total': Property.query.count(),
                'approved': Property.query.filter_by(status='approved').count(),
                'pending': Property.query.filter_by(status='pending').count(),
                'rejected': Property.query.filter_by(status='rejected').count()
            },
            'mutations': {
                'total': Mutation.query.count(),
                'pending': Mutation.query.filter_by(status='pending').count(),
                'approved': Mutation.query.filter_by(status='approved').count()
            },
            'payments': {
                'total': Payment.query.count(),
                'completed': Payment.query.filter_by(status='completed').count(),
                'total_amount': float(db.session.query(func.sum(Payment.amount)).filter(
                    Payment.status == 'completed'
                ).scalar() or 0)
            },
            'users': {
                'total': User.query.count(),
                'by_role': {
                    role: User.query.filter_by(role=role).count()
                    for role in ['admin', 'registrar', 'officer', 'citizen']
                }
            }
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =====================================================
# API DOCUMENTATION ENDPOINT
# =====================================================

@bp.route('/docs', methods=['GET'])
def api_documentation():
    """
    API Documentation in OpenAPI/Swagger format
    """
    docs = {
        'openapi': '3.0.0',
        'info': {
            'title': 'Land Registry Management System API',
            'version': '1.0.0',
            'description': 'Comprehensive REST API for property management'
        },
        'servers': [
            {'url': '/api/v1', 'description': 'API v1'}
        ],
        'paths': {
            '/properties/bulk-import': {
                'post': {
                    'summary': 'Bulk import properties',
                    'tags': ['Bulk Operations'],
                    'security': [{'bearerAuth': []}],
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'properties': {
                                            'type': 'array',
                                            'items': {'type': 'object'}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': {'description': 'Success'},
                        '400': {'description': 'Bad Request'},
                        '500': {'description': 'Server Error'}
                    }
                }
            },
            '/search/properties': {
                'post': {
                    'summary': 'Advanced property search',
                    'tags': ['Search'],
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'query': {'type': 'string'},
                                        'filters': {'type': 'object'},
                                        'page': {'type': 'integer'},
                                        'per_page': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '/export/properties': {
                'get': {
                    'summary': 'Export properties to CSV/JSON',
                    'tags': ['Export'],
                    'parameters': [
                        {'name': 'format', 'in': 'query', 'schema': {'type': 'string', 'enum': ['csv', 'json']}},
                        {'name': 'status', 'in': 'query', 'schema': {'type': 'string'}},
                        {'name': 'district', 'in': 'query', 'schema': {'type': 'string'}}
                    ]
                }
            },
            '/stats/summary': {
                'get': {
                    'summary': 'Get comprehensive statistics',
                    'tags': ['Statistics']
                }
            }
        }
    }
    
    return jsonify(docs), 200


# Error handlers
@bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500
