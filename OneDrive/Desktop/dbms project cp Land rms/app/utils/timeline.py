"""
Timeline utility functions for generating activity timelines.
"""

from datetime import datetime


def generate_property_timeline(property_obj):
    """
    Generate timeline for a property showing all changes and events.
    
    Args:
        property_obj: Property model instance
        
    Returns:
        list: Timeline items sorted by timestamp (newest first)
    """
    timeline = []
    
    # Property creation
    timeline.append({
        'title': 'Property Registered',
        'description': f'Property registered with ULPIN {property_obj.ulpin}',
        'timestamp': property_obj.created_at,
        'type': 'success',
        'icon': 'fa-home',
        'metadata': {
            'Type': property_obj.property_type.replace('_', ' ').title(),
            'Area': f"{property_obj.area_sqft} sq ft",
            'Location': f"{property_obj.district}"
        }
    })
    
    # Mutations
    from app.models.mutation import Mutation
    mutations = Mutation.query.filter_by(property_id=property_obj.id).order_by(Mutation.created_at.desc()).all()
    
    for mutation in mutations:
        icon_map = {
            'approved': ('fa-check-circle', 'success'),
            'rejected': ('fa-times-circle', 'danger'),
            'pending': ('fa-clock', 'warning'),
            'under_review': ('fa-search', 'info')
        }
        icon, type_class = icon_map.get(mutation.status, ('fa-circle', 'info'))
        
        timeline.append({
            'title': f'Mutation {mutation.status.replace("_", " ").title()}',
            'description': f'{mutation.mutation_type.replace("_", " ").title()} mutation {mutation.status}',
            'timestamp': mutation.approval_date or mutation.created_at,
            'type': type_class,
            'icon': icon,
            'metadata': {
                'Mutation #': mutation.mutation_number or 'N/A',
                'Type': mutation.mutation_type.replace('_', ' ').title(),
                'From': mutation.previous_owners or 'N/A',
                'To': mutation.new_owners or 'N/A'
            }
        })
    
    # Payments
    from app.models.payment import Payment
    payments = Payment.query.filter_by(property_id=property_obj.id).order_by(Payment.created_at.desc()).limit(10).all()
    
    for payment in payments:
        type_class = 'success' if payment.status == 'success' else 'warning' if payment.status == 'pending' else 'danger'
        
        timeline.append({
            'title': f'Payment {payment.status.title()}',
            'description': f'{payment.payment_type.replace("_", " ").title()} - ₹{payment.amount:,.2f}',
            'timestamp': payment.created_at,
            'type': type_class,
            'icon': 'fa-rupee-sign',
            'metadata': {
                'Transaction': payment.transaction_id,
                'Amount': f'₹{payment.amount:,.2f}',
                'Status': payment.status.title()
            }
        })
    
    # Sort by timestamp (newest first)
    timeline.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return timeline


def generate_mutation_timeline(mutation):
    """
    Generate timeline for a mutation showing workflow progress.
    
    Args:
        mutation: Mutation model instance
        
    Returns:
        list: Timeline items sorted by timestamp
    """
    timeline = []
    
    # Application submitted
    timeline.append({
        'title': 'Application Submitted',
        'description': f'{mutation.mutation_type.replace("_", " ").title()} mutation request submitted',
        'timestamp': mutation.created_at,
        'type': 'info',
        'icon': 'fa-file-alt',
        'metadata': {
            'Mutation #': mutation.mutation_number or 'N/A',
            'Requester': mutation.requester.full_name,
            'Property': mutation.property.ulpin
        }
    })
    
    # Under review
    if mutation.status in ['under_review', 'documents_verified', 'approved', 'rejected']:
        timeline.append({
            'title': 'Under Review',
            'description': 'Application is being reviewed by officer',
            'timestamp': mutation.processing_date or mutation.created_at,
            'type': 'warning',
            'icon': 'fa-search',
            'metadata': {}
        })
    
    # Documents verified
    if mutation.status in ['documents_verified', 'approved']:
        timeline.append({
            'title': 'Documents Verified',
            'description': 'All submitted documents have been verified',
            'timestamp': mutation.processing_date or mutation.created_at,
            'type': 'info',
            'icon': 'fa-check-double',
            'metadata': {}
        })
    
    # Approved/Rejected
    if mutation.status == 'approved':
        timeline.append({
            'title': 'Application Approved',
            'description': 'Mutation approved and certificate issued',
            'timestamp': mutation.approval_date or datetime.now(),
            'type': 'success',
            'icon': 'fa-check-circle',
            'metadata': {
                'Certificate #': mutation.mutation_certificate_number or 'Pending',
                'Processed By': mutation.processed_by_user.full_name if mutation.processed_by_user else 'N/A'
            }
        })
    elif mutation.status == 'rejected':
        timeline.append({
            'title': 'Application Rejected',
            'description': mutation.rejection_reason or 'Application was rejected',
            'timestamp': mutation.rejection_date or datetime.now(),
            'type': 'danger',
            'icon': 'fa-times-circle',
            'metadata': {
                'Rejected By': mutation.processed_by_user.full_name if mutation.processed_by_user else 'N/A'
            }
        })
    
    # Sort by timestamp
    timeline.sort(key=lambda x: x['timestamp'])
    
    return timeline


def generate_user_activity_timeline(user, limit=20):
    """
    Generate activity timeline for a user showing their actions.
    
    Args:
        user: User model instance
        limit: Maximum number of items to return
        
    Returns:
        list: Timeline items sorted by timestamp (newest first)
    """
    timeline = []
    
    # Account created
    timeline.append({
        'title': 'Account Created',
        'description': f'{user.role.title()} account created',
        'timestamp': user.created_at,
        'type': 'success',
        'icon': 'fa-user-plus',
        'metadata': {
            'Email': user.email,
            'Role': user.role.title()
        }
    })
    
    # Recent mutations requested
    from app.models.mutation import Mutation
    mutations = Mutation.query.filter_by(requester_id=user.id).order_by(Mutation.created_at.desc()).limit(5).all()
    
    for mutation in mutations:
        timeline.append({
            'title': 'Mutation Requested',
            'description': f'{mutation.mutation_type.replace("_", " ").title()} for {mutation.property.ulpin}',
            'timestamp': mutation.created_at,
            'type': 'info',
            'icon': 'fa-exchange-alt',
            'metadata': {
                'Mutation #': mutation.mutation_number or 'N/A',
                'Status': mutation.status.replace('_', ' ').title()
            }
        })
    
    # Recent payments
    from app.models.payment import Payment
    payments = Payment.query.filter_by(user_id=user.id).order_by(Payment.created_at.desc()).limit(5).all()
    
    for payment in payments:
        timeline.append({
            'title': 'Payment Made',
            'description': f'{payment.payment_type.replace("_", " ").title()} - ₹{payment.amount:,.2f}',
            'timestamp': payment.created_at,
            'type': 'success' if payment.status == 'success' else 'warning',
            'icon': 'fa-rupee-sign',
            'metadata': {
                'Amount': f'₹{payment.amount:,.2f}',
                'Status': payment.status.title()
            }
        })
    
    # Last login
    if user.last_login:
        timeline.append({
            'title': 'Last Login',
            'description': 'User logged into the system',
            'timestamp': user.last_login,
            'type': 'info',
            'icon': 'fa-sign-in-alt',
            'metadata': {}
        })
    
    # Sort by timestamp (newest first) and limit
    timeline.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return timeline[:limit]
