import os
import shutil
from fastapi import UploadFile

UPLOAD_FOLDER = "uploads"

def ensure_upload_folder(folder_path: str = "uploads") -> str:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def process_pdf_upload(file: UploadFile, path: str = "uploads") -> dict:
    # Validate file is PDF
    if not file.filename or not file.filename.endswith(".pdf"):
        raise ValueError("Only PDF files are allowed")
    
    # Full path to save the file
    path_upload = UPLOAD_FOLDER + "/" + path
    # Ensure upload folder exists
    ensure_upload_folder(path_upload)
    
    # Save file
    file_path = os.path.join(path_upload, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        return {
            "filename": file.filename,
            "file_size": file_size
        }
    except Exception as e:
        raise IOError(f"Failed to save file: {str(e)}")
