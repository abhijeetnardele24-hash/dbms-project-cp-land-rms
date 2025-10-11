from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db
from models.tax_assessment import TaxAssessment
from models.parcel import Parcel
from datetime import datetime, date
import traceback

tax_bp = Blueprint('tax', __name__, url_prefix='/tax')

@tax_bp.route('/')
@login_required
def list_tax_assessments():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    year_filter = request.args.get('year', '')
    
    query = TaxAssessment.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if year_filter:
        query = query.filter_by(assessment_year=int(year_filter))
    
    tax_assessments = query.order_by(TaxAssessment.assessment_year.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Get unique years for filter dropdown
    years = db.session.query(TaxAssessment.assessment_year).distinct().order_by(TaxAssessment.assessment_year.desc()).all()
    years = [year[0] for year in years]
    
    return render_template('tax_list.html', 
                         tax_assessments=tax_assessments, 
                         status_filter=status_filter,
                         year_filter=year_filter,
                         years=years)

@tax_bp.route('/<int:tax_id>')
@login_required
def view_tax_assessment(tax_id):
    tax_assessment = TaxAssessment.query.get_or_404(tax_id)
    return render_template('tax_details.html', tax_assessment=tax_assessment)

@tax_bp.route('/test')
@login_required
def test_route():
    return "Tax route is working!"

@tax_bp.route('/test_no_auth')
def test_route_no_auth():
    return "Tax route working without authentication!"

@tax_bp.route('/test_create_no_auth')
def test_create_no_auth():
    try:
        from models.parcel import Parcel
        parcels = Parcel.query.all()
        return f"Found {len(parcels)} parcels. Database working!"
    except Exception as e:
        import traceback
        return f"Error: {str(e)}<br><pre>{traceback.format_exc()}</pre>"

@tax_bp.route('/create_simple')
@login_required
def create_simple():
    """Simple create route for testing"""
    try:
        user_info = f"User: {current_user.username}, Role: {current_user.role}"
        return f"Authenticated route working! {user_info}"
    except Exception as e:
        return f"Error in authenticated route: {str(e)}"

@tax_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_tax_assessment():
    """Create new tax assessment with proper error handling"""
    
    # Check permissions
    if current_user.role not in ['Admin', 'Registrar']:
        flash('You do not have permission to create tax assessments.', 'error')
        return redirect(url_for('tax.list_tax_assessments'))
    
    if request.method == 'POST':
        try:
            # Get and validate form data
            parcel_id = request.form.get('parcel_id')
            assessment_year = request.form.get('assessment_year')
            land_value = request.form.get('land_value')
            building_value = request.form.get('building_value', '0')
            tax_due = request.form.get('tax_due')
            
            # Validate required fields
            if not all([parcel_id, assessment_year, land_value, tax_due]):
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('tax.create_tax_assessment'))
            
            # Convert to proper types
            parcel_id = int(parcel_id)
            assessment_year = int(assessment_year)
            land_value = float(land_value)
            building_value = float(building_value)
            tax_due = float(tax_due)
            total_assessed_value = land_value + building_value
            
            # Verify parcel exists
            parcel = Parcel.query.get(parcel_id)
            if not parcel:
                flash('Selected parcel does not exist.', 'error')
                return redirect(url_for('tax.create_tax_assessment'))
            
            # Create new tax assessment
            tax_assessment = TaxAssessment(
                parcel_id=parcel_id,
                assessment_year=assessment_year,
                land_value=land_value,
                building_value=building_value,
                total_assessed_value=total_assessed_value,
                tax_due=tax_due,
                status='Unpaid'
            )
            
            # Save to database
            db.session.add(tax_assessment)
            db.session.commit()
            
            flash('Tax assessment created successfully!', 'success')
            return redirect(url_for('tax.view_tax_assessment', tax_id=tax_assessment.tax_id))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Invalid input values: {str(e)}', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating tax assessment: {str(e)}', 'error')
    
    # GET request - show form
    try:
        parcels = Parcel.query.all()
        current_year = datetime.now().year
        
        # Use inline HTML to avoid template issues
        html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create Tax Assessment - LRMS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <div class="row">
            <div class="col-lg-8 mx-auto">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-receipt me-2"></i>
                            Create Tax Assessment
                        </h5>
                    </div>
                    <div class="card-body">
                        <form method="POST">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="parcel_id" class="form-label">Parcel <span class="text-danger">*</span></label>
                                        <select class="form-select" id="parcel_id" name="parcel_id" required>
                                            <option value="">Select a parcel</option>
'''
        
        # Add parcel options
        for parcel in parcels:
            html_content += f'                                            <option value="{parcel.parcel_id}">{parcel.survey_no} (ID: {parcel.parcel_id})</option>\n'
        
        html_content += f'''
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="assessment_year" class="form-label">Assessment Year <span class="text-danger">*</span></label>
                                        <input type="number" class="form-control" id="assessment_year" name="assessment_year" 
                                               value="{current_year}" min="2000" max="2100" required>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="land_value" class="form-label">Land Value (₹) <span class="text-danger">*</span></label>
                                        <input type="number" class="form-control" id="land_value" name="land_value" 
                                               step="0.01" min="0" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="building_value" class="form-label">Building Value (₹)</label>
                                        <input type="number" class="form-control" id="building_value" name="building_value" 
                                               value="0" step="0.01" min="0">
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="tax_due" class="form-label">Tax Due (₹) <span class="text-danger">*</span></label>
                                        <input type="number" class="form-control" id="tax_due" name="tax_due" 
                                               step="0.01" min="0" required>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="d-flex justify-content-between">
                                <a href="/tax/" class="btn btn-secondary">
                                    <i class="bi bi-arrow-left me-1"></i>Back to List
                                </a>
                                <button type="submit" class="btn btn-primary">
                                    <i class="bi bi-check-lg me-1"></i>Create Assessment
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Auto-calculate tax (1% of total value)
        function calculateTax() {{
            const landValue = parseFloat(document.getElementById('land_value').value) || 0;
            const buildingValue = parseFloat(document.getElementById('building_value').value) || 0;
            const total = landValue + buildingValue;
            const taxDue = total * 0.01; // 1% tax rate
            document.getElementById('tax_due').value = taxDue.toFixed(2);
        }}
        
        document.getElementById('land_value').addEventListener('input', calculateTax);
        document.getElementById('building_value').addEventListener('input', calculateTax);
    </script>
</body>
</html>
'''
        
        return html_content
        
    except Exception as e:
        traceback.print_exc()
        flash(f'Error loading form: {str(e)}', 'error')
        return redirect(url_for('tax.list_tax_assessments'))

@tax_bp.route('/<int:tax_id>/payment', methods=['GET', 'POST'])
@login_required
def record_payment(tax_id):
    if current_user.role not in ['Admin', 'Registrar']:
        flash('You do not have permission to record payments.', 'error')
        return redirect(url_for('tax.view_tax_assessment', tax_id=tax_id))
    
    tax_assessment = TaxAssessment.query.get_or_404(tax_id)
    
    if request.method == 'POST':
        try:
            payment_amount = float(request.form.get('payment_amount'))
            payment_date = datetime.strptime(request.form.get('payment_date'), '%Y-%m-%d').date()
            
            tax_assessment.amount_paid = (tax_assessment.amount_paid or 0) + payment_amount
            tax_assessment.paid_on = payment_date
            
            # Update status based on payment
            if tax_assessment.amount_paid >= tax_assessment.tax_due:
                tax_assessment.status = 'Paid'
            elif tax_assessment.amount_paid > 0:
                tax_assessment.status = 'Partial'
            else:
                tax_assessment.status = 'Unpaid'
            
            db.session.commit()
            
            flash(f'Payment of ₹{payment_amount:,.2f} recorded successfully!', 'success')
            return redirect(url_for('tax.view_tax_assessment', tax_id=tax_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error recording payment: {str(e)}', 'error')
    
    return render_template('tax_payment.html', tax_assessment=tax_assessment)

@tax_bp.route('/api/summary')
@login_required
def tax_summary_api():
    """API endpoint for tax summary statistics"""
    current_year = datetime.now().year
    
    # Total assessments for current year
    total_assessments = TaxAssessment.query.filter_by(assessment_year=current_year).count()
    
    # Total tax due and collected for current year
    current_year_taxes = TaxAssessment.query.filter_by(assessment_year=current_year).all()
    total_due = sum(tax.tax_due for tax in current_year_taxes)
    total_collected = sum(tax.amount_paid or 0 for tax in current_year_taxes)
    
    # Status breakdown
    paid_count = TaxAssessment.query.filter_by(assessment_year=current_year, status='Paid').count()
    unpaid_count = TaxAssessment.query.filter_by(assessment_year=current_year, status='Unpaid').count()
    partial_count = TaxAssessment.query.filter_by(assessment_year=current_year, status='Partial').count()
    
    return jsonify({
        'total_assessments': total_assessments,
        'total_due': float(total_due),
        'total_collected': float(total_collected),
        'collection_rate': (total_collected / total_due * 100) if total_due > 0 else 0,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
        'partial_count': partial_count
    })
