"""
Citizen routes for property registration, mutations, and payments.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, date
from app.models import db
from app.models.property import Property
from app.models.owner import Owner
from app.models.ownership import Ownership
from app.models.mutation import Mutation, MutationDocument
from app.models.payment import Payment
from app.models.master_data import LandCategory, UsageType
from app.models.notification import Notification
from app.utils.decorators import citizen_required
from app.utils.file_utils import save_uploaded_file, get_file_size
from app.forms.property_forms import PropertyRegistrationForm
from app.forms.mutation_forms import MutationRequestForm
from app.forms.payment_forms import PaymentForm

bp = Blueprint('citizen', __name__)


@bp.route('/dashboard')
@login_required
@citizen_required
def dashboard():
    """Citizen dashboard with advanced analytics."""
    from sqlalchemy import func, extract
    from datetime import timedelta
    
    # Get user's properties
    owner = Owner.query.filter_by(user_id=current_user.id).first()
    my_properties_count = 0
    approved_properties = 0
    rejected_properties = 0
    
    if owner:
        my_properties_count = owner.ownerships.filter_by(is_active=True).count()
        approved_properties = Property.query.join(Ownership).join(Owner).filter(
            Owner.user_id == current_user.id,
            Property.status == 'approved'
        ).count()
        rejected_properties = Property.query.join(Ownership).join(Owner).filter(
            Owner.user_id == current_user.id,
            Property.status == 'rejected'
        ).count()
    
    # Get pending applications
    pending_properties = Property.query.join(Ownership).join(Owner).filter(
        Owner.user_id == current_user.id,
        Property.status.in_(['pending', 'under_review'])
    ).count()
    
    # Mutation statistics
    pending_mutations = Mutation.query.filter_by(
        requester_id=current_user.id,
        status='pending'
    ).count()
    
    approved_mutations = Mutation.query.filter_by(
        requester_id=current_user.id,
        status='approved'
    ).count()
    
    rejected_mutations = Mutation.query.filter_by(
        requester_id=current_user.id,
        status='rejected'
    ).count()
    
    # Payment statistics
    total_payments = Payment.query.filter_by(user_id=current_user.id).count()
    total_amount_paid = db.session.query(func.sum(Payment.amount)).filter(
        Payment.user_id == current_user.id,
        Payment.status == 'completed'
    ).scalar() or 0
    
    pending_payments = Payment.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).count()
    
    # Last 6 months payment trend
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_payments = db.session.query(
        extract('year', Payment.payment_date).label('year'),
        extract('month', Payment.payment_date).label('month'),
        func.sum(Payment.amount).label('total'),
        func.count(Payment.id).label('count')
    ).filter(
        Payment.user_id == current_user.id,
        Payment.payment_date >= six_months_ago
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    # Property by type breakdown
    if owner:
        property_by_type = db.session.query(
            Property.property_type,
            func.count(Property.id).label('count')
        ).join(Ownership).join(Owner).filter(
            Owner.user_id == current_user.id,
            Ownership.is_active == True
        ).group_by(Property.property_type).all()
    else:
        property_by_type = []
    
    # Recent notifications
    recent_notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Payment history
    recent_payments = Payment.query.filter_by(
        user_id=current_user.id
    ).order_by(Payment.payment_date.desc()).limit(10).all()
    
    return render_template('citizen/dashboard.html',
                         my_properties_count=my_properties_count,
                         approved_properties=approved_properties,
                         rejected_properties=rejected_properties,
                         pending_properties=pending_properties,
                         pending_mutations=pending_mutations,
                         approved_mutations=approved_mutations,
                         rejected_mutations=rejected_mutations,
                         total_payments=total_payments,
                         total_amount_paid=total_amount_paid,
                         pending_payments=pending_payments,
                         monthly_payments=monthly_payments,
                         property_by_type=property_by_type,
                         recent_notifications=recent_notifications,
                         recent_payments=recent_payments,
                         current_date=datetime.now())




@bp.route('/my-properties')
@login_required
@citizen_required
def my_properties():
    """View user's properties."""
    page = request.args.get('page', 1, type=int)
    
    owner = Owner.query.filter_by(user_id=current_user.id).first()
    
    if owner:
        properties = [ownership.property for ownership in 
                     owner.ownerships.filter_by(is_active=True).all()]
    else:
        properties = []
    
    return render_template('citizen/my_properties.html', properties=properties)


@bp.route('/property/<int:property_id>')
@login_required
@citizen_required
def property_detail(property_id):
    """View detailed property information with history and timeline."""
    property_obj = Property.query.get_or_404(property_id)
    
    # Check if user owns this property
    owner = Owner.query.filter_by(user_id=current_user.id).first()
    if not owner:
        flash('Access denied.', 'danger')
        return redirect(url_for('citizen.my_properties'))
    
    ownership = Ownership.query.filter_by(
        property_id=property_id,
        owner_id=owner.id,
        is_active=True
    ).first()
    
    if not ownership:
        flash('Access denied. You do not own this property.', 'danger')
        return redirect(url_for('citizen.my_properties'))
    
    # Get ownership history (all owners including past)
    ownership_history = Ownership.query.filter_by(
        property_id=property_id
    ).order_by(Ownership.acquisition_date.desc()).all()
    
    # Get mutation history
    mutation_history = Mutation.query.filter_by(
        property_id=property_id
    ).order_by(Mutation.created_at.desc()).all()
    
    # Get payment history
    payment_history = Payment.query.filter_by(
        property_id=property_id
    ).order_by(Payment.payment_date.desc()).all()
    
    # Get documents
    from app.models.document import Document
    documents = Document.query.filter_by(
        property_id=property_id
    ).order_by(Document.uploaded_at.desc()).all()
    
    return render_template('citizen/property_detail.html', 
                         property=property_obj, 
                         ownership=ownership,
                         ownership_history=ownership_history,
                         mutation_history=mutation_history,
                         payment_history=payment_history,
                         documents=documents)


@bp.route('/register-property', methods=['GET', 'POST'])
@login_required
@citizen_required
def register_property():
    """Register a new property."""
    form = PropertyRegistrationForm()
    
    # Populate select fields
    form.land_category_id.choices = [(0, 'Select Category')] + [
        (c.id, c.name) for c in LandCategory.query.filter_by(is_active=True).all()
    ]
    form.usage_type_id.choices = [(0, 'Select Usage Type')] + [
        (u.id, u.name) for u in UsageType.query.filter_by(is_active=True).all()
    ]
    
    if form.validate_on_submit():
        # Create property with all form fields
        property_obj = Property(
            # Location details
            state=form.state.data,
            district=form.district.data,
            taluka=form.taluka.data,
            village_city=form.village_city.data,
            locality=form.locality.data,
            sub_locality=form.sub_locality.data,
            street_address=form.street_address.data,
            landmark=form.landmark.data,
            pincode=form.pincode.data,
            ward_number=form.ward_number.data,
            zone=form.zone.data,
            gram_panchayat=form.gram_panchayat.data,
            
            # GPS & Mapping
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            altitude=form.altitude.data,
            
            # Land Measurements
            survey_number=form.survey_number.data,
            plot_number=form.plot_number.data,
            block_number=form.block_number.data,
            khasra_number=form.khasra_number.data,
            area=form.area.data,
            area_unit=form.area_unit.data,
            length=form.length.data,
            width=form.width.data,
            road_frontage=form.road_frontage.data,
            frontage_direction=form.frontage_direction.data if form.frontage_direction.data else None,
            plot_shape=form.plot_shape.data if form.plot_shape.data else None,
            terrain_type=form.terrain_type.data if form.terrain_type.data else None,
            built_up_area=form.built_up_area.data,
            carpet_area=form.carpet_area.data,
            
            # Boundaries
            north_boundary=form.north_boundary.data,
            south_boundary=form.south_boundary.data,
            east_boundary=form.east_boundary.data,
            west_boundary=form.west_boundary.data,
            
            # Property Classification
            property_type=form.property_type.data,
            sub_property_type=form.sub_property_type.data,
            land_category_id=form.land_category_id.data if form.land_category_id.data else None,
            usage_type_id=form.usage_type_id.data if form.usage_type_id.data else None,
            current_land_use=form.current_land_use.data,
            zoning_classification=form.zoning_classification.data,
            property_nature=form.property_nature.data if form.property_nature.data else None,
            property_age_years=form.property_age_years.data,
            property_condition=form.property_condition.data if form.property_condition.data else None,
            occupancy_status=form.occupancy_status.data if form.occupancy_status.data else None,
            
            # Construction Details
            number_of_floors=form.number_of_floors.data,
            number_of_bedrooms=form.number_of_bedrooms.data,
            number_of_bathrooms=form.number_of_bathrooms.data,
            number_of_kitchens=form.number_of_kitchens.data,
            parking_spaces=form.parking_spaces.data,
            construction_type=form.construction_type.data if form.construction_type.data else None,
            flooring_type=form.flooring_type.data,
            year_of_construction=form.year_of_construction.data,
            
            # Soil & Agriculture
            soil_type=form.soil_type.data if form.soil_type.data else None,
            soil_quality=form.soil_quality.data if form.soil_quality.data else None,
            irrigation_type=form.irrigation_type.data,
            current_crop=form.current_crop.data,
            tree_count=form.tree_count.data,
            
            # Water Resources
            water_source=form.water_source.data if form.water_source.data else None,
            borewell_depth_ft=form.borewell_depth_ft.data,
            water_supply_hours_per_day=form.water_supply_hours_per_day.data,
            
            # Electricity & Utilities
            electricity_connection_type=form.electricity_connection_type.data if form.electricity_connection_type.data else None,
            electricity_load_kw=form.electricity_load_kw.data,
            electricity_meter_number=form.electricity_meter_number.data,
            
            # Road & Access
            road_access=form.road_access.data if form.road_access.data else None,
            road_type=form.road_type.data if form.road_type.data else None,
            road_width_ft=form.road_width_ft.data,
            distance_from_main_road_m=form.distance_from_main_road_km.data,
            
            # Amenities
            has_compound_wall=(form.has_compound_wall.data == 'yes') if form.has_compound_wall.data else None,
            has_gate=(form.has_main_gate.data == 'yes') if form.has_main_gate.data else None,
            has_security=(form.has_security.data == 'yes') if form.has_security.data else None,
            
            # Valuation
            market_value=form.market_value.data,
            registered_value=form.registered_value.data,
            stamp_duty_paid=form.stamp_duty_paid.data,
            registration_charges_paid=form.registration_fee_paid.data,
            
            # Legal & Compliance
            has_encumbrance=(form.encumbrance_status.data == 'yes') if form.encumbrance_status.data else False,
            legal_disputes=form.legal_issues.data,
            
            # Additional Info
            description=form.description.data,
            special_features=form.special_features.data,
            
            # Status
            status='pending',
            created_at=datetime.utcnow()
        )
        
        db.session.add(property_obj)
        db.session.flush()  # Get property ID
        
        # Create or get owner
        owner = Owner.query.filter_by(user_id=current_user.id).first()
        if not owner:
            owner = Owner(
                user_id=current_user.id,
                full_name=current_user.full_name,
                phone=current_user.phone,
                email=current_user.email,
                owner_type='individual'
            )
            db.session.add(owner)
            db.session.flush()
        
        # Create ownership
        ownership = Ownership(
            property_id=property_obj.id,
            owner_id=owner.id,
            ownership_percentage=100.0,
            ownership_type='sole',
            acquisition_date=date.today(),
            acquisition_mode='purchase',
            is_active=True
        )
        db.session.add(ownership)
        
        # Handle document uploads
        # (Simplified - in production you'd want proper document handling)
        
        db.session.commit()
        
        flash('Property registration submitted successfully! You will be notified once reviewed.', 'success')
        return redirect(url_for('citizen.my_properties'))
    
    return render_template('citizen/register_property.html', form=form)


@bp.route('/submit-mutation', methods=['GET', 'POST'])
@login_required
@citizen_required
def submit_mutation():
    """Submit a mutation request."""
    form = MutationRequestForm()
    
    # Get user's properties for the dropdown
    owner = Owner.query.filter_by(user_id=current_user.id).first()
    if owner:
        approved_properties = [(ownership.property.id, 
                              f"{ownership.property.ulpin} - {ownership.property.village_city}")
                              for ownership in owner.ownerships.filter_by(is_active=True).all()
                              if ownership.property.status == 'approved']
        form.property_id.choices = approved_properties
    else:
        form.property_id.choices = []
    
    if form.validate_on_submit():
        mutation = Mutation(
            property_id=form.property_id.data,
            requester_id=current_user.id,
            mutation_type=form.mutation_type.data,
            description=form.description.data,
            reason=form.reason.data,
            previous_owners=form.previous_owners.data,
            new_owners=form.new_owners.data,
            status='pending',
            mutation_fee=500.0  # Default fee
        )
        
        db.session.add(mutation)
        db.session.flush()
        
        mutation.generate_mutation_number()
        
        # Handle document uploads
        # (Simplified version)
        
        db.session.commit()
        
        flash('Mutation request submitted successfully!', 'success')
        return redirect(url_for('citizen.my_mutations'))
    
    return render_template('citizen/submit_mutation.html', form=form)


@bp.route('/my-mutations')
@login_required
@citizen_required
def my_mutations():
    """View user's mutation requests."""
    page = request.args.get('page', 1, type=int)
    
    mutations_pagination = Mutation.query.filter_by(
        requester_id=current_user.id
    ).order_by(Mutation.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('citizen/my_mutations.html', mutations=mutations_pagination)


@bp.route('/mutation/<int:mutation_id>')
@login_required
@citizen_required
def mutation_detail(mutation_id):
    """View detailed mutation information."""
    mutation = Mutation.query.get_or_404(mutation_id)
    
    # Verify that this mutation belongs to the current user
    if mutation.requester_id != current_user.id:
        flash('Access denied. This mutation does not belong to you.', 'danger')
        return redirect(url_for('citizen.my_mutations'))
    
    return render_template('citizen/mutation_detail.html', mutation=mutation)


@bp.route('/payments')
@login_required
@citizen_required
def payments():
    """View payment history."""
    page = request.args.get('page', 1, type=int)
    
    payments_pagination = Payment.query.filter_by(
        user_id=current_user.id
    ).order_by(Payment.payment_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('citizen/payments.html', payments=payments_pagination)


@bp.route('/make-payment', methods=['GET', 'POST'])
@login_required
@citizen_required
def make_payment():
    """Make a payment."""
    form = PaymentForm()
    
    # Get user's properties
    owner = Owner.query.filter_by(user_id=current_user.id).first()
    if owner:
        properties = [(ownership.property.id, 
                      f"{ownership.property.ulpin} - {ownership.property.village_city}")
                     for ownership in owner.ownerships.filter_by(is_active=True).all()
                     if ownership.property.status == 'approved']
        form.property_id.choices = properties
    else:
        form.property_id.choices = []
    
    if form.validate_on_submit():
        # Generate unique payment reference before creating payment
        year = datetime.utcnow().year
        # Get last payment ID to generate next reference
        last_payment = Payment.query.order_by(Payment.id.desc()).first()
        next_id = (last_payment.id + 1) if last_payment else 1
        payment_ref = f"PAY{year}{next_id:08d}"
        receipt_num = f"REC{year}{datetime.utcnow().month:02d}{next_id:06d}"
        
        # Create payment with pending status first
        payment = Payment(
            user_id=current_user.id,
            property_id=form.property_id.data,
            payment_type=form.payment_type.data,
            amount=form.amount.data,
            tax_year=form.tax_year.data,
            payment_method=form.payment_method.data,
            payment_mode_details=form.payment_mode_details.data,
            description=form.description.data,
            payment_reference=payment_ref,
            receipt_number=receipt_num,
            status='pending',
            payment_date=datetime.utcnow()
        )
        
        db.session.add(payment)
        db.session.commit()
        
        # Redirect to Razorpay payment gateway simulation
        return redirect(url_for('citizen.razorpay_payment', payment_id=payment.id))
    
    return render_template('citizen/make_payment.html', form=form)


@bp.route('/notifications')
@login_required
@citizen_required
def notifications():
    """View all notifications."""
    page = request.args.get('page', 1, type=int)
    
    notifications_pagination = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    
    # Mark as read
    unread = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    for notif in unread:
        notif.mark_as_read()
    db.session.commit()
    
    return render_template('citizen/notifications.html', notifications=notifications_pagination)


@bp.route('/razorpay-payment/<int:payment_id>')
@login_required
@citizen_required
def razorpay_payment(payment_id):
    """Simulated Razorpay payment gateway."""
    payment = Payment.query.get_or_404(payment_id)
    
    # Verify payment belongs to current user
    if payment.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('citizen.payments'))
    
    # Generate fake transaction ID
    import random
    import string
    transaction_id = 'razorpay_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    
    return render_template('citizen/razorpay_payment.html', 
                         payment=payment,
                         transaction_id=transaction_id)


@bp.route('/process-payment/<int:payment_id>', methods=['POST'])
@login_required
@citizen_required
def process_payment(payment_id):
    """Process the simulated payment."""
    payment = Payment.query.get_or_404(payment_id)
    
    # Verify payment belongs to current user
    if payment.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('citizen.payments'))
    
    # Get payment method from form
    payment_method = request.form.get('payment_method', 'online')
    transaction_id = request.form.get('transaction_id')
    
    # Update payment status
    payment.status = 'completed'
    payment.completed_date = datetime.utcnow()
    payment.receipt_issued_date = datetime.utcnow()
    payment.transaction_id = transaction_id
    payment.payment_method = payment_method
    
    db.session.commit()
    
    flash(f'Payment successful! Receipt Number: {payment.receipt_number}', 'success')
    return redirect(url_for('citizen.payment_success', payment_id=payment.id))


@bp.route('/payment/<int:payment_id>')
@login_required
@citizen_required
def payment_detail(payment_id):
    """View detailed payment information."""
    payment = Payment.query.get_or_404(payment_id)
    
    # Verify payment belongs to current user
    if payment.user_id != current_user.id:
        flash('Access denied. This payment does not belong to you.', 'danger')
        return redirect(url_for('citizen.payments'))
    
    return render_template('citizen/payment_detail.html', payment=payment)


@bp.route('/payment-success/<int:payment_id>')
@login_required
@citizen_required
def payment_success(payment_id):
    """Payment success page with receipt."""
    payment = Payment.query.get_or_404(payment_id)
    
    # Verify payment belongs to current user
    if payment.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('citizen.payments'))
    
    return render_template('citizen/payment_success.html', payment=payment)


@bp.route('/search-properties')
@login_required
@citizen_required
def search_properties():
    """Advanced property search."""
    query = request.args.get('query', '')
    property_type = request.args.get('property_type', '')
    status = request.args.get('status', '')
    district = request.args.get('district', '')
    min_area = request.args.get('min_area', type=float)
    max_area = request.args.get('max_area', type=float)
    
    # Get user's owner record
    owner = Owner.query.filter_by(user_id=current_user.id).first()
    
    if not owner:
        properties = []
    else:
        # Build query
        properties_query = Property.query.join(Ownership).join(Owner).filter(
            Owner.user_id == current_user.id,
            Ownership.is_active == True
        )
        
        # Apply filters
        if query:
            properties_query = properties_query.filter(
                db.or_(
                    Property.ulpin.like(f'%{query}%'),
                    Property.survey_number.like(f'%{query}%'),
                    Property.village_city.like(f'%{query}%'),
                    Property.district.like(f'%{query}%')
                )
            )
        
        if property_type:
            properties_query = properties_query.filter(Property.property_type == property_type)
        
        if status:
            properties_query = properties_query.filter(Property.status == status)
        
        if district:
            properties_query = properties_query.filter(Property.district.like(f'%{district}%'))
        
        if min_area:
            properties_query = properties_query.filter(Property.area >= min_area)
        
        if max_area:
            properties_query = properties_query.filter(Property.area <= max_area)
        
        properties = properties_query.all()
    
    return render_template('citizen/search_properties.html', properties=properties)


@bp.route('/profile')
@login_required
@citizen_required
def profile():
    """View/edit profile."""
    return render_template('citizen/profile.html', user=current_user)
