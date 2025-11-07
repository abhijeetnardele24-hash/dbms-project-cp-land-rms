"""
Download routes for PDF certificates and reports
"""

from flask import Blueprint, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from io import BytesIO

from app.models import Property, Payment, Mutation, Owner, Ownership, User, db
from app.utils.pdf_generator import (
    create_property_certificate,
    create_payment_receipt,
    create_mutation_certificate
)
from app.utils.qr_generator import save_property_qr

bp = Blueprint('download', __name__, url_prefix='/download')


@bp.route('/certificate/<ulpin>')
@login_required
def download_certificate(ulpin):
    """Download property certificate PDF"""
    try:
        # Get property
        property_obj = Property.query.filter_by(ulpin=ulpin).first_or_404()
        
        # Check if user has access
        if current_user.role not in ['admin', 'registrar']:
            # Check if user owns the property
            owner = Owner.query.filter_by(user_id=current_user.id).first()
            if not owner:
                flash('Access denied.', 'danger')
                return redirect(url_for('citizen.dashboard'))
            
            ownership = Ownership.query.filter_by(
                property_id=property_obj.id,
                owner_id=owner.id,
                is_active=True
            ).first()
            
            if not ownership:
                flash('Access denied. You do not own this property.', 'danger')
                return redirect(url_for('citizen.my_properties'))
        
        # Generate QR code
        qr_path = save_property_qr(ulpin)
        
        # Get owner details
        ownership = Ownership.query.filter_by(
            property_id=property_obj.id,
            is_active=True
        ).first()
        
        owner = ownership.owner if ownership else None
        
        # Prepare property data
        property_data = {
            'certificate_no': f'CERT{property_obj.id:06d}',
            'ulpin': property_obj.ulpin,
            'village_city': property_obj.village_city,
            'district': property_obj.district,
            'state': property_obj.state or 'Maharashtra',
            'survey_number': property_obj.survey_number or 'N/A',
            'area': property_obj.area,
            'area_unit': property_obj.area_unit or 'sqft',
            'property_type': property_obj.property_type or 'residential',
            'status': property_obj.status,
            'owner_name': owner.full_name if owner else 'N/A',
            'owner_phone': owner.phone if owner else 'N/A',
            'owner_email': owner.email if owner else 'N/A'
        }
        
        # Generate PDF
        pdf_buffer = create_property_certificate(property_data, qr_path)
        
        if pdf_buffer:
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'Property_Certificate_{ulpin}.pdf'
            )
        else:
            flash('Error generating certificate.', 'danger')
            return redirect(url_for('citizen.my_properties'))
            
    except Exception as e:
        print(f"Error downloading certificate: {str(e)}")
        flash('Error generating certificate.', 'danger')
        return redirect(url_for('citizen.my_properties'))


@bp.route('/receipt/<int:payment_id>')
@login_required
def download_receipt(payment_id):
    """Download payment receipt PDF"""
    try:
        # Get payment
        payment = Payment.query.get_or_404(payment_id)
        
        # Check if user has access
        if current_user.role not in ['admin', 'registrar'] and payment.user_id != current_user.id:
            flash('Access denied.', 'danger')
            return redirect(url_for('citizen.payments'))
        
        # Get property details
        property_obj = payment.property if payment.property_id else None
        
        # Prepare payment data
        payment_data = {
            'receipt_number': payment.receipt_number or f'REC{payment.id:08d}',
            'payment_reference': payment.payment_reference or f'PAY{payment.id:08d}',
            'transaction_id': payment.transaction_id or 'N/A',
            'amount': f'{payment.amount:.2f}',
            'payment_type': payment.payment_type or 'general',
            'payment_method': payment.payment_method or 'online',
            'property_ulpin': property_obj.ulpin if property_obj else 'N/A',
            'user_name': payment.user.full_name if payment.user else 'N/A'
        }
        
        # Generate PDF
        pdf_buffer = create_payment_receipt(payment_data)
        
        if pdf_buffer:
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'Payment_Receipt_{payment.receipt_number}.pdf'
            )
        else:
            flash('Error generating receipt.', 'danger')
            return redirect(url_for('citizen.payments'))
            
    except Exception as e:
        print(f"Error downloading receipt: {str(e)}")
        flash('Error generating receipt.', 'danger')
        return redirect(url_for('citizen.payments'))


@bp.route('/mutation-certificate/<int:mutation_id>')
@login_required
def download_mutation_certificate(mutation_id):
    """Download mutation certificate PDF"""
    try:
        # Get mutation
        mutation = Mutation.query.get_or_404(mutation_id)
        
        # Check if approved
        if mutation.status != 'approved':
            flash('Certificate only available for approved mutations.', 'warning')
            return redirect(url_for('citizen.my_mutations'))
        
        # Check if user has access
        if current_user.role not in ['admin', 'officer'] and mutation.requester_id != current_user.id:
            flash('Access denied.', 'danger')
            return redirect(url_for('citizen.my_mutations'))
        
        # Get property details
        property_obj = mutation.property
        
        # Prepare mutation data
        mutation_data = {
            'mutation_number': mutation.mutation_number or f'MUT{mutation.id:06d}',
            'property_ulpin': property_obj.ulpin if property_obj else 'N/A',
            'mutation_type': mutation.mutation_type or 'transfer',
            'previous_owners': mutation.previous_owners or 'N/A',
            'new_owners': mutation.new_owners or 'N/A',
            'approval_date': mutation.approval_date.strftime('%d %B %Y') if mutation.approval_date else datetime.now().strftime('%d %B %Y')
        }
        
        # Generate PDF
        pdf_buffer = create_mutation_certificate(mutation_data)
        
        if pdf_buffer:
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'Mutation_Certificate_{mutation.mutation_number}.pdf'
            )
        else:
            flash('Error generating certificate.', 'danger')
            return redirect(url_for('citizen.my_mutations'))
            
    except Exception as e:
        print(f"Error downloading mutation certificate: {str(e)}")
        flash('Error generating certificate.', 'danger')
        return redirect(url_for('citizen.my_mutations'))


@bp.route('/monthly-report/<int:year>/<int:month>')
@login_required
def download_monthly_report(year, month):
    """Download monthly revenue report PDF"""
    try:
        # Only admin can download reports
        if current_user.role != 'admin':
            flash('Access denied. Admin only.', 'danger')
            return redirect(url_for('main.index'))
        
        # Import here to avoid circular import
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from sqlalchemy import func, extract
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        elements.append(Paragraph(f"Monthly Revenue Report", title_style))
        elements.append(Paragraph(f"{month_names[month]} {year}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Get statistics
        payments = Payment.query.filter(
            Payment.status == 'completed',
            extract('year', Payment.payment_date) == year,
            extract('month', Payment.payment_date) == month
        ).all()
        
        total_revenue = sum(p.amount for p in payments)
        total_transactions = len(payments)
        
        # Summary table
        summary_data = [
            ['Month:', f"{month_names[month]} {year}"],
            ['Total Transactions:', str(total_transactions)],
            ['Total Revenue:', f"₹ {total_revenue:,.2f}"],
            ['Average Transaction:', f"₹ {(total_revenue/total_transactions if total_transactions > 0 else 0):,.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#d1d5db')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Payment breakdown by type
        payment_types = {}
        for payment in payments:
            ptype = payment.payment_type or 'other'
            if ptype not in payment_types:
                payment_types[ptype] = {'count': 0, 'amount': 0}
            payment_types[ptype]['count'] += 1
            payment_types[ptype]['amount'] += payment.amount
        
        if payment_types:
            elements.append(Paragraph("Payment Breakdown by Type", styles['Heading2']))
            
            breakdown_data = [['Payment Type', 'Transactions', 'Amount']]
            for ptype, data in payment_types.items():
                breakdown_data.append([
                    ptype.replace('_', ' ').title(),
                    str(data['count']),
                    f"₹ {data['amount']:,.2f}"
                ])
            
            breakdown_table = Table(breakdown_data, colWidths=[2*inch, 1.5*inch, 2*inch])
            breakdown_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(breakdown_table)
        
        # Footer
        elements.append(Spacer(1, 0.5*inch))
        footer = f"""
        <para align=center fontSize=9 textColor=#6b7280>
        Generated on {datetime.now().strftime('%d %B %Y, %I:%M %p')}<br/>
        © 2025 Land Registry Management System
        </para>
        """
        elements.append(Paragraph(footer, styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Monthly_Report_{month_names[month]}_{year}.pdf'
        )
        
    except Exception as e:
        print(f"Error generating monthly report: {str(e)}")
        flash('Error generating report.', 'danger')
        return redirect(url_for('admin.dashboard'))
