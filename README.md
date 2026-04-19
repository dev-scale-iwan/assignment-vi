# Assignment VI - RAG System with PDF Upload

A FastAPI-based application that supports PDF file uploads and implements RAG (Retrieval-Augmented Generation) capabilities with ChromaDB.

## Prerequisites

- Python 3.13 or higher
- `uv` package manager (optional but recommended)

## Installation & Setup

### 1. Activate Virtual Environment

```bash
source .venv/bin/activate
```

Or on Windows:
```bash
.venv\Scripts\activate
```

### 2. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
pip install -r requirements.txt
```

**New Dependencies Added:**
- `celery` - Background task processing
- `redis` - Message broker for Celery
- `mistralai` - OCR API client
- `chonkie` - Semantic text chunking
- `chromadb` - Vector database for RAG

### 3. Initialize Database & Run Migrations

First, ensure you're in the virtual environment, then run Alembic migrations:

```bash
source .venv/bin/activate
alembic upgrade head
```

This will:
- Create the database file (`iwansusanto.db`)
- Apply all pending migrations
- Create the `file` table and other required database schemas

**Note**: If this is the first time setting up the project and migrations haven't been generated yet, follow the Database Migrations section below first.

### 3. Start Redis

Ensure Redis is installed and running before starting Celery:

```bash
redis-server
```

### 4. Start Celery Worker (for PDF Processing)

Using Makefile:

```bash
make celery
```

Or manually:

```bash
celery -A app.core.celery_app worker --loglevel=info --queues=pdf_extraction
```

This starts the background worker that processes PDF extraction tasks asynchronously.

## Running the Application

### Using Makefile (Recommended)

```bash
make dev
```

This runs the development server with auto-reload enabled.

### Manual Start

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or using Python module syntax:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will start at:
- **API Base URL**: `http://localhost:8000`
- **API Documentation (Scalar)**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

## Model Context Protocol (MCP)

This project integrates with the [Model Context Protocol](https://modelcontextprotocol.io/), allowing AI agents (like Claude Desktop or other MCP-compatible clients) to interact with your PDF RAG system directly.

### Running the MCP Server

The MCP server uses `streamable-http` transport and can be started using the following commands:

Using Makefile:
```bash
make mcp
```

For development and debugging with the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):
```bash
make mcp-dev
```

### Available MCP Tools

AI agents can use the following tools once connected to the MCP server:

- **`get_root`**: Get the root response and health status of the API.
- **`list_files`**: List all uploaded PDF files with pagination.
- **`get_file_detail`**: Get detailed metadata for a specific PDF using its ID.
- **`search_pdf`**: Search for content across all uploaded PDFs using vector search.
- **`upload_pdf`**: Upload a PDF file by providing its local file path.

### Available Endpoints

#### File Status Values

The `status` field in the file table tracks the PDF processing state:

- `uploaded` - File uploaded successfully, waiting for processing
- `processing` - PDF text extraction in progress
- `completed` - PDF extraction and storage completed successfully
- `extraction_failed` - PDF text extraction failed (OCR error)
- `storage_failed` - Text extraction succeeded but ChromaDB storage failed
- `error` - General processing error

#### Health Check
- **GET** `/health` - API health status
  - Response: `{"status": "ok"}`

#### Root
- **GET** `/` - API information
  - Response: Available endpoints and descriptions

## API Usage Examples

### List Files with Pagination

```bash
# Get first 100 files (default)
curl -X GET "http://localhost:8000/pdf/"

# Get 50 files
curl -X GET "http://localhost:8000/pdf/?limit=50"

# Skip first 10 files, get next 100
curl -X GET "http://localhost:8000/pdf/?offset=10"

# Get 20 files starting from the 41st file
curl -X GET "http://localhost:8000/pdf/?limit=20&offset=40"
```

Response:
```json
{
  "files": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "nama": "document.pdf",
      "path": "uploads/pdf/document.pdf",
      "size": 102400,
      "type": "application/pdf"
    }
  ],
  "count": 150,
  "page": 1,
  "limit": 100,
  "offset": 0
}
```

### Get File Details

```bash
curl -X GET "http://localhost:8000/pdf/550e8400-e29b-41d4-a716-446655440000"
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "nama": "document.pdf",
  "path": "uploads/pdf/document.pdf",
  "size": 102400,
  "type": "application/pdf"
}
```

Error Response (404):
```json
{
  "detail": "File with ID 550e8400-e29b-41d4-a716-446655440000 not found"
}
```

### Upload a PDF File

```bash
curl -X POST "http://localhost:8000/pdf/upload" \
  -F "file=@document.pdf"
```

Response:
```json
{
  "filename": "document-1640995200.pdf",
  "file_size": 102400,
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "File uploaded successfully. PDF extraction started in background."
}
```

**Note**: Files are automatically renamed to format: `lowercase-spaces-to-dashes-unix-timestamp.pdf`. For example:
- `"My Document.pdf"` → `"my-document-1640995200.pdf"`
- `"Report 2024.pdf"` → `"report-2024-1640995200.pdf"`

## Project Structure

```
assignment-vi/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── schema/
│   │   ├── pdf.py          # PDF-related schemas
│   │   └── file.py         # File model schemas
│   ├── router/
│   │   └── pdf.py          # PDF upload routes
│   ├── utils/
│   │   └── utils.py        # Utility functions
│   ├── models/             # SQLModel database models
│   │   ├── file.py         # File model with SQLite table
│   │   └── engine.py       # Database engine and session
│   └── core/               # Configuration and settings
├── alembic/                # Database migrations
│   ├── versions/           # Migration scripts
│   ├── env.py              # Alembic environment configuration
│   └── alembic.ini         # Alembic configuration
├── uploads/                # Uploaded PDF files (auto-created)
│   └── pdf/                # Subdirectory for PDF uploads
├── iwansusanto.db          # SQLite database file (auto-created)
├── pyproject.toml          # Project dependencies
├── .gitignore              # Git ignore rules
├── Makefile                # Development commands
└── README.md               # This file
```

## Database Migrations

This project uses **Alembic** for database schema management with SQLModel.

### Initial Setup (First Time Only)

If migrations have not been generated yet, create the initial migration:

```bash
alembic revision --autogenerate -m "Initial migration"
```

This command:
- Detects all SQLModel models in `app/models/`
- Automatically generates migration script in `alembic/versions/`
- Prepares the schema changes for application

Then apply the migration:

```bash
alembic upgrade head
```

### Create a New Migration

After modifying any model in `app/models/`, generate a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Examples:
```bash
alembic revision --autogenerate -m "Add user authentication table"
alembic revision --autogenerate -m "Add timestamp columns to file model"
```

### Apply Pending Migrations

Apply all pending migrations to your database:

```bash
alembic upgrade head
```

### View Current Migration Status

See which migrations have been applied:

```bash
alembic current
```

### View Migration History

View all migrations and their status:

```bash
alembic history
```

### Downgrade to Previous Migration

Rollback to the previous migration:

```bash
alembic downgrade -1
```

Or rollback multiple steps:

```bash
alembic downgrade -3
```

### Downgrade to Specific Migration

Rollback to a specific migration by ID:

```bash
alembic downgrade <migration_id>
```

### Migration Best Practices

1. **Always review generated migrations** before applying them
2. **Create descriptive migration messages** for clarity
3. **Test migrations in development** before production
4. **Commit migration files** to version control
5. **Run `alembic upgrade head`** after pulling latest code

## Makefile Commands

The project includes a `Makefile` for common development tasks:

```bash
make dev        # Start development server with auto-reload on port 8000
make celery     # Start Celery worker for background PDF processing
make mcp        # Start the MCP server
make mcp-dev    # Start the MCP server in development mode with inspector
```

To view all available commands:
```bash
make help
```

### PDF Processing Pipeline

When you upload a PDF:

1. **File Upload**: PDF saved to disk, metadata stored in database with status "uploaded"
2. **Background Task**: Celery worker processes PDF with Mistral OCR API
3. **Text Extraction**: Full text extracted from all pages with page-level metadata
4. **Semantic Chunking**: Content split into meaningful chunks using Chonkie
5. **Vector Storage**: Both chunks and individual pages stored in ChromaDB collections:
   - `pdf_chunks` - Semantically chunked text for RAG retrieval
   - `pdf_pages` - Individual page content for page-specific queries
6. **Status Update**: File status updated to "completed" or appropriate error status

### Data Structure

The extraction process returns structured data including:

- **Full content**: Complete extracted text
- **Pages array**: Individual page information with:
  - `page_number`: 1-based page numbering
  - `id`: Unique page identifier
  - `content`: Page markdown content
  - `document`: Source PDF path
- **Chunks array**: Semantically chunked text pieces
- **Metadata**: Page count, chunk count, processing status

### Requirements

- **Redis** (for Celery broker): Install Redis and ensure it's running
- **Celery Worker**: Must be running to process PDF extraction tasks

### Environment Variables

Add to your `.env` file:

```bash
# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Mistral AI API
MISTRALAI_API_KEY=your_mistral_api_key_here

# MCP Configuration
MCP_PORT=8001
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'sqlmodel'`

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate
uv sync
```

### Issue: `alembic upgrade head` fails

**Solution**: Make sure the virtual environment is activated before running Alembic:
```bash
source .venv/bin/activate
alembic upgrade head
```

### Issue: Database tables not created after migration

**Solution**: Verify migration files exist and were applied:
```bash
# Check migration history
alembic history

# Check current revision
alembic current

# Apply migrations
alembic upgrade head
```

### Issue: Migration file shows empty (no changes detected)

**Solution**: Ensure all models are imported in `alembic/env.py`:
```python
from app.models.file import File
```

Then regenerate migration:
```bash
alembic revision --autogenerate -m "Description"
```

### Issue: Need to rollback changes

**Solution**: Use downgrade command:
```bash
# Rollback one migration
alembic downgrade -1

# Rollback multiple migrations
alembic downgrade -3

# Rollback to specific migration
alembic downgrade <migration_id>
```

### Issue: Port 8000 already in use

**Solution**: Use a different port:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Development

### Code Quality

The project uses Ruff for code formatting and linting. Configuration is in `pyproject.toml`.

### Running Tests

```bash
pytest
```

## Dependencies

Key dependencies:
- **FastAPI**: Web framework
- **SQLModel**: SQL ORM with Pydantic
- **SQLAlchemy**: Database toolkit
- **Alembic**: Database migrations
- **Uvicorn**: ASGI server
- **ChromaDB**: Vector database for RAG
- **Chonkie**: Text chunking library
- **MistralAI**: LLM API client
- **python-multipart**: Form data handling

See `pyproject.toml` for complete dependency list.

## License

MIT

## Author

Iwan Susanto
