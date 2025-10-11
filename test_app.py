#!/usr/bin/env python3
"""
Minimal test app to isolate the issue
"""

from flask import Flask, request, redirect, url_for
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key'

@app.route('/')
def index():
    return """
    <h1>Test App Working!</h1>
    <p><a href="/test_tax">Test Tax Route</a></p>
    <p><a href="/test_db">Test Database</a></p>
    <p><a href="/test_create">Test Create Form</a></p>
    """

@app.route('/test_tax')
def test_tax():
    return "Tax route working in test app!"

@app.route('/test_db')
def test_db():
    try:
        from config import Config
        from models import db
        from models.tax_assessment import TaxAssessment
        from models.parcel import Parcel
        
        app.config.from_object(Config)
        db.init_app(app)
        
        with app.app_context():
            parcels = Parcel.query.all()
            assessments = TaxAssessment.query.all()
            
        return f"Database test successful! Parcels: {len(parcels)}, Assessments: {len(assessments)}"
    except Exception as e:
        import traceback
        return f"Database test failed: {str(e)}<br><pre>{traceback.format_exc()}</pre>"

@app.route('/test_create', methods=['GET', 'POST'])
def test_create():
    if request.method == 'POST':
        try:
            from config import Config
            from models import db
            from models.tax_assessment import TaxAssessment
            
            app.config.from_object(Config)
            db.init_app(app)
            
            with app.app_context():
                # Create test assessment
                assessment = TaxAssessment(
                    parcel_id=1,
                    assessment_year=2025,
                    land_value=100000.0,
                    building_value=50000.0,
                    total_assessed_value=150000.0,
                    tax_due=1500.0,
                    status='Unpaid'
                )
                
                db.session.add(assessment)
                db.session.commit()
                
                return f"SUCCESS! Created assessment with ID: {assessment.tax_id}"
                
        except Exception as e:
            import traceback
            return f"ERROR: {str(e)}<br><pre>{traceback.format_exc()}</pre>"
    
    # GET request - show form
    return """
    <form method="POST">
        <h2>Test Tax Assessment Creation</h2>
        <button type="submit">Create Test Assessment</button>
    </form>
    """

if __name__ == '__main__':
    print("Starting test app on port 5008...")
    app.run(debug=True, host='0.0.0.0', port=5008)
