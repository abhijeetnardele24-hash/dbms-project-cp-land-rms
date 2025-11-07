"""
QR Code Generator for Property Certificates
Generates secure QR codes for property verification
"""

import qrcode
import os
from io import BytesIO
import hashlib
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


class QRCodeGenerator:
    """Generate QR codes for property certificates"""
    
    @staticmethod
    def generate_property_qr(property_ulpin, base_url="http://localhost:5000"):
        """
        Generate QR code for property verification
        
        Args:
            property_ulpin: Property ULPIN
            base_url: Base URL of the application
            
        Returns:
            BytesIO object containing QR code image
        """
        try:
            # Create verification URL
            verification_url = f"{base_url}/verify/{property_ulpin}"
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(verification_url)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to BytesIO
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            
            return img_io
        except Exception as e:
            print(f"Error generating QR code: {str(e)}")
            return None
    
    @staticmethod
    def generate_property_qr_with_logo(property_ulpin, logo_path=None, base_url="http://localhost:5000"):
        """
        Generate QR code with embedded logo
        
        Args:
            property_ulpin: Property ULPIN
            logo_path: Path to logo image (optional)
            base_url: Base URL of the application
            
        Returns:
            BytesIO object containing QR code image with logo
        """
        try:
            # Create verification URL
            verification_url = f"{base_url}/verify/{property_ulpin}"
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(verification_url)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            
            # Add logo if provided
            if logo_path and os.path.exists(logo_path):
                logo = Image.open(logo_path)
                
                # Calculate logo size (1/5 of QR code)
                qr_width, qr_height = img.size
                logo_size = qr_width // 5
                
                # Resize logo
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Calculate position (center)
                logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                
                # Paste logo
                img.paste(logo, logo_pos)
            
            # Save to BytesIO
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            
            return img_io
        except Exception as e:
            print(f"Error generating QR code with logo: {str(e)}")
            return None
    
    @staticmethod
    def save_qr_code(property_ulpin, save_dir='static/qr_codes'):
        """
        Generate and save QR code to file
        
        Args:
            property_ulpin: Property ULPIN
            save_dir: Directory to save QR codes
            
        Returns:
            Path to saved QR code file
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(save_dir, exist_ok=True)
            
            # Generate QR code
            qr_io = QRCodeGenerator.generate_property_qr(property_ulpin)
            
            if qr_io:
                # Save to file
                filename = f"{property_ulpin}.png"
                filepath = os.path.join(save_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(qr_io.getvalue())
                
                return filepath
            
            return None
        except Exception as e:
            print(f"Error saving QR code: {str(e)}")
            return None
    
    @staticmethod
    def generate_secure_hash(property_ulpin, timestamp=None):
        """
        Generate secure hash for QR code verification
        
        Args:
            property_ulpin: Property ULPIN
            timestamp: Optional timestamp
            
        Returns:
            Secure hash string
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        data = f"{property_ulpin}:{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()


# Convenience functions
def generate_qr_for_property(property_ulpin):
    """Generate QR code for property"""
    return QRCodeGenerator.generate_property_qr(property_ulpin)

def save_property_qr(property_ulpin):
    """Save QR code to file"""
    return QRCodeGenerator.save_qr_code(property_ulpin)
