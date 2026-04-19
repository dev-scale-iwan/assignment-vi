from chonkie import TokenChunker, SentenceChunker, SemanticChunker, RecursiveChunker

text = (
    "The MistralAI OCR API is a powerful tool that allows you to extract text from images. "
    "It can process documents, tables, and even images embedded within the document. "
    "In this example, we will use the MistralAI OCR API to process a PDF document from arXiv and save the extracted text to a Markdown file. "
    "We will also save any images found in the document as separate files. "
    "To get started, make sure you have your MistralAI API key set up in your environment variables. "
)

# print("==== TOKEN CHUNKER EXAMPLE ====")
# chunker = TokenChunker(chunk_size=100, chunk_overlap=20)
# for i, chunk in enumerate(chunker.chunk(text)):
#     print(f"Chunk {i}: {chunk.text}\n")

# print("==== SENTENCE CHUNKER EXAMPLE ====")
# chunker = SentenceChunker(chunk_size=30, chunk_overlap=20)
# for i, chunk in enumerate(chunker.chunk(text)):
#     print(f"Chunk {i}: {chunk.text}\n")


print("==== RECURSIVE CHUNKER EXAMPLE ====")
chunker = RecursiveChunker(chunk_size=30)
for i, chunk in enumerate(chunker.chunk(text)):
    print(f"Chunk {i}: {chunk.text}\n")


# print("==== SEMANTIC CHUNKER EXAMPLE ====")
# chunker = SemanticChunker(chunk_size=50, threshold=0.5)
# for i, chunk in enumerate(chunker.chunk(text)):
#     print(f" Chunk {i}: {chunk.text}\n")
