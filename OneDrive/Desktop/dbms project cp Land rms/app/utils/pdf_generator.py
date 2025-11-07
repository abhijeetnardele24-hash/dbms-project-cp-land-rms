"""
PDF Report Generator
Generates professional PDFs for certificates, receipts, and reports
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import os


class PDFGenerator:
    """Generate professional PDF documents"""
    
    @staticmethod
    def generate_property_certificate(property_data, qr_code_path=None):
        """
        Generate property certificate PDF
        
        Args:
            property_data: Dictionary containing property information
            qr_code_path: Path to QR code image (optional)
            
        Returns:
            BytesIO object containing PDF
        """
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, 
                                   topMargin=0.5*inch, bottomMargin=0.5*inch)
            
            # Container for elements
            elements = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a237e'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=styles['Normal'],
                fontSize=14,
                textColor=colors.HexColor('#4a5568'),
                spaceAfter=20,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'Heading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#2c5282'),
                spaceAfter=12,
                spaceBefore=15,
                fontName='Helvetica-Bold'
            )
            
            # Header
            elements.append(Paragraph("LAND REGISTRY MANAGEMENT SYSTEM", title_style))
            elements.append(Paragraph("Property Ownership Certificate", subtitle_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # Certificate Number and Date
            cert_data = [
                ['Certificate No:', property_data.get('certificate_no', 'N/A')],
                ['Issue Date:', datetime.now().strftime('%d %B %Y')],
                ['ULPIN:', property_data.get('ulpin', 'N/A')]
            ]
            
            cert_table = Table(cert_data, colWidths=[2*inch, 4*inch])
            cert_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2d3748')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#4a5568')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(cert_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Property Details Section
            elements.append(Paragraph("Property Details", heading_style))
            
            property_details = [
                ['Location:', f"{property_data.get('village_city', 'N/A')}, {property_data.get('district', 'N/A')}"],
                ['State:', property_data.get('state', 'N/A')],
                ['Survey Number:', property_data.get('survey_number', 'N/A')],
                ['Area:', f"{property_data.get('area', 'N/A')} {property_data.get('area_unit', 'sqft')}"],
                ['Property Type:', property_data.get('property_type', 'N/A').title()],
                ['Status:', property_data.get('status', 'N/A').upper()]
            ]
            
            property_table = Table(property_details, colWidths=[2*inch, 4*inch])
            property_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2d3748')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#4a5568')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#e2e8f0')),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(property_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Owner Details Section
            if property_data.get('owner_name'):
                elements.append(Paragraph("Owner Information", heading_style))
                
                owner_details = [
                    ['Owner Name:', property_data.get('owner_name', 'N/A')],
                    ['Contact:', property_data.get('owner_phone', 'N/A')],
                    ['Email:', property_data.get('owner_email', 'N/A')]
                ]
                
                owner_table = Table(owner_details, colWidths=[2*inch, 4*inch])
                owner_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2d3748')),
                    ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#4a5568')),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#e2e8f0')),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                elements.append(owner_table)
                elements.append(Spacer(1, 0.3*inch))
            
            # QR Code
            if qr_code_path and os.path.exists(qr_code_path):
                qr_img = Image(qr_code_path, width=1.5*inch, height=1.5*inch)
                elements.append(Paragraph("Scan to Verify", subtitle_style))
                elements.append(qr_img)
                elements.append(Spacer(1, 0.2*inch))
            
            # Footer
            elements.append(Spacer(1, 0.5*inch))
            footer_text = """
            <para align=center fontSize=9 textColor=#718096>
            This is a computer-generated certificate and does not require a signature.<br/>
            For verification, scan the QR code or visit our website.<br/>
            © 2025 Land Registry Management System. All rights reserved.
            </para>
            """
            elements.append(Paragraph(footer_text, styles['Normal']))
            
            # Build PDF
            doc.build(elements)
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            print(f"Error generating property certificate: {str(e)}")
            return None
    
    @staticmethod
    def generate_payment_receipt(payment_data):
        """
        Generate payment receipt PDF
        
        Args:
            payment_data: Dictionary containing payment information
            
        Returns:
            BytesIO object containing PDF
        """
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                   topMargin=0.5*inch, bottomMargin=0.5*inch)
            
            elements = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontSize=22,
                textColor=colors.HexColor('#047857'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            # Header
            elements.append(Paragraph("PAYMENT RECEIPT", title_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # Receipt Box
            receipt_data = [
                ['Receipt Number:', payment_data.get('receipt_number', 'N/A')],
                ['Payment Reference:', payment_data.get('payment_reference', 'N/A')],
                ['Transaction ID:', payment_data.get('transaction_id', 'N/A')],
                ['Date & Time:', datetime.now().strftime('%d %B %Y, %I:%M %p')],
                ['', '']
            ]
            
            receipt_table = Table(receipt_data, colWidths=[2.5*inch, 3.5*inch])
            receipt_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(receipt_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Amount Section
            amount_style = ParagraphStyle(
                'Amount',
                parent=styles['Heading1'],
                fontSize=32,
                textColor=colors.HexColor('#047857'),
                spaceAfter=10,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            elements.append(Paragraph(f"₹ {payment_data.get('amount', '0.00')}", amount_style))
            elements.append(Spacer(1, 0.3*inch))
            
            # Payment Details
            payment_details = [
                ['Payment Type:', payment_data.get('payment_type', 'N/A').title()],
                ['Payment Method:', payment_data.get('payment_method', 'N/A').title()],
                ['Property ULPIN:', payment_data.get('property_ulpin', 'N/A')],
                ['Paid By:', payment_data.get('user_name', 'N/A')],
                ['Status:', 'COMPLETED ✓']
            ]
            
            details_table = Table(payment_details, colWidths=[2.5*inch, 3.5*inch])
            details_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#6b7280')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#d1d5db')),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(details_table)
            
            # Footer
            elements.append(Spacer(1, 1*inch))
            footer_text = """
            <para align=center fontSize=9 textColor=#6b7280>
            This is a computer-generated receipt and does not require a signature.<br/>
            Please keep this receipt for your records.<br/>
            For any queries, contact us at support@lrms.com<br/>
            © 2025 Land Registry Management System
            </para>
            """
            elements.append(Paragraph(footer_text, styles['Normal']))
            
            # Build PDF
            doc.build(elements)
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            print(f"Error generating payment receipt: {str(e)}")
            return None
    
    @staticmethod
    def generate_mutation_certificate(mutation_data):
        """
        Generate mutation certificate PDF
        
        Args:
            mutation_data: Dictionary containing mutation information
            
        Returns:
            BytesIO object containing PDF
        """
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                   topMargin=0.5*inch, bottomMargin=0.5*inch)
            
            elements = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontSize=22,
                textColor=colors.HexColor('#7c3aed'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            # Header
            elements.append(Paragraph("MUTATION CERTIFICATE", title_style))
            elements.append(Paragraph("Property Ownership Transfer", styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            
            # Mutation Details
            mutation_details = [
                ['Mutation Number:', mutation_data.get('mutation_number', 'N/A')],
                ['Property ULPIN:', mutation_data.get('property_ulpin', 'N/A')],
                ['Mutation Type:', mutation_data.get('mutation_type', 'N/A').title()],
                ['Previous Owner:', mutation_data.get('previous_owners', 'N/A')],
                ['New Owner:', mutation_data.get('new_owners', 'N/A')],
                ['Approval Date:', mutation_data.get('approval_date', datetime.now().strftime('%d %B %Y'))],
                ['Status:', 'APPROVED ✓']
            ]
            
            details_table = Table(mutation_details, colWidths=[2.5*inch, 3.5*inch])
            details_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#d1d5db')),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(details_table)
            
            # Footer
            elements.append(Spacer(1, 1*inch))
            footer_text = """
            <para align=center fontSize=9 textColor=#6b7280>
            This certificate confirms the approved mutation of property ownership.<br/>
            © 2025 Land Registry Management System
            </para>
            """
            elements.append(Paragraph(footer_text, styles['Normal']))
            
            # Build PDF
            doc.build(elements)
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            print(f"Error generating mutation certificate: {str(e)}")
            return None


# Convenience functions
def create_property_certificate(property_data, qr_path=None):
    """Generate property certificate PDF"""
    return PDFGenerator.generate_property_certificate(property_data, qr_path)

def create_payment_receipt(payment_data):
    """Generate payment receipt PDF"""
    return PDFGenerator.generate_payment_receipt(payment_data)

def create_mutation_certificate(mutation_data):
    """Generate mutation certificate PDF"""
    return PDFGenerator.generate_mutation_certificate(mutation_data)
