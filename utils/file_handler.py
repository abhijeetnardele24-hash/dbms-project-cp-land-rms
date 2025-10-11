"""
Secure file upload handling for Government Property Management Portal
"""

import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import mimetypes
from flask import current_app, flash

# Optional PIL import for image processing
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class FileUploadHandler:
    """Handles secure file uploads with validation"""
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        'documents': {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'},
        'images': {'jpg', 'jpeg', 'png', 'gif'},
        'all': {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'txt'}
    }
    
    # Maximum file sizes (in bytes)
    MAX_FILE_SIZE = {
        'documents': 10 * 1024 * 1024,  # 10MB
        'images': 5 * 1024 * 1024,      # 5MB
    }
    
    @staticmethod
    def allowed_file(filename, file_type='all'):
        """Check if file extension is allowed"""
        if not filename:
            return False
        
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return extension in FileUploadHandler.ALLOWED_EXTENSIONS.get(file_type, set())
    
    @staticmethod
    def validate_file_size(file, file_type='documents'):
        """Validate file size"""
        if not file:
            return False
        
        # Get file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        max_size = FileUploadHandler.MAX_FILE_SIZE.get(file_type, 10 * 1024 * 1024)
        return file_size <= max_size
    
    @staticmethod
    def validate_file_content(file):
        """Validate file content using MIME type"""
        if not file:
            return False
        
        # Check MIME type
        mime_type, _ = mimetypes.guess_type(file.filename)
        allowed_mimes = {
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg',
            'image/png',
            'image/gif',
            'text/plain'
        }
        
        return mime_type in allowed_mimes
    
    @staticmethod
    def generate_unique_filename(original_filename):
        """Generate unique filename to prevent conflicts"""
        if not original_filename:
            return None
        
        # Get file extension
        extension = ''
        if '.' in original_filename:
            extension = '.' + original_filename.rsplit('.', 1)[1].lower()
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{extension}"
    
    @staticmethod
    def save_file(file, upload_folder='uploads', file_type='documents'):
        """
        Save uploaded file securely
        Returns: (success, filename, error_message)
        """
        if not file or file.filename == '':
            return False, None, "No file selected"
        
        # Validate file extension
        if not FileUploadHandler.allowed_file(file.filename, file_type):
            return False, None, f"File type not allowed. Allowed: {', '.join(FileUploadHandler.ALLOWED_EXTENSIONS[file_type])}"
        
        # Validate file size
        if not FileUploadHandler.validate_file_size(file, file_type):
            max_size_mb = FileUploadHandler.MAX_FILE_SIZE[file_type] / (1024 * 1024)
            return False, None, f"File too large. Maximum size: {max_size_mb}MB"
        
        # Validate file content
        if not FileUploadHandler.validate_file_content(file):
            return False, None, "Invalid file content"
        
        try:
            # Generate unique filename
            unique_filename = FileUploadHandler.generate_unique_filename(file.filename)
            
            # Create upload directory if it doesn't exist
            upload_path = os.path.join(current_app.static_folder, upload_folder)
            os.makedirs(upload_path, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_path, unique_filename)
            file.save(file_path)
            
            # If it's an image, create thumbnail
            if file_type == 'images':
                FileUploadHandler.create_thumbnail(file_path)
            
            return True, unique_filename, None
            
        except Exception as e:
            return False, None, f"Error saving file: {str(e)}"
    
    @staticmethod
    def create_thumbnail(image_path, size=(150, 150)):
        """Create thumbnail for images"""
        if not PIL_AVAILABLE:
            print("PIL not available, skipping thumbnail creation")
            return
            
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Generate thumbnail filename
                base_name = os.path.splitext(image_path)[0]
                thumb_path = f"{base_name}_thumb.jpg"
                
                # Save thumbnail
                img.save(thumb_path, "JPEG", quality=85)
                
        except Exception as e:
            print(f"Error creating thumbnail: {str(e)}")
    
    @staticmethod
    def delete_file(filename, upload_folder='uploads'):
        """Delete uploaded file and its thumbnail"""
        try:
            file_path = os.path.join(current_app.static_folder, upload_folder, filename)
            
            # Delete main file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Delete thumbnail if exists
            base_name = os.path.splitext(file_path)[0]
            thumb_path = f"{base_name}_thumb.jpg"
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
                
            return True
            
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
            return False
    
    @staticmethod
    def get_file_url(filename, upload_folder='uploads'):
        """Get URL for uploaded file"""
        if not filename:
            return None
        return f"/static/{upload_folder}/{filename}"

# Global file handler instance
file_handler = FileUploadHandler()
