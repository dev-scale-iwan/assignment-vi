from typing import Any

from fastapi import APIRouter, HTTPException
import chromadb

search_router = APIRouter(prefix="/search", tags=["Search"])


@search_router.get("/{q}")
async def search_pdf_content(q: str, n_results: int = 3) -> Any:
    """Search stored PDF content in ChromaDB by query text."""
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        collection = chroma_client.get_or_create_collection(name="pdf_chunks")

        results = collection.query(query_texts=[q], n_results=n_results)
        documents = results.get("documents")
        metadatas = results.get("metadatas")
        ids = results.get("ids")

        if documents is None:
            raise HTTPException(status_code=404, detail="No search results returned")

        return {
            "query": q,
            "n_results": n_results,
            "documents": documents[0],
            "metadatas": metadatas[0] if metadatas else None,
            "ids": ids[0] if ids else None,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
