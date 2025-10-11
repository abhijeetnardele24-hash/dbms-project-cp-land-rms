"""
Encryption utilities for Government Property Management Portal
Handles Aadhaar number encryption using Fernet symmetric encryption
"""

from cryptography.fernet import Fernet
import os
import base64
from typing import Optional

class AadhaarEncryption:
    """Handles Aadhaar number encryption and decryption"""
    
    def __init__(self):
        # Generate or load encryption key
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self) -> bytes:
        """Get existing key or create new one"""
        key_file = 'aadhaar_key.key'
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_aadhaar(self, aadhaar_number: str) -> str:
        """
        Encrypt Aadhaar number
        Args:
            aadhaar_number: 12-digit Aadhaar number
        Returns:
            Encrypted string (base64 encoded)
        """
        if not aadhaar_number:
            return ""
        
        # Remove spaces and validate format
        aadhaar_clean = aadhaar_number.replace(" ", "").replace("-", "")
        
        if not aadhaar_clean.isdigit() or len(aadhaar_clean) != 12:
            raise ValueError("Invalid Aadhaar number format")
        
        # Encrypt
        encrypted_bytes = self.cipher.encrypt(aadhaar_clean.encode())
        return base64.urlsafe_b64encode(encrypted_bytes).decode()
    
    def decrypt_aadhaar(self, encrypted_aadhaar: str) -> str:
        """
        Decrypt Aadhaar number
        Args:
            encrypted_aadhaar: Encrypted Aadhaar string
        Returns:
            Decrypted 12-digit Aadhaar number
        """
        if not encrypted_aadhaar:
            return ""
        
        try:
            # Decode and decrypt
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_aadhaar.encode())
            decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
            return decrypted_bytes.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt Aadhaar: {str(e)}")
    
    def mask_aadhaar(self, aadhaar_number: str) -> str:
        """
        Mask Aadhaar number for display (show only last 4 digits)
        Args:
            aadhaar_number: 12-digit Aadhaar number
        Returns:
            Masked Aadhaar (XXXX-XXXX-1234)
        """
        if not aadhaar_number or len(aadhaar_number) < 4:
            return "XXXX-XXXX-XXXX"
        
        clean_aadhaar = aadhaar_number.replace(" ", "").replace("-", "")
        if len(clean_aadhaar) == 12:
            return f"XXXX-XXXX-{clean_aadhaar[-4:]}"
        return "XXXX-XXXX-XXXX"

# Global instance
aadhaar_crypto = AadhaarEncryption()
