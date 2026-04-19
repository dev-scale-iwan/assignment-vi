import os
import base64
from typing import Dict, Any

import chromadb
from chonkie import SemanticChunker
from dotenv import load_dotenv
from mistralai.client import Mistral

from app.models.engine import engine
from app.models.file import File as FileModel
from sqlmodel import Session, select

load_dotenv()

# Initialize Mistral client
client = Mistral(api_key=os.getenv("MISTRALAI_API_KEY"))


def extract_with_mistral(pdf_path: str) -> Dict[str, Any]:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        print(f"Extracting text from PDF: {pdf_path}")

        # Read PDF file and encode as base64
        with open(pdf_path, "rb") as f:
            pdf_data = base64.b64encode(f.read()).decode('utf-8')

        # Process with Mistral OCR
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_base64",
                "document_base64": pdf_data
            }
        )

        # Extract full content from all pages and collect page information
        full_content = ""
        pages_info = []
        for i, page in enumerate(ocr_response.pages):
            full_content += page.markdown + "\n"
            pages_info.append({
                "page_number": i + 1,  # 1-based page numbering
                "id": f"page_{i + 1}",
                "content": page.markdown,
                "document": pdf_path
            })

        print(f"✓ Extracted {len(full_content)} characters from PDF")

        # Perform semantic chunking
        print("Chunking text with Chonkie SemanticChunker...")
        chunker = SemanticChunker(chunk_size=512, threshold=0.5)
        chunks = chunker.chunk(full_content)
        print(f"✓ Created {len(chunks)} chunks")

        return {
            "content": full_content,
            "chunks": [chunk.text for chunk in chunks],
            "pages": pages_info,
            "num_pages": len(ocr_response.pages),
            "num_chunks": len(chunks),
            "status": "success"
        }

    except Exception as e:
        print(f"✗ Error extracting PDF: {str(e)}")
        return {
            "error": str(e),
            "status": "failed"
        }


def store_extracted_content(file_id: str, extracted_data: Dict[str, Any]) -> bool:
    try:
        if extracted_data.get("status") != "success":
            print(f"Skipping storage for failed extraction: {file_id}")
            return False

        # Initialize ChromaDB client
        chroma_client = chromadb.PersistentClient(path="./chroma_db")

        # Store chunks in collection
        chunks_collection = chroma_client.get_or_create_collection(name="pdf_chunks")

        # Prepare chunk documents and metadata
        chunk_documents = extracted_data["chunks"]
        chunk_metadatas = [{
            "file_id": file_id,
            "chunk_index": i,
            "total_chunks": len(chunk_documents),
            "type": "chunk"
        } for i in range(len(chunk_documents))]

        # Generate IDs for chunks
        chunk_ids = [f"{file_id}_chunk_{i}" for i in range(len(chunk_documents))]

        # Add chunks to ChromaDB
        chunks_collection.add(
            documents=chunk_documents,
            metadatas=chunk_metadatas,
            ids=chunk_ids
        )

        # Store pages in separate collection
        pages_collection = chroma_client.get_or_create_collection(name="pdf_pages")

        # Prepare page documents and metadata
        page_documents = [page["content"] for page in extracted_data["pages"]]
        page_metadatas = [{
            "file_id": file_id,
            "page_number": page["page_number"],
            "page_id": page["id"],
            "document": page["document"],
            "type": "page"
        } for page in extracted_data["pages"]]

        # Generate IDs for pages
        page_ids = [f"{file_id}_page_{page['page_number']}" for page in extracted_data["pages"]]

        # Add pages to ChromaDB
        pages_collection.add(
            documents=page_documents,
            metadatas=page_metadatas,
            ids=page_ids
        )

        print(f"✓ Stored {len(chunk_documents)} chunks and {len(page_documents)} pages in ChromaDB for file {file_id}")
        return True

    except Exception as e:
        print(f"✗ Error storing content in ChromaDB: {str(e)}")
        return False


def update_file_status(file_id: str, status: str, extracted_data: Dict[str, Any] = None) -> bool:
    try:
        with Session(engine) as session:
            # Get file record
            statement = select(FileModel).where(FileModel.id == file_id)
            file_record = session.exec(statement).first()

            if not file_record:
                print(f"File not found: {file_id}")
                return False

            # Update status in database
            file_record.status = status
            session.add(file_record)
            session.commit()

            print(f"✓ Updated status for file {file_id}: {status}")

            if extracted_data and extracted_data.get("status") == "success":
                print(f"  - Pages: {extracted_data.get('num_pages', 0)}")
                print(f"  - Chunks: {extracted_data.get('num_chunks', 0)}")
                print(f"  - Characters: {len(extracted_data.get('content', ''))}")
                if "pages" in extracted_data:
                    print(f"  - Page details available: {len(extracted_data['pages'])} pages")

            return True

    except Exception as e:
        print(f"✗ Error updating file status: {str(e)}")
        return False