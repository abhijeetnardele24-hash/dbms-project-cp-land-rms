from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db
from models.tenant_agreement import TenantAgreement
from models.owner import Owner
from models.parcel import Parcel
from utils.decorators import registrar_required
from datetime import datetime

tenant_bp = Blueprint('tenant', __name__, url_prefix='/tenant')

@tenant_bp.route('/create/<int:owner_id>', methods=['GET', 'POST'])
@registrar_required
def create_agreement(owner_id):
    """Create a new tenant agreement for an owner"""
    owner = Owner.query.get_or_404(owner_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            parcel_id = int(request.form.get('parcel_id'))
            tenant_id = int(request.form.get('tenant_id'))
            tenant_name = request.form.get('tenant_name')
            phone_number = request.form.get('phone_number')
            rent_amount = float(request.form.get('rent_amount', 0))
            deposit_amount = float(request.form.get('deposit_amount', 0))
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
            end_date_str = request.form.get('end_date')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            
            # Validate parcel exists and is owned by this owner
            from models.ownership import Ownership
            ownership = Ownership.query.filter_by(
                owner_id=owner_id,
                parcel_id=parcel_id,
                date_to=None  # Active ownership
            ).first()
            
            if not ownership:
                flash('You can only create agreements for parcels you own.', 'error')
                return redirect(url_for('tenant.create_agreement', owner_id=owner_id))
            
            # Create tenant agreement
            agreement = TenantAgreement(
                parcel_id=parcel_id,
                owner_id=owner_id,
                tenant_id=tenant_id,
                tenant_name=tenant_name,
                phone_number=phone_number,
                rent_amount=rent_amount,
                deposit_amount=deposit_amount,
                start_date=start_date,
                end_date=end_date
            )
            
            db.session.add(agreement)
            db.session.commit()
            
            flash(f'Tenant agreement created successfully! Agreement ID: {agreement.agreement_id}', 'success')
            return redirect(url_for('owner.view_owner', owner_id=owner_id))
            
        except ValueError as e:
            db.session.rollback()
            flash('Invalid input values. Please check your entries.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating agreement: {str(e)}', 'error')
            print(f"DEBUG: Agreement creation error: {str(e)}")
    
    # GET request - show form
    try:
        from models.ownership import Ownership
        
        # Get parcels owned by this owner
        owned_parcels = db.session.query(Parcel).join(Ownership).filter(
            Ownership.owner_id == owner_id,
            Ownership.date_to == None  # Active ownership
        ).all()
        
        # Get all potential tenants (other owners)
        potential_tenants = Owner.query.filter(Owner.owner_id != owner_id).all()
        
        from datetime import date
        return render_template('tenant_agreement_form.html',
                             owner=owner,
                             owned_parcels=owned_parcels,
                             potential_tenants=potential_tenants,
                             today=date.today())
    except Exception as e:
        flash(f'Error loading form: {str(e)}', 'error')
        return redirect(url_for('owner.view_owner', owner_id=owner_id))

@tenant_bp.route('/<int:agreement_id>')
@login_required
def view_agreement(agreement_id):
    """View tenant agreement details"""
    agreement = TenantAgreement.query.get_or_404(agreement_id)
    return render_template('tenant_agreement_details.html', agreement=agreement)

@tenant_bp.route('/api/tenant/<int:tenant_id>')
@login_required
def get_tenant_info(tenant_id):
    """Get tenant information for auto-fill"""
    tenant = Owner.query.get_or_404(tenant_id)
    return jsonify({
        'name': tenant.name,
        'phone': tenant.contact_no
    })
