from pydantic import BaseModel
from typing import Optional
import uuid


class FileBase(BaseModel):
    """Base schema for file operations"""
    nama: str
    path: str
    size: float
    type: str


class FileCreate(FileBase):
    """Schema for creating a file record"""
    pass


class FileResponse(FileBase):
    """Schema for file response"""
    id: uuid.UUID

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "nama": "document.pdf",
                "path": "uploads/pdf/document.pdf",
                "size": 102400,
                "type": "application/pdf"
            }
        }


class PDFUploadResponse(BaseModel):
    """Response schema for PDF upload endpoint"""
    filename: str
    file_size: int
    message: str
    file_id: Optional[uuid.UUID] = None

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "document.pdf",
                "file_size": 102400,
                "message": "File uploaded successfully",
                "file_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
