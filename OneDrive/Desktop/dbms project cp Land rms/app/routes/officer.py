"""
Officer routes for mutation requests and ownership updates.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.models import db
from app.models.mutation import Mutation
from app.models.audit_log import AuditLog
from app.utils.decorators import officer_required
from app.utils.notification_utils import notify_mutation_status_change
from app.forms.mutation_forms import MutationApprovalForm

bp = Blueprint('officer', __name__)


@bp.route('/dashboard')
@login_required
@officer_required
def dashboard():
    """Officer dashboard."""
    
    # Statistics
    pending_mutations = Mutation.query.filter_by(status='pending').count()
    under_review = Mutation.query.filter_by(status='under_review').count()
    my_approvals = Mutation.query.filter_by(processed_by=current_user.id).count()
    
    # Recent mutations
    recent_mutations = Mutation.query.order_by(Mutation.created_at.desc()).limit(10).all()
    
    return render_template('officer/dashboard.html',
                         pending_mutations=pending_mutations,
                         under_review=under_review,
                         my_approvals=my_approvals,
                         recent_mutations=recent_mutations)


@bp.route('/pending-mutations')
@login_required
@officer_required
def pending_mutations():
    """View pending mutation requests."""
    page = request.args.get('page', 1, type=int)
    
    mutations_pagination = Mutation.query.filter(
        Mutation.status.in_(['pending', 'under_review', 'documents_verified'])
    ).order_by(Mutation.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('officer/pending_mutations.html', 
                         mutations=mutations_pagination)


@bp.route('/mutation/<int:mutation_id>')
@login_required
@officer_required
def view_mutation(mutation_id):
    """View mutation details."""
    mutation = Mutation.query.get_or_404(mutation_id)
    form = MutationApprovalForm()
    
    return render_template('officer/mutation_detail.html', 
                         mutation=mutation, form=form)


@bp.route('/mutation/<int:mutation_id>/process', methods=['POST'])
@login_required
@officer_required
def process_mutation(mutation_id):
    """Approve or reject mutation request."""
    mutation = Mutation.query.get_or_404(mutation_id)
    form = MutationApprovalForm()
    
    if form.validate_on_submit():
        try:
            action = form.action.data
            comments = form.officer_comments.data
            
            # Set processing date and officer for all actions
            mutation.processing_date = datetime.utcnow()
            mutation.processed_by = current_user.id
            mutation.officer_comments = comments
            
            if action == 'approve':
                mutation.status = 'approved'
                mutation.approval_date = datetime.utcnow()
                
                # Generate certificate number
                if not mutation.mutation_certificate_number:
                    mutation.generate_certificate_number()
                    mutation.certificate_issued_date = datetime.utcnow()
                
                # Log action
                AuditLog.log_action(
                    user_id=current_user.id,
                    action='approve_mutation',
                    action_type='approve',
                    entity_type='mutation',
                    entity_id=mutation.id,
                    description=f'Officer approved mutation: {mutation.mutation_number}',
                    status='success'
                )
                
                # Notify requester
                notify_mutation_status_change(mutation.id, 'approved', mutation.requester_id)
                
                flash('Mutation request approved successfully!', 'success')
                
            elif action == 'reject':
                mutation.status = 'rejected'
                mutation.rejection_date = datetime.utcnow()
                mutation.rejection_reason = comments
                
                # Log action
                AuditLog.log_action(
                    user_id=current_user.id,
                    action='reject_mutation',
                    action_type='reject',
                    entity_type='mutation',
                    entity_id=mutation.id,
                    description=f'Officer rejected mutation: {mutation.mutation_number}',
                    status='success'
                )
                
                # Notify requester
                notify_mutation_status_change(mutation.id, 'rejected', mutation.requester_id)
                
                flash('Mutation request rejected.', 'warning')
                
            elif action == 'request_info':
                mutation.status = 'information_required'
                mutation.additional_info_required = form.additional_info_required.data
                
                # Notify requester
                notify_mutation_status_change(mutation.id, 'information_required', mutation.requester_id)
                
                flash('Additional information requested from applicant.', 'info')
            
            # Commit all changes
            db.session.commit()
            
            return redirect(url_for('officer.pending_mutations'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error processing mutation: {str(e)}', 'danger')
            return redirect(url_for('officer.view_mutation', mutation_id=mutation_id))
    
    # Form validation failed
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field}: {error}', 'danger')
    
    return redirect(url_for('officer.view_mutation', mutation_id=mutation_id))


@bp.route('/my-approvals')
@login_required
@officer_required
def my_approvals():
    """View mutations approved by current officer."""
    page = request.args.get('page', 1, type=int)
    
    mutations_pagination = Mutation.query.filter_by(
        processed_by=current_user.id
    ).order_by(Mutation.approval_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('officer/my_approvals.html', 
                         mutations=mutations_pagination)
