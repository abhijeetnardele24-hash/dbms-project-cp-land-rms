"""
PDF Export utilities for generating certificates, reports, and documents.
Uses ReportLab library for professional PDF generation.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.platypus import PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
import io


def generate_mutation_certificate_pdf(mutation):
    """
    Generate a professional mutation certificate PDF.
    
    Args:
        mutation: Mutation object with related property and owner data
        
    Returns:
        BytesIO: PDF file as bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Certificate_Title',
                             parent=styles['Heading1'],
                             fontSize=24,
                             textColor=colors.HexColor('#4a5568'),
                             alignment=TA_CENTER,
                             spaceAfter=30))
    
    styles.add(ParagraphStyle(name='Certificate_Subtitle',
                             parent=styles['Normal'],
                             fontSize=14,
                             textColor=colors.HexColor('#718096'),
                             alignment=TA_CENTER,
                             spaceAfter=20))
    
    styles.add(ParagraphStyle(name='Certificate_Body',
                             parent=styles['Normal'],
                             fontSize=11,
                             alignment=TA_LEFT,
                             spaceAfter=12))
    
    # Title
    title = Paragraph("MUTATION CERTIFICATE", styles['Certificate_Title'])
    elements.append(title)
    
    subtitle = Paragraph("Land Registry Management System", styles['Certificate_Subtitle'])
    elements.append(subtitle)
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Certificate Number Box
    cert_data = [
        ['Certificate Number:', mutation.mutation_certificate_number or 'N/A'],
        ['Issue Date:', mutation.certificate_issued_date.strftime('%d %B %Y') if mutation.certificate_issued_date else 'N/A']
    ]
    
    cert_table = Table(cert_data, colWidths=[2.5*inch, 3.5*inch])
    cert_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2d3748')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
    ]))
    
    elements.append(cert_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Property Details
    prop_text = Paragraph("<b>Property Details</b>", styles['Certificate_Body'])
    elements.append(prop_text)
    
    property_data = [
        ['ULPIN:', mutation.property.ulpin],
        ['Property Type:', mutation.property.property_type.replace('_', ' ').title()],
        ['Address:', f"{mutation.property.locality}, {mutation.property.district}"],
        ['Pincode:', mutation.property.pincode],
        ['Area:', f"{mutation.property.area_sqft} sq ft"],
        ['Market Value:', f"₹{mutation.property.market_value:,.2f}"]
    ]
    
    prop_table = Table(property_data, colWidths=[2*inch, 4*inch])
    prop_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2d3748')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    
    elements.append(prop_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Mutation Details
    mutation_text = Paragraph("<b>Mutation Details</b>", styles['Certificate_Body'])
    elements.append(mutation_text)
    
    mutation_details = [
        ['Mutation Type:', mutation.mutation_type.replace('_', ' ').title()],
        ['Previous Owner:', mutation.previous_owners or 'N/A'],
        ['New Owner:', mutation.new_owners or 'N/A'],
        ['Application Date:', mutation.created_at.strftime('%d %B %Y')],
        ['Approval Date:', mutation.approval_date.strftime('%d %B %Y') if mutation.approval_date else 'N/A'],
        ['Status:', mutation.status.replace('_', ' ').title()]
    ]
    
    if mutation.processed_by_user:
        mutation_details.append(['Processed By:', mutation.processed_by_user.full_name])
    
    if mutation.officer_comments:
        mutation_details.append(['Comments:', mutation.officer_comments])
    
    mut_table = Table(mutation_details, colWidths=[2*inch, 4*inch])
    mut_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2d3748')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    
    elements.append(mut_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # QR Code (if available)
    try:
        from app.utils.qr_code_generator import generate_certificate_qr
        qr_data = generate_certificate_qr(mutation.mutation_certificate_number, mutation.id)
        
        if qr_data and qr_data.startswith('data:image/png;base64,'):
            import base64
            qr_bytes = base64.b64decode(qr_data.split(',')[1])
            qr_image = Image(BytesIO(qr_bytes), width=1.5*inch, height=1.5*inch)
            
            qr_label = Paragraph("<b>Scan to Verify</b>", styles['Certificate_Subtitle'])
            elements.append(qr_label)
            elements.append(qr_image)
    except Exception as e:
        pass  # Skip QR code if generation fails
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_text = f"""
    <para align=center>
    <font size=8 color='#718096'>
    This is an official document issued by the Land Registry Management System.<br/>
    Certificate generated on {datetime.now().strftime('%d %B %Y at %I:%M %p')}<br/>
    For verification, visit: http://verify.landregistry.gov.in/verify/{mutation.mutation_certificate_number}
    </font>
    </para>
    """
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_properties_pdf(properties):
    """
    Generate PDF report of properties.
    
    Args:
        properties: List of Property objects
        
    Returns:
        BytesIO: PDF file as bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=36, leftMargin=36,
                           topMargin=36, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    title = Paragraph("Properties Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary
    summary_text = f"<b>Total Properties:</b> {len(properties)}<br/><b>Generated:</b> {datetime.now().strftime('%d %B %Y at %I:%M %p')}"
    elements.append(Paragraph(summary_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Properties Table
    data = [['ULPIN', 'Type', 'District', 'Area (sqft)', 'Value (₹)']]
    
    for prop in properties:
        data.append([
            prop.ulpin,
            prop.property_type.replace('_', ' ').title()[:15],
            prop.district[:15],
            f"{prop.area_sqft:,}",
            f"₹{prop.market_value:,.0f}"
        ])
    
    table = Table(data, colWidths=[2*inch, 1.3*inch, 1.3*inch, 1*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_mutations_pdf(mutations):
    """Generate PDF report of mutations."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=36, leftMargin=36,
                           topMargin=36, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                fontSize=18, textColor=colors.HexColor('#2d3748'),
                                spaceAfter=30, alignment=TA_CENTER)
    
    title = Paragraph("Mutations Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    summary_text = f"<b>Total Mutations:</b> {len(mutations)}<br/><b>Generated:</b> {datetime.now().strftime('%d %B %Y at %I:%M %p')}"
    elements.append(Paragraph(summary_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    data = [['Mutation #', 'Type', 'Property', 'Status', 'Date']]
    
    for mut in mutations:
        data.append([
            mut.mutation_number or 'N/A',
            mut.mutation_type.replace('_', ' ').title()[:12],
            mut.property.ulpin[:20],
            mut.status.replace('_', ' ').title(),
            mut.created_at.strftime('%d/%m/%y')
        ])
    
    table = Table(data, colWidths=[1.5*inch, 1.2*inch, 2*inch, 1.2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer
