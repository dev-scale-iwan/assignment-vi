import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schema.pdf import PDFUploadResponse
from app.utils.utils import process_pdf_upload

pdf_router = APIRouter(prefix="/pdf", tags=["PDF"])

@pdf_router.post("/pdf/upload", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> PDFUploadResponse:
    try:
        result = process_pdf_upload(file, '/pdf')
        return PDFUploadResponse(
            filename=result["filename"],
            file_size=result["file_size"],
            message="File uploaded successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except IOError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
