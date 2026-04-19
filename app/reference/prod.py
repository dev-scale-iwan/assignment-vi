import os

import chromadb

from chonkie import SemanticChunker
from dotenv import load_dotenv
from mistralai.client import Mistral



load_dotenv()

# 1. Extract text from PDF using Mistral OCR API
client = Mistral(api_key=os.getenv("MISTRALAI_API_KEY"))

print("Extracting text from PDF...")

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url", 
        "document_url": "https://zanshin-sailing.com/wp-content/uploads/pdf-files/Cooking/cooking_cookbook_free_stonesoup_ecookbook.pdf"
    }
)

full_content = ""
for page in ocr_response.pages:
    full_content += page.markdown + "\n"
    
print(f"✓ Extracted {len(full_content)} characters from PDF")

# 2. Semantic Chunking with Chonkie
print("Chunking text with Chonkie SemanticChunker...")

chunker = SemanticChunker(chunk_size=512, threshold=0.5)
chunks = chunker.chunk(full_content)
print(f"✓ Created {len(chunks)} chunks")


# 3. Store chunks in ChromaDB
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection(name="pdf_cookie_book")

collection.add(
    documents=[chunk.text for chunk in chunks],
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

# 4. Querying the collection
while True:
    query = input("\nEnter a query to search the PDF content (or 'exit' to quit): ")
    if query.strip().lower() == "exit":
        break
    
    results = collection.query(query_texts=[query], n_results=3)
    
    docs = results['documents']
    assert docs is not None
    
    print(f"\nRelevant chunks:")
    for i, doc in enumerate(docs[0]):
        print(f" [{i+1}] - {doc[:200]}...\n")
