import chromadb
import sys
import os
import shutil

print("Initializing documents...")

documents = [
    "Pyhton is a programming language that is widely used for web development, data analysis, artificial intelligence, and scientific computing. It is known for its simplicity and readability, making it a popular choice for beginners and experienced developers alike.",
    "The MistralAI OCR API is a powerful tool that allows you to extract text from images. It can process documents, tables, and even images embedded within the document. In this example, we will use the MistralAI OCR API to process a PDF document from arXiv and save the extracted text to a Markdown file. We will also save any images found in the document as separate files. To get started, make sure you have your MistralAI API key set up in your environment variables.",
    "The Chonkie library provides various chunking strategies to break down text into manageable pieces. The TokenChunker splits text based on a specified number of tokens, while the SentenceChunker breaks text into sentences. The RecursiveChunker recursively divides text until it meets the desired chunk size, and the SemanticChunker groups text based on semantic similarity. These chunking techniques are essential for processing large documents and preparing them for tasks like summarization, question answering, or information retrieval.",
    "In this example, we will demonstrate how to use the RecursiveChunker from the Chonkie library to break down a sample text into smaller chunks. The RecursiveChunker will recursively divide the text until it meets the specified chunk size, ensuring that the chunks are coherent and meaningful. This approach is particularly useful for processing long documents or articles, allowing us to work with manageable pieces of text for various natural language processing tasks.",
    "RAG (Retrieval-Augmented Generation) is a powerful technique that combines retrieval-based methods with generative models to enhance the quality and relevance of generated content. In a RAG system, a retriever component is used to fetch relevant information from a knowledge base or document collection, which is then fed into a generative model to produce coherent and contextually appropriate responses. This approach allows for more accurate and informative outputs, as the generative model can leverage the retrieved information to generate responses that are grounded in real-world data. RAG has been successfully applied in various applications, including question answering, summarization, and conversational agents."
]

print(f"Loaded {len(documents)} documents")

metadatas = [
    {"category": "programming", "level": "beginner"},
    {"category": "AI", "level": "intermediate"},
    {"category": "NLP", "level": "advanced"},
    {"category": "Data Science", "level": "intermediate"},
    {"category": "AI", "level": "beginner"}
]

def main():
    try:
        # Clean up any locked database
        chroma_path = "./chroma_db"
        if os.path.exists(chroma_path):
            print(f"Removing existing {chroma_path} directory...")
            shutil.rmtree(chroma_path, ignore_errors=True)
            print("✓ Cleaned up")
        
        print("Connecting to ChromaDB (in-memory mode)...")
        sys.stdout.flush()
        
        # Use in-memory client to avoid locking issues
        client = chromadb.EphemeralClient()
        print("✓ ChromaDB client initialized")
        
        print("Creating collection...")
        sys.stdout.flush()
        
        collection = client.create_collection(name="docs")
        print("✓ Collection created")
        
        print("Adding documents to collection...")
        collection.add(documents=documents, metadatas=metadatas, ids=[str(i) for i in range(len(documents))])
        
        print("✓ All documents added to ChromaDB")
        
        while True:
            print("\n--- Options ---")
            print("1. Search documents")
            print("2. Delete specific document (by ID)")
            print("3. Delete all documents")
            print("4. Delete collection")
            print("5. Exit")
            
            choice = input("Select option (1-5): ").strip()
            
            if choice == "1":
                query = input("Enter a query to search the documents: ")
                results = collection.query(query_texts=[query], n_results=3, where={"category": "AI"})
                docs = results['documents']
                
                metas = results['metadatas']
                
                assert docs is not None
                assert metas is not None
                    
                print("\nRelevant documents (filter by category 'AI'):")
                for doc, meta in zip(docs[0], metas[0]):
                    print(f"  - [{meta}] {doc})")
            elif choice == "2":
                doc_id = input("Enter document ID to delete (0-4): ").strip()
                try:
                    collection.delete(ids=[doc_id])
                    print(f"✓ Document {doc_id} deleted")
                except Exception as e:
                    print(f"Error deleting document: {e}")
                    
            elif choice == "3":
                doc_ids = [str(i) for i in range(len(documents))]
                collection.delete(ids=doc_ids)
                print(f"✓ All {len(doc_ids)} documents deleted")
                
            elif choice == "4":
                client.delete_collection(name="docs")
                print("✓ Collection deleted")
                collection = client.create_collection(name="docs")
                print("✓ New collection created")
                
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid option")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()