from pydantic import BaseModel


class PDFUploadResponse(BaseModel):
    """Response schema for PDF upload endpoint"""
    filename: str
    file_size: int
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "document.pdf",
                "file_size": 102400,
                "message": "File uploaded successfully"
            }
        }
