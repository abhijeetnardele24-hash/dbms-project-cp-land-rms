"""
Public routes for certificate and property verification (no login required).
"""
from flask import Blueprint, render_template, abort, request
from app.models.mutation import Mutation
from app.models.property import Property
from app.models.payment import Payment
from app.utils.qr_code_generator import generate_certificate_qr, generate_property_qr

bp = Blueprint('public', __name__, url_prefix='/verify')


@bp.route('/<certificate_number>')
def verify_certificate(certificate_number):
    """Public certificate verification page."""
    mutation = Mutation.query.filter_by(
        mutation_certificate_number=certificate_number
    ).first()
    
    # Generate QR code for verification URL
    verification_url = request.url_root.rstrip('/') + '/verify/' + certificate_number
    qr_code = generate_certificate_qr(certificate_number, mutation.id if mutation else None)
    
    return render_template('public/verify_certificate.html', 
                         mutation=mutation,
                         certificate_number=certificate_number,
                         qr_code=qr_code)


@bp.route('/property/<ulpin>')
def verify_property(ulpin):
    """Public property verification page."""
    property_obj = Property.query.filter_by(ulpin=ulpin).first()
    
    # Generate QR code even if property not found (for error page)
    qr_code = generate_property_qr(ulpin)
    
    mutations = None
    payments = None
    
    if property_obj:
        # Get mutation history for this property (ordered by date)
        mutations = Mutation.query.filter_by(
            property_id=property_obj.id
        ).order_by(Mutation.created_at.desc()).all()
        
        # Get payment history for this property
        payments = Payment.query.filter_by(
            property_id=property_obj.id,
            status='success'
        ).order_by(Payment.created_at.desc()).limit(10).all()
    
    return render_template('public/verify_property.html',
                         property=property_obj,
                         ulpin=ulpin,
                         mutations=mutations,
                         payments=payments,
                         qr_code=qr_code)
