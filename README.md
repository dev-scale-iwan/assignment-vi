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

### 3. Initialize Database & Run Migrations

Run Alembic migrations to set up the database schema:

```bash
alembic upgrade head
```

This will:
- Create the database file (`iwansusanto.db`)
- Apply all pending migrations
- Set up required tables

## Running the Application

### Start the FastAPI Server

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

### Available Endpoints

#### PDF Upload
- **POST** `/pdf/upload` - Upload a PDF file
  - Request: Form data with file (PDF only)
  - Response: JSON with filename, file_size, and success message

#### Health Check
- **GET** `/health` - API health status
  - Response: `{"status": "ok"}`

#### Root
- **GET** `/` - API information
  - Response: Available endpoints and descriptions

## API Usage Examples

### Upload a PDF File

```bash
curl -X POST "http://localhost:8000/pdf/upload" \
  -F "file=@document.pdf"
```

Response:
```json
{
  "filename": "document.pdf",
  "file_size": 102400,
  "message": "File uploaded successfully"
}
```

## Project Structure

```
assignment-vi/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── schema/
│   │   └── pdf.py          # Pydantic schemas for API responses
│   ├── router/
│   │   └── pdf.py          # PDF upload routes
│   ├── utils/
│   │   └── utils.py        # Utility functions
│   ├── models/             # SQLModel database models
│   └── core/               # Configuration and settings
├── alembic/                # Database migrations
│   ├── versions/           # Migration scripts
│   ├── env.py              # Alembic environment configuration
│   └── alembic.ini         # Alembic configuration
├── uploads/                # Uploaded PDF files (auto-created)
├── pyproject.toml          # Project dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Database Migrations

### Create a New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Pending Migrations

```bash
alembic upgrade head
```

### Downgrade to Previous Migration

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic history
```

## Environment Variables

Create a `.env` file in the root directory (see `.env-example` for reference):

```bash
# Database
DATABASE_URL=sqlite:///iwansusanto.db

# API Configuration
API_TITLE=Assignment VI - RAG System
API_VERSION=0.1.0
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
