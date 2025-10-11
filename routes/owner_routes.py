from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from utils.decorators import role_required, registrar_required
from models import db
from models.owner import Owner
from models.ownership import Ownership
from datetime import datetime

owner_bp = Blueprint('owner', __name__, url_prefix='/owner')

@owner_bp.route('/')
@login_required
def list_owners():
    print(f"DEBUG: list_owners route called by user {current_user.username}")
    page = request.args.get('page', 1, type=int)
    owners = Owner.query.paginate(
        page=page, per_page=20, error_out=False
    )
    print(f"DEBUG: Found {owners.total} owners")
    return render_template('owner_list.html', owners=owners)

@owner_bp.route('/<int:owner_id>')
@login_required
def view_owner(owner_id):
    from models.tenant_agreement import TenantAgreement
    
    owner = Owner.query.get_or_404(owner_id)
    ownerships = Ownership.query.filter_by(owner_id=owner_id).all()
    
    # Get tenant agreements where this owner is the property owner
    agreements_as_owner = TenantAgreement.query.filter_by(owner_id=owner_id).all()
    
    # Get tenant agreements where this owner is the tenant
    agreements_as_tenant = TenantAgreement.query.filter_by(tenant_id=owner_id).all()
    
    from datetime import date
    
    return render_template('owner_details.html', 
                         owner=owner, 
                         ownerships=ownerships,
                         agreements_as_owner=agreements_as_owner,
                         agreements_as_tenant=agreements_as_tenant,
                         today=date.today())

@owner_bp.route('/create', methods=['GET', 'POST'])
@registrar_required
def create_owner():
    
    if request.method == 'POST':
        try:
            owner = Owner(
                name=request.form.get('name'),
                owner_type=request.form.get('owner_type'),
                pan=request.form.get('pan'),
                address=request.form.get('address'),
                contact_no=request.form.get('contact_no')
            )
            
            # Handle Aadhaar encryption properly
            aadhaar_number = request.form.get('aadhaar_number')
            if aadhaar_number:
                try:
                    owner.set_aadhaar(aadhaar_number)
                except Exception as e:
                    print(f"Aadhaar encryption error: {str(e)}")
                    # Continue without Aadhaar if encryption fails
            
            db.session.add(owner)
            db.session.commit()
            
            flash('Owner created successfully!', 'success')
            return redirect(url_for('owner.view_owner', owner_id=owner.owner_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating owner: {str(e)}', 'error')
            print(f"DEBUG: Owner creation error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    return render_template('owner_form.html', owner=None)

@owner_bp.route('/<int:owner_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_owner(owner_id):
    if current_user.role not in ['Admin', 'Registrar']:
        flash('You do not have permission to edit owners.', 'error')
        return redirect(url_for('owner.view_owner', owner_id=owner_id))
    
    owner = Owner.query.get_or_404(owner_id)
    
    if request.method == 'POST':
        try:
            owner.name = request.form.get('name')
            owner.owner_type = request.form.get('owner_type')
            owner.pan = request.form.get('pan')
            owner.address = request.form.get('address')
            owner.contact_no = request.form.get('contact_no')
            
            # Handle Aadhaar encryption properly
            aadhaar_number = request.form.get('aadhaar_number')
            if aadhaar_number:
                try:
                    owner.set_aadhaar(aadhaar_number)
                except Exception as e:
                    print(f"Aadhaar encryption error: {str(e)}")
                    # Continue without updating Aadhaar if encryption fails
            
            db.session.commit()
            
            flash('Owner updated successfully!', 'success')
            return redirect(url_for('owner.view_owner', owner_id=owner_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating owner: {str(e)}', 'error')
    
    return render_template('owner_form.html', owner=owner)

@owner_bp.route('/<int:owner_id>/add_ownership', methods=['GET', 'POST'])
@login_required
def add_ownership(owner_id):
    """Add ownership of a parcel to this owner"""
    if current_user.role not in ['Admin', 'Registrar']:
        flash('You do not have permission to add ownership.', 'error')
        return redirect(url_for('owner.view_owner', owner_id=owner_id))
    
    owner = Owner.query.get_or_404(owner_id)
    
    if request.method == 'POST':
        try:
            from models.ownership import Ownership
            from models.parcel import Parcel
            from datetime import datetime
            
            parcel_id = int(request.form.get('parcel_id'))
            ownership_type = request.form.get('ownership_type')
            share_fraction = float(request.form.get('share_fraction', 1.0))
            date_from = datetime.strptime(request.form.get('date_from'), '%Y-%m-%d').date()
            
            # Check if parcel exists
            parcel = Parcel.query.get(parcel_id)
            if not parcel:
                flash('Selected parcel does not exist.', 'error')
                return redirect(url_for('owner.add_ownership', owner_id=owner_id))
            
            # Check if ownership already exists for this owner and parcel
            existing_ownership = Ownership.query.filter_by(
                owner_id=owner_id,
                parcel_id=parcel_id,
                date_to=None  # Active ownership
            ).first()
            
            if existing_ownership:
                flash('This owner already has active ownership of this parcel.', 'error')
                return redirect(url_for('owner.add_ownership', owner_id=owner_id))
            
            # Create new ownership
            ownership = Ownership(
                owner_id=owner_id,
                parcel_id=parcel_id,
                ownership_type=ownership_type,
                share_fraction=share_fraction,
                date_from=date_from,
                date_to=None  # Active ownership
            )
            
            db.session.add(ownership)
            db.session.commit()
            
            flash(f'Ownership added successfully! {owner.name} now owns {share_fraction*100}% of parcel {parcel.survey_no}.', 'success')
            return redirect(url_for('owner.view_owner', owner_id=owner_id))
            
        except ValueError as e:
            db.session.rollback()
            flash('Invalid input values. Please check your entries.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding ownership: {str(e)}', 'error')
            print(f"DEBUG: Ownership creation error: {str(e)}")
    
    # GET request - show form with available parcels
    try:
        from models.parcel import Parcel
        from models.ownership import Ownership
        
        # Get all parcels
        all_parcels = Parcel.query.all()
        
        # Get parcels already owned by this owner
        owned_parcel_ids = db.session.query(Ownership.parcel_id).filter_by(
            owner_id=owner_id,
            date_to=None  # Active ownerships only
        ).all()
        owned_parcel_ids = [pid[0] for pid in owned_parcel_ids]
        
        # Available parcels (not owned by this owner)
        available_parcels = [p for p in all_parcels if p.parcel_id not in owned_parcel_ids]
        
        from datetime import date
        return render_template('add_ownership.html', 
                             owner=owner, 
                             available_parcels=available_parcels,
                             today=date.today())
    except Exception as e:
        flash(f'Error loading form: {str(e)}', 'error')
        return redirect(url_for('owner.view_owner', owner_id=owner_id))

@owner_bp.route('/api/search')
@login_required
def search_owners_api():
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    
    owners = Owner.query.filter(
        Owner.name.contains(query)
    ).limit(10).all()
    
    return jsonify([{
        'id': owner.owner_id,
        'name': owner.name,
        'owner_type': owner.owner_type,
        'contact_no': owner.contact_no
    } for owner in owners])
