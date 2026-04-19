import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session, select, func
import uuid

from app.schema.file import PDFUploadResponse, FileResponse, FileListResponse
from app.utils.utils import process_pdf_upload
from app.utils.query_params import standard_query_params
from app.models.engine import get_db
from app.models.file import File as FileModel
from app.core.tasks import extract_pdf_task

logger = logging.getLogger(__name__)

pdf_router = APIRouter(prefix="/pdf", tags=["PDF"])


@pdf_router.get("/", response_model=FileListResponse)
async def list_files(
    db: Session = Depends(get_db),
    query_params: dict = Depends(standard_query_params)
) -> FileListResponse:
    try:
        # Set default limit to 100 if not provided
        limit = query_params.get("limit") or 100
        offset = query_params.get("offset") or 0
        
        # Get total count of files
        count_statement = select(func.count()).select_from(FileModel)
        total_count = db.exec(count_statement).one()
        
        # Get paginated files
        statement = select(FileModel).offset(offset).limit(limit)
        files = db.exec(statement).all()
        
        # Calculate current page (1-based)
        page = (offset // limit) + 1 if limit > 0 else 1
        
        return FileListResponse(
            files=files,
            count=total_count,
            page=page,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve files: {str(e)}"
        )


@pdf_router.get("/{file_id}", response_model=FileResponse)
async def get_file_detail(
    file_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> FileResponse:
    try:
        statement = select(FileModel).where(FileModel.id == file_id)
        file = db.exec(statement).first()
        
        if not file:
            raise HTTPException(
                status_code=404,
                detail=f"File with ID {file_id} not found"
            )
        
        return file
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve file: {str(e)}"
        )


@pdf_router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> PDFUploadResponse:
    """
    Upload a PDF file and store it in the uploads folder and database.
    Triggers PDF text extraction as a background task.
    
    Args:
        file: PDF file to upload
        db: Database session
        
    Returns:
        PDFUploadResponse with filename, file_size, file_id and success message
        
    Raises:
        HTTPException: If file validation or upload fails
    """
    try:
        result = process_pdf_upload(file, db, path="pdf")
        
        # Trigger PDF extraction task asynchronously on the pdf_extraction queue
        task = extract_pdf_task.apply_async(
            args=[result["file_id"], result["file_path"]],
            queue="pdf_extraction"
        )
        logger.info(f"📤 Task queued - File: {result['file_id']}, Task ID: {task.id}")
        
        return PDFUploadResponse(
            filename=result["filename"],
            file_size=result["file_size"],
            file_id=result["file_id"],
            message=f"File uploaded successfully. PDF extraction queued as task {task.id}."
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
