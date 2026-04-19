import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session

from app.schema.file import PDFUploadResponse
from app.utils.utils import process_pdf_upload
from app.models.engine import get_db

pdf_router = APIRouter(prefix="/pdf", tags=["PDF"])


@pdf_router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> PDFUploadResponse:
    try:
        result = process_pdf_upload(file, db, path="pdf")
        return PDFUploadResponse(
            filename=result["filename"],
            file_size=result["file_size"],
            file_id=result["file_id"],
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
