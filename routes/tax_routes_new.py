from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db
from datetime import datetime

# Create a new blueprint for testing
tax_new_bp = Blueprint('tax_new', __name__, url_prefix='/tax_new')

@tax_new_bp.route('/')
@login_required
def list_tax_assessments():
    return "Tax New Route Working - List"

@tax_new_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_tax_assessment():
    print("DEBUG: NEW tax route accessed")
    
    if request.method == 'POST':
        print("DEBUG: POST request received")
        return "Form submitted successfully!"
    
    # Simple GET request - return basic HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Tax Form</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row">
                <div class="col-md-6 mx-auto">
                    <div class="card">
                        <div class="card-header">
                            <h5>Create Tax Assessment</h5>
                        </div>
                        <div class="card-body">
                            <form method="POST">
                                <div class="mb-3">
                                    <label class="form-label">Parcel ID</label>
                                    <input type="number" class="form-control" name="parcel_id" value="1" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Assessment Year</label>
                                    <input type="number" class="form-control" name="assessment_year" value="2025" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Land Value</label>
                                    <input type="number" class="form-control" name="land_value" step="0.01" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Building Value</label>
                                    <input type="number" class="form-control" name="building_value" step="0.01" value="0">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Tax Due</label>
                                    <input type="number" class="form-control" name="tax_due" step="0.01" required>
                                </div>
                                <button type="submit" class="btn btn-primary">Create Assessment</button>
                                <a href="/tax_new/" class="btn btn-secondary">Cancel</a>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@tax_new_bp.route('/test_db')
@login_required
def test_database():
    try:
        # Test basic database connectivity
        from models.parcel import Parcel
        parcels = Parcel.query.all()
        return f"Database test successful. Found {len(parcels)} parcels."
    except Exception as e:
        return f"Database test failed: {str(e)}"

@tax_new_bp.route('/test_create_real', methods=['POST'])
@login_required
def test_create_real():
    try:
        from models.tax_assessment import TaxAssessment
        
        # Get form data
        parcel_id = int(request.form.get('parcel_id', 1))
        assessment_year = int(request.form.get('assessment_year', 2025))
        land_value = float(request.form.get('land_value', 100000))
        building_value = float(request.form.get('building_value', 0))
        tax_due = float(request.form.get('tax_due', 1000))
        
        # Create assessment
        tax_assessment = TaxAssessment(
            parcel_id=parcel_id,
            assessment_year=assessment_year,
            land_value=land_value,
            building_value=building_value,
            total_assessed_value=land_value + building_value,
            tax_due=tax_due,
            status='Unpaid'
        )
        
        db.session.add(tax_assessment)
        db.session.commit()
        
        return f"Tax assessment created successfully! ID: {tax_assessment.tax_id}"
        
    except Exception as e:
        db.session.rollback()
        import traceback
        return f"Error: {str(e)}<br><pre>{traceback.format_exc()}</pre>"
