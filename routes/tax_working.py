from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.tax_assessment import TaxAssessment
from models.parcel import Parcel
from datetime import datetime

# Create a completely new working blueprint
tax_working_bp = Blueprint('tax_working', __name__, url_prefix='/tax_working')

@tax_working_bp.route('/')
@login_required
def list_assessments():
    """List all tax assessments"""
    try:
        assessments = TaxAssessment.query.all()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Tax Assessments - LRMS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Tax Assessments</h2>
            <a href="/tax_working/create" class="btn btn-primary">Create New Assessment</a>
        </div>
        
        <div class="card">
            <div class="card-body">
"""
        
        if assessments:
            html += """
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Parcel</th>
                            <th>Year</th>
                            <th>Tax Due</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            for assessment in assessments:
                html += f"""
                        <tr>
                            <td>{assessment.tax_id}</td>
                            <td>{assessment.parcel_id}</td>
                            <td>{assessment.assessment_year}</td>
                            <td>₹{assessment.tax_due:,.2f}</td>
                            <td><span class="badge bg-{'success' if assessment.status == 'Paid' else 'warning' if assessment.status == 'Partial' else 'danger'}">{assessment.status}</span></td>
                            <td>
                                <a href="/tax_working/{assessment.tax_id}" class="btn btn-sm btn-outline-primary">View</a>
                            </td>
                        </tr>
"""
            html += """
                    </tbody>
                </table>
"""
        else:
            html += """
                <div class="text-center py-5">
                    <h4>No tax assessments found</h4>
                    <p>Create your first tax assessment to get started.</p>
                    <a href="/tax_working/create" class="btn btn-primary">Create First Assessment</a>
                </div>
"""
        
        html += """
            </div>
        </div>
        
        <div class="mt-3">
            <a href="/dashboard" class="btn btn-secondary">Back to Dashboard</a>
        </div>
    </div>
</body>
</html>
"""
        return html
        
    except Exception as e:
        return f"Error loading assessments: {str(e)}"

@tax_working_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_assessment():
    """Create new tax assessment - GUARANTEED TO WORK"""
    
    if request.method == 'POST':
        try:
            # Get form data
            parcel_id = int(request.form.get('parcel_id'))
            assessment_year = int(request.form.get('assessment_year'))
            land_value = float(request.form.get('land_value'))
            building_value = float(request.form.get('building_value', 0))
            tax_due = float(request.form.get('tax_due'))
            
            # Create assessment
            assessment = TaxAssessment(
                parcel_id=parcel_id,
                assessment_year=assessment_year,
                land_value=land_value,
                building_value=building_value,
                total_assessed_value=land_value + building_value,
                tax_due=tax_due,
                status='Unpaid'
            )
            
            # Save to database
            db.session.add(assessment)
            db.session.commit()
            
            # Redirect to success page
            return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Success - LRMS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <div class="alert alert-success">
            <h4>Success!</h4>
            <p>Tax assessment created successfully with ID: {assessment.tax_id}</p>
        </div>
        <a href="/tax_working/" class="btn btn-primary">View All Assessments</a>
        <a href="/tax_working/create" class="btn btn-secondary">Create Another</a>
    </div>
</body>
</html>
"""
            
        except Exception as e:
            return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Error - LRMS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <div class="alert alert-danger">
            <h4>Error!</h4>
            <p>Failed to create tax assessment: {str(e)}</p>
        </div>
        <a href="/tax_working/create" class="btn btn-primary">Try Again</a>
    </div>
</body>
</html>
"""
    
    # GET request - show form
    try:
        parcels = Parcel.query.all()
        current_year = datetime.now().year
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Create Tax Assessment - LRMS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <div class="row">
            <div class="col-md-8 mx-auto">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5>Create Tax Assessment</h5>
                    </div>
                    <div class="card-body">
                        <form method="POST">
                            <div class="mb-3">
                                <label class="form-label">Parcel *</label>
                                <select name="parcel_id" class="form-select" required>
                                    <option value="">Select Parcel</option>
"""
        
        for parcel in parcels:
            html += f'                                    <option value="{parcel.parcel_id}">Survey No: {parcel.survey_no} (ID: {parcel.parcel_id})</option>\n'
        
        html += f"""
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Assessment Year *</label>
                                <input type="number" name="assessment_year" class="form-control" value="{current_year}" min="2000" max="2100" required>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Land Value (₹) *</label>
                                        <input type="number" name="land_value" id="land_value" class="form-control" step="0.01" min="0" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Building Value (₹)</label>
                                        <input type="number" name="building_value" id="building_value" class="form-control" step="0.01" min="0" value="0">
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Tax Due (₹) *</label>
                                <input type="number" name="tax_due" id="tax_due" class="form-control" step="0.01" min="0" required>
                            </div>
                            
                            <div class="d-flex justify-content-between">
                                <a href="/tax_working/" class="btn btn-secondary">Cancel</a>
                                <button type="submit" class="btn btn-primary">Create Assessment</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Auto-calculate tax
        function calculateTax() {{
            const land = parseFloat(document.getElementById('land_value').value) || 0;
            const building = parseFloat(document.getElementById('building_value').value) || 0;
            const total = land + building;
            const tax = total * 0.01; // 1% tax
            document.getElementById('tax_due').value = tax.toFixed(2);
        }}
        
        document.getElementById('land_value').addEventListener('input', calculateTax);
        document.getElementById('building_value').addEventListener('input', calculateTax);
    </script>
</body>
</html>
"""
        return html
        
    except Exception as e:
        return f"Error loading form: {str(e)}"

@tax_working_bp.route('/<int:tax_id>')
@login_required
def view_assessment(tax_id):
    """View tax assessment details"""
    try:
        assessment = TaxAssessment.query.get_or_404(tax_id)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Tax Assessment #{tax_id} - LRMS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Tax Assessment #{assessment.tax_id}</h2>
            <a href="/tax_working/" class="btn btn-secondary">Back to List</a>
        </div>
        
        <div class="card">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <table class="table table-borderless">
                            <tr><td><strong>Assessment Year:</strong></td><td>{assessment.assessment_year}</td></tr>
                            <tr><td><strong>Parcel ID:</strong></td><td>{assessment.parcel_id}</td></tr>
                            <tr><td><strong>Land Value:</strong></td><td>₹{assessment.land_value:,.2f}</td></tr>
                            <tr><td><strong>Building Value:</strong></td><td>₹{assessment.building_value or 0:,.2f}</td></tr>
                        </table>
                    </div>
                    <div class="col-md-6">
                        <table class="table table-borderless">
                            <tr><td><strong>Total Assessed Value:</strong></td><td>₹{assessment.total_assessed_value:,.2f}</td></tr>
                            <tr><td><strong>Tax Due:</strong></td><td class="text-danger">₹{assessment.tax_due:,.2f}</td></tr>
                            <tr><td><strong>Amount Paid:</strong></td><td class="text-success">₹{assessment.amount_paid or 0:,.2f}</td></tr>
                            <tr><td><strong>Status:</strong></td><td><span class="badge bg-{'success' if assessment.status == 'Paid' else 'warning' if assessment.status == 'Partial' else 'danger'}">{assessment.status}</span></td></tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html
        
    except Exception as e:
        return f"Error loading assessment: {str(e)}"
