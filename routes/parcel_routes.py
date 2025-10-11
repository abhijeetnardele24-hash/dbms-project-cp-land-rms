from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db
from models.parcel import Parcel
from models.location import Location
from models.ownership import Ownership
from models.encumbrance import Encumbrance
from models.tax_assessment import TaxAssessment
from sqlalchemy import or_

parcel_bp = Blueprint('parcel', __name__, url_prefix='/parcel')

@parcel_bp.route('/')
@login_required
def list_parcels():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Parcel.query.join(Location)
    
    if search:
        query = query.filter(
            or_(
                Parcel.ulpin.contains(search),
                Parcel.survey_no.contains(search),
                Location.village.contains(search),
                Location.district.contains(search)
            )
        )
    
    parcels = query.paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('parcel_list.html', parcels=parcels, search=search)

@parcel_bp.route('/<int:parcel_id>')
@login_required
def view_parcel(parcel_id):
    parcel = Parcel.query.get_or_404(parcel_id)
    ownerships = Ownership.query.filter_by(parcel_id=parcel_id, date_to=None).all()
    encumbrances = Encumbrance.query.filter_by(parcel_id=parcel_id, status='Active').all()
    tax_assessments = TaxAssessment.query.filter_by(parcel_id=parcel_id).order_by(TaxAssessment.assessment_year.desc()).limit(5).all()
    
    return render_template('parcel_details.html', 
                         parcel=parcel, 
                         ownerships=ownerships,
                         encumbrances=encumbrances,
                         tax_assessments=tax_assessments)

@parcel_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_parcel():
    if current_user.role not in ['Admin', 'Registrar']:
        flash('You do not have permission to create parcels.', 'error')
        return redirect(url_for('parcel.list_parcels'))
    
    if request.method == 'POST':
        try:
            # Create or get location
            location = Location.query.filter_by(
                village=request.form.get('village'),
                taluka=request.form.get('taluka'),
                district=request.form.get('district'),
                state=request.form.get('state'),
                pincode=request.form.get('pincode')
            ).first()
            
            if not location:
                location = Location(
                    village=request.form.get('village'),
                    taluka=request.form.get('taluka'),
                    district=request.form.get('district'),
                    state=request.form.get('state'),
                    pincode=request.form.get('pincode')
                )
                db.session.add(location)
                db.session.flush()
            
            parcel = Parcel(
                ulpin=request.form.get('ulpin'),
                survey_no=request.form.get('survey_no'),
                total_area=float(request.form.get('total_area')),
                land_category=request.form.get('land_category'),
                current_use_type=request.form.get('current_use_type'),
                location_id=location.location_id,
                centroid_lat=float(request.form.get('centroid_lat')) if request.form.get('centroid_lat') else None,
                centroid_lon=float(request.form.get('centroid_lon')) if request.form.get('centroid_lon') else None
            )
            
            db.session.add(parcel)
            db.session.commit()
            
            flash('Parcel created successfully!', 'success')
            return redirect(url_for('parcel.view_parcel', parcel_id=parcel.parcel_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating parcel: {str(e)}', 'error')
    
    return render_template('parcel_form.html', parcel=None)

@parcel_bp.route('/<int:parcel_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_parcel(parcel_id):
    if current_user.role not in ['Admin', 'Registrar']:
        flash('You do not have permission to edit parcels.', 'error')
        return redirect(url_for('parcel.view_parcel', parcel_id=parcel_id))
    
    parcel = Parcel.query.get_or_404(parcel_id)
    
    if request.method == 'POST':
        try:
            parcel.survey_no = request.form.get('survey_no')
            parcel.total_area = float(request.form.get('total_area'))
            parcel.land_category = request.form.get('land_category')
            parcel.current_use_type = request.form.get('current_use_type')
            parcel.centroid_lat = float(request.form.get('centroid_lat')) if request.form.get('centroid_lat') else None
            parcel.centroid_lon = float(request.form.get('centroid_lon')) if request.form.get('centroid_lon') else None
            
            db.session.commit()
            
            flash('Parcel updated successfully!', 'success')
            return redirect(url_for('parcel.view_parcel', parcel_id=parcel_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating parcel: {str(e)}', 'error')
    
    return render_template('parcel_form.html', parcel=parcel)
