import os
import shutil
import time
import re
from fastapi import UploadFile
from sqlmodel import Session
from app.models.file import File

UPLOAD_FOLDER = "uploads"


def generate_filename(original_filename: str) -> str:
    # Get unix timestamp
    timestamp = int(time.time())
    
    # Split filename and extension
    name_part, ext = os.path.splitext(original_filename)
    
    # Convert to lowercase and replace spaces/non-word chars with dashes
    clean_name = re.sub(r'[^\w\s-]', '', name_part)  # Remove special chars except spaces and dashes
    clean_name = re.sub(r'[-\s]+', '-', clean_name.lower())  # Replace spaces/dashes with single dash, lowercase
    
    # Remove leading/trailing dashes
    clean_name = clean_name.strip('-')
    
    # Combine with timestamp
    new_filename = f"{clean_name}-{timestamp}{ext}"
    
    return new_filename


def ensure_upload_folder(folder_path: str = "uploads") -> str:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def process_pdf_upload(file: UploadFile, db: Session, path: str = "pdf") -> dict:
    # Validate file is PDF
    if not file.filename or not file.filename.endswith(".pdf"):
        raise ValueError("Only PDF files are allowed")
    
    # Generate new filename
    new_filename = generate_filename(file.filename)
    
    # Full path to save the file
    path_upload = os.path.join(UPLOAD_FOLDER, path)
    # Ensure upload folder exists
    ensure_upload_folder(path_upload)
    
    # Save file with new filename
    file_path = os.path.join(path_upload, new_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create file record in database with new filename
        file_record = File(
            nama=new_filename,  # Store the new filename
            path=file_path,
            size=file_size,
            type="application/pdf",
            status="uploaded"  # Set initial status
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        
        return {
            "filename": new_filename,  # Return the new filename
            "file_size": file_size,
            "file_id": str(file_record.id),
            "file_path": file_path  # Add file path for Celery task
        }
    except Exception as e:
        db.rollback()
        raise IOError(f"Failed to save file: {str(e)}")
