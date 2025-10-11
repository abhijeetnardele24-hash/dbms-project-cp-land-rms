"""
Document routes for Government Property Management Portal
Handles document management, uploads, and viewing
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from utils.decorators import role_required, registrar_required
from utils.file_handler import file_handler
from models import db
from models.document import Document
from models.mutation import Mutation
from models.encumbrance import Encumbrance
from models.tenant_agreement import TenantAgreement
from datetime import datetime
import os

document_bp = Blueprint('document', __name__, url_prefix='/document')

@document_bp.route('/')
@login_required
def list_documents():
    """List all documents with filtering"""
    page = request.args.get('page', 1, type=int)
    doc_type_filter = request.args.get('doc_type', '')
    search = request.args.get('search', '')
    
    query = Document.query
    
    if doc_type_filter:
        query = query.filter_by(doc_type=doc_type_filter)
    
    if search:
        query = query.filter(Document.file_name.contains(search))
    
    documents = query.order_by(Document.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Get document types for filter
    doc_types = ['Sale Deed', 'Lease Deed', 'Mutation Record', 'Encumbrance', 'Tax Receipt']
    
    return render_template('document_list.html', 
                         documents=documents,
                         doc_types=doc_types,
                         doc_type_filter=doc_type_filter,
                         search=search)

@document_bp.route('/<int:document_id>')
@login_required
def view_document(document_id):
    """View document details"""
    document = Document.query.get_or_404(document_id)
    
    # Find related records
    related_mutations = Mutation.query.filter_by(document_id=document_id).all()
    related_encumbrances = Encumbrance.query.filter_by(document_id=document_id).all()
    related_agreements = TenantAgreement.query.filter_by(document_id=document_id).all()
    
    return render_template('document_details.html', 
                         document=document,
                         related_mutations=related_mutations,
                         related_encumbrances=related_encumbrances,
                         related_agreements=related_agreements)

@document_bp.route('/upload', methods=['GET', 'POST'])
@registrar_required
def upload_document():
    """Upload new document"""
    if request.method == 'POST':
        try:
            # Get form data
            doc_type = request.form.get('doc_type')
            registration_office = request.form.get('registration_office')
            registered_at = request.form.get('registered_at')
            
            # Handle file upload
            uploaded_file = request.files.get('document_file')
            if not uploaded_file or uploaded_file.filename == '':
                flash('Please select a file to upload.', 'error')
                return render_template('document_upload.html')
            
            # Save file securely
            success, filename, error_msg = file_handler.save_file(
                uploaded_file, 
                upload_folder='uploads/documents',
                file_type='documents'
            )
            
            if not success:
                flash(f'File upload failed: {error_msg}', 'error')
                return render_template('document_upload.html')
            
            # Create document record
            document = Document(
                doc_type=doc_type,
                file_name=uploaded_file.filename,
                file_path=f'uploads/documents/{filename}',
                registration_office=registration_office,
                registered_at=datetime.strptime(registered_at, '%Y-%m-%d') if registered_at else None
            )
            
            db.session.add(document)
            db.session.commit()
            
            flash('Document uploaded successfully!', 'success')
            return redirect(url_for('document.view_document', document_id=document.document_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error uploading document: {str(e)}', 'error')
    
    doc_types = ['Sale Deed', 'Lease Deed', 'Mutation Record', 'Encumbrance', 'Tax Receipt']
    return render_template('document_upload.html', doc_types=doc_types)

@document_bp.route('/<int:document_id>/download')
@login_required
def download_document(document_id):
    """Download document file"""
    document = Document.query.get_or_404(document_id)
    
    if not document.file_path:
        flash('Document file not found.', 'error')
        return redirect(url_for('document.view_document', document_id=document_id))
    
    try:
        file_path = os.path.join('static', document.file_path)
        return send_file(file_path, as_attachment=True, download_name=document.file_name)
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('document.view_document', document_id=document_id))

@document_bp.route('/<int:document_id>/delete', methods=['POST'])
@role_required('Admin')
def delete_document(document_id):
    """Delete document (Admin only)"""
    document = Document.query.get_or_404(document_id)
    
    try:
        # Delete physical file
        if document.file_path:
            file_handler.delete_file(
                os.path.basename(document.file_path),
                upload_folder='uploads/documents'
            )
        
        # Delete database record
        db.session.delete(document)
        db.session.commit()
        
        flash('Document deleted successfully!', 'success')
        return redirect(url_for('document.list_documents'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting document: {str(e)}', 'error')
        return redirect(url_for('document.view_document', document_id=document_id))

@document_bp.route('/api/search')
@login_required
def search_documents_api():
    """API endpoint for document search"""
    query = request.args.get('q', '')
    doc_type = request.args.get('type', '')
    
    if len(query) < 2:
        return jsonify([])
    
    search_query = Document.query.filter(Document.file_name.contains(query))
    
    if doc_type:
        search_query = search_query.filter_by(doc_type=doc_type)
    
    documents = search_query.limit(10).all()
    
    return jsonify([{
        'id': doc.document_id,
        'file_name': doc.file_name,
        'doc_type': doc.doc_type,
        'registered_at': doc.registered_at.strftime('%Y-%m-%d') if doc.registered_at else None,
        'registration_office': doc.registration_office
    } for doc in documents])

@document_bp.route('/api/stats')
@login_required
def document_stats_api():
    """API endpoint for document statistics"""
    
    # Document type distribution
    type_stats = db.session.query(
        Document.doc_type,
        db.func.count(Document.document_id).label('count')
    ).group_by(Document.doc_type).all()
    
    # Recent uploads
    recent_count = Document.query.filter(
        Document.created_at >= datetime.now().replace(hour=0, minute=0, second=0)
    ).count()
    
    # Total documents
    total_docs = Document.query.count()
    
    return jsonify({
        'total_documents': total_docs,
        'recent_uploads': recent_count,
        'type_distribution': [{'type': stat[0], 'count': stat[1]} for stat in type_stats]
    })
