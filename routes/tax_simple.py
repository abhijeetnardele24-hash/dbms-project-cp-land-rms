from flask import Blueprint, request, session, redirect
from models import db
from models.tax_assessment import TaxAssessment
from models.parcel import Parcel
from datetime import datetime

# Simple blueprint without complex dependencies
tax_simple_bp = Blueprint('tax_simple', __name__, url_prefix='/tax_simple')

@tax_simple_bp.route('/')
def list_tax():
    """Simple tax list without authentication"""
    try:
        assessments = TaxAssessment.query.all()
        
        html = """<!DOCTYPE html>
<html><head><title>Tax Assessments</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head><body><div class="container mt-4">
<h2>Tax Assessments</h2>
<a href="/tax_simple/create" class="btn btn-primary mb-3">Create New</a>
<table class="table"><thead><tr><th>ID</th><th>Parcel</th><th>Year</th><th>Tax Due</th><th>Status</th></tr></thead><tbody>"""
        
        for a in assessments:
            html += f"<tr><td>{a.tax_id}</td><td>{a.parcel_id}</td><td>{a.assessment_year}</td><td>₹{a.tax_due}</td><td>{a.status}</td></tr>"
        
        html += "</tbody></table></div></body></html>"
        return html
    except Exception as e:
        return f"Error: {str(e)}"

@tax_simple_bp.route('/create', methods=['GET', 'POST'])
def create_tax():
    """Simple create without authentication"""
    
    if request.method == 'POST':
        try:
            # Get form data
            parcel_id = int(request.form['parcel_id'])
            year = int(request.form['year'])
            land_value = float(request.form['land_value'])
            building_value = float(request.form.get('building_value', 0))
            tax_due = float(request.form['tax_due'])
            
            # Create assessment
            assessment = TaxAssessment(
                parcel_id=parcel_id,
                assessment_year=year,
                land_value=land_value,
                building_value=building_value,
                total_assessed_value=land_value + building_value,
                tax_due=tax_due,
                status='Unpaid'
            )
            
            db.session.add(assessment)
            db.session.commit()
            
            return f"""<!DOCTYPE html>
<html><head><title>Success</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head><body><div class="container mt-4">
<div class="alert alert-success">
<h4>Success!</h4>
<p>Tax assessment created with ID: {assessment.tax_id}</p>
</div>
<a href="/tax_simple/" class="btn btn-primary">View All</a>
<a href="/tax_simple/create" class="btn btn-secondary">Create Another</a>
</div></body></html>"""
            
        except Exception as e:
            return f"""<!DOCTYPE html>
<html><head><title>Error</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head><body><div class="container mt-4">
<div class="alert alert-danger">Error: {str(e)}</div>
<a href="/tax_simple/create" class="btn btn-primary">Try Again</a>
</div></body></html>"""
    
    # GET - show form
    try:
        parcels = Parcel.query.all()
        year = datetime.now().year
        
        html = f"""<!DOCTYPE html>
<html><head><title>Create Tax Assessment</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head><body><div class="container mt-4">
<div class="card"><div class="card-header"><h5>Create Tax Assessment</h5></div>
<div class="card-body">
<form method="POST">
<div class="mb-3">
<label>Parcel:</label>
<select name="parcel_id" class="form-select" required>
<option value="">Select Parcel</option>"""
        
        for p in parcels:
            html += f'<option value="{p.parcel_id}">Survey: {p.survey_no} (ID: {p.parcel_id})</option>'
        
        html += f"""</select></div>
<div class="mb-3">
<label>Year:</label>
<input type="number" name="year" class="form-control" value="{year}" required>
</div>
<div class="mb-3">
<label>Land Value (₹):</label>
<input type="number" name="land_value" class="form-control" step="0.01" required>
</div>
<div class="mb-3">
<label>Building Value (₹):</label>
<input type="number" name="building_value" class="form-control" step="0.01" value="0">
</div>
<div class="mb-3">
<label>Tax Due (₹):</label>
<input type="number" name="tax_due" class="form-control" step="0.01" required>
</div>
<button type="submit" class="btn btn-primary">Create</button>
<a href="/tax_simple/" class="btn btn-secondary">Cancel</a>
</form></div></div></div></body></html>"""
        
        return html
    except Exception as e:
        return f"Error loading form: {str(e)}"
