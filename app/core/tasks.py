from app.core.celery_app import celery_app
from app.core.extract_pdf import extract_with_mistral, store_extracted_content, update_file_status


@celery_app.task(bind=True, name="extract_pdf_task")
def extract_pdf_task(self, file_id: str, pdf_path: str):
    try:
        # Update status to processing
        update_file_status(file_id, "processing")

        # Extract text from PDF
        extracted_data = extract_with_mistral(pdf_path)

        if extracted_data.get("status") == "success":
            # Store extracted content in ChromaDB
            storage_success = store_extracted_content(file_id, extracted_data)

            if storage_success:
                # Update status to completed
                update_file_status(file_id, "completed", extracted_data)
                return {"status": "success", "file_id": file_id}
            else:
                # Storage failed
                update_file_status(file_id, "storage_failed", extracted_data)
                return {"status": "storage_failed", "file_id": file_id}
        else:
            # Extraction failed
            update_file_status(file_id, "extraction_failed", extracted_data)
            return {"status": "extraction_failed", "file_id": file_id, "error": extracted_data.get("error")}

    except Exception as e:
        # General error
        update_file_status(file_id, "error", {"error": str(e)})
        return {"status": "error", "file_id": file_id, "error": str(e)}