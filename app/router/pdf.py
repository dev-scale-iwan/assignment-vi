import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schema.pdf import PDFUploadResponse
from app.utils.utils import ensure_upload_folder

pdf_router = APIRouter(prefix="/pdf", tags=["PDF"])

UPLOAD_FOLDER = "uploads"


@pdf_router.post("/pdf/upload", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> PDFUploadResponse:
    """
    Upload a PDF file and store it in the /uploads folder
    
    Args:
        file: PDF file to upload
        
    Returns:
        PDFUploadResponse with filename, file size and success message
        
    Raises:
        HTTPException: If file is not a PDF
    """
    # Validate file is PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Ensure upload folder exists
    ensure_upload_folder(UPLOAD_FOLDER)
    
    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        return PDFUploadResponse(
            filename=file.filename,
            file_size=file_size,
            message="File uploaded successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )
