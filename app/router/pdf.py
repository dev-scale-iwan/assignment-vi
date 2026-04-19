import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session, select, func

from app.schema.file import PDFUploadResponse, FileResponse, FileListResponse
from app.utils.utils import process_pdf_upload
from app.utils.query_params import standard_query_params
from app.models.engine import get_db
from app.models.file import File as FileModel

pdf_router = APIRouter(prefix="/pdf", tags=["PDF"])


@pdf_router.get("/", response_model=FileListResponse)
async def list_files(
    db: Session = Depends(get_db),
    query_params: dict = Depends(standard_query_params)
) -> FileListResponse:
    """
    Get a paginated list of all uploaded files from the database.
    
    Args:
        db: Database session
        query_params: Query parameters (limit, offset)
        
    Returns:
        FileListResponse with files list and pagination metadata
    """
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
