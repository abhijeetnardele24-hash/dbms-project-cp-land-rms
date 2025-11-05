"""
File handling utility functions for document uploads.
"""

import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """
    Check if file extension is allowed.
    
    Args:
        filename: Name of the file
    
    Returns:
        bool: True if file extension is allowed
    """
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file, subfolder='documents'):
    """
    Save uploaded file to the upload folder with a unique name.
    
    Args:
        file: FileStorage object from request.files
        subfolder: Subfolder within UPLOAD_FOLDER (e.g., 'documents', 'images')
    
    Returns:
        tuple: (success: bool, file_path: str or error_message: str)
    """
    if not file:
        return False, 'No file provided'
    
    if file.filename == '':
        return False, 'No file selected'
    
    if not allowed_file(file.filename):
        return False, 'File type not allowed. Allowed types: PDF, JPG, JPEG, PNG'
    
    try:
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{extension}"
        
        # Create subfolder if it doesn't exist
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        # Return relative path for database storage
        relative_path = os.path.join(subfolder, unique_filename)
        return True, relative_path
        
    except Exception as e:
        current_app.logger.error(f'Error saving file: {str(e)}')
        return False, f'Error saving file: {str(e)}'


def get_file_size(file):
    """
    Get file size in bytes.
    
    Args:
        file: FileStorage object
    
    Returns:
        int: File size in bytes
    """
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size


def delete_file(file_path):
    """
    Delete a file from the upload folder.
    
    Args:
        file_path: Relative path to the file
    
    Returns:
        bool: True if file was deleted successfully
    """
    try:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    except Exception as e:
        current_app.logger.error(f'Error deleting file: {str(e)}')
        return False
