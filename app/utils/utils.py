import os
import shutil
from fastapi import UploadFile
from sqlmodel import Session
from app.models.file import File

UPLOAD_FOLDER = "uploads"


def ensure_upload_folder(folder_path: str = "uploads") -> str:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def process_pdf_upload(file: UploadFile, db: Session, path: str = "pdf") -> dict:
    # Validate file is PDF
    if not file.filename or not file.filename.endswith(".pdf"):
        raise ValueError("Only PDF files are allowed")
    
    # Full path to save the file
    path_upload = os.path.join(UPLOAD_FOLDER, path)
    # Ensure upload folder exists
    ensure_upload_folder(path_upload)
    
    # Save file
    file_path = os.path.join(path_upload, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create file record in database
        file_record = File(
            nama=file.filename,
            path=file_path,
            size=file_size,
            type="application/pdf"
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        
        return {
            "filename": file.filename,
            "file_size": file_size,
            "file_id": str(file_record.id)
        }
    except Exception as e:
        db.rollback()
        raise IOError(f"Failed to save file: {str(e)}")
