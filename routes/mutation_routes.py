from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db
from models.mutation import Mutation
from models.parcel import Parcel
from models.owner import Owner
from datetime import datetime, date

mutation_bp = Blueprint('mutation', __name__, url_prefix='/mutation')

@mutation_bp.route('/')
@login_required
def list_mutations():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = Mutation.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    mutations = query.order_by(Mutation.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('mutation_list.html', mutations=mutations, status_filter=status_filter)

@mutation_bp.route('/<int:mutation_id>')
@login_required
def view_mutation(mutation_id):
    mutation = Mutation.query.get_or_404(mutation_id)
    return render_template('mutation_details.html', mutation=mutation)

@mutation_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_mutation():
    if current_user.role not in ['Admin', 'Registrar']:
        flash('You do not have permission to create mutations.', 'error')
        return redirect(url_for('mutation.list_mutations'))
    
    if request.method == 'POST':
        try:
            mutation = Mutation(
                parcel_id=int(request.form.get('parcel_id')),
                from_owner_id=int(request.form.get('from_owner_id')),
                to_owner_id=int(request.form.get('to_owner_id')),
                mutation_type=request.form.get('mutation_type'),
                date_of_mutation=datetime.strptime(request.form.get('date_of_mutation'), '%Y-%m-%d').date(),
                consideration_value=float(request.form.get('consideration_value')) if request.form.get('consideration_value') else None,
                status='Pending'
            )
            
            db.session.add(mutation)
            db.session.commit()
            
            flash('Mutation created successfully!', 'success')
            return redirect(url_for('mutation.view_mutation', mutation_id=mutation.mutation_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating mutation: {str(e)}', 'error')
    
    parcels = Parcel.query.all()
    owners = Owner.query.all()
    return render_template('mutation_form.html', mutation=None, parcels=parcels, owners=owners)

@mutation_bp.route('/<int:mutation_id>/approve', methods=['POST'])
@login_required
def approve_mutation(mutation_id):
    if current_user.role not in ['Admin', 'Approver']:
        flash('You do not have permission to approve mutations.', 'error')
        return redirect(url_for('mutation.view_mutation', mutation_id=mutation_id))
    
    mutation = Mutation.query.get_or_404(mutation_id)
    
    if mutation.status != 'Pending':
        flash('Only pending mutations can be approved.', 'error')
        return redirect(url_for('mutation.view_mutation', mutation_id=mutation_id))
    
    try:
        mutation.status = 'Approved'
        mutation.approved_by = current_user.user_id
        mutation.approved_on = date.today()
        
        # Update ownership records
        # End current ownership
        current_ownership = db.session.query(Ownership).filter_by(
            parcel_id=mutation.parcel_id,
            owner_id=mutation.from_owner_id,
            date_to=None
        ).first()
        
        if current_ownership:
            current_ownership.date_to = mutation.date_of_mutation
        
        # Create new ownership
        new_ownership = Ownership(
            parcel_id=mutation.parcel_id,
            owner_id=mutation.to_owner_id,
            share_fraction=current_ownership.share_fraction if current_ownership else 1.0,
            ownership_type='Freehold',  # Default, can be customized
            date_from=mutation.date_of_mutation
        )
        
        db.session.add(new_ownership)
        db.session.commit()
        
        flash('Mutation approved successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error approving mutation: {str(e)}', 'error')
    
    return redirect(url_for('mutation.view_mutation', mutation_id=mutation_id))

@mutation_bp.route('/<int:mutation_id>/reject', methods=['POST'])
@login_required
def reject_mutation(mutation_id):
    if current_user.role not in ['Admin', 'Approver']:
        flash('You do not have permission to reject mutations.', 'error')
        return redirect(url_for('mutation.view_mutation', mutation_id=mutation_id))
    
    mutation = Mutation.query.get_or_404(mutation_id)
    
    if mutation.status != 'Pending':
        flash('Only pending mutations can be rejected.', 'error')
        return redirect(url_for('mutation.view_mutation', mutation_id=mutation_id))
    
    try:
        mutation.status = 'Rejected'
        mutation.approved_by = current_user.user_id
        mutation.approved_on = date.today()
        
        db.session.commit()
        
        flash('Mutation rejected successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error rejecting mutation: {str(e)}', 'error')
    
    return redirect(url_for('mutation.view_mutation', mutation_id=mutation_id))
