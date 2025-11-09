"""
QR Code Generator for Certificate Verification
"""
import qrcode
from io import BytesIO
import base64
from flask import url_for


def generate_qr_code(data, size=10, border=2):
    """
    Generate QR code for the given data.
    
    Args:
        data (str): Data to encode in QR code
        size (int): Size of QR code boxes
        border (int): Border size
        
    Returns:
        str: Base64 encoded PNG image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"


def generate_certificate_qr(certificate_number, mutation_id=None):
    """
    Generate QR code for certificate verification.
    
    Args:
        certificate_number (str): Certificate number
        mutation_id (int): Optional mutation ID
        
    Returns:
        str: Base64 encoded QR code image
    """
    # Create verification URL
    verification_data = {
        'cert': certificate_number,
        'type': 'mutation'
    }
    
    if mutation_id:
        verification_data['id'] = mutation_id
    
    # Create verification URL (will be accessible without login)
    # Format: domain.com/verify/MUT202500001
    verification_url = f"http://127.0.0.1:5000/verify/{certificate_number}"
    
    return generate_qr_code(verification_url)


def generate_property_qr(ulpin):
    """
    Generate QR code for property verification.
    
    Args:
        ulpin (str): Property ULPIN
        
    Returns:
        str: Base64 encoded QR code image
    """
    verification_url = f"http://127.0.0.1:5000/verify/property/{ulpin}"
    return generate_qr_code(verification_url)
