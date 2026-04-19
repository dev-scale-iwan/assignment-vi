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

### Available Endpoints

#### PDF Upload
- **POST** `/pdf/upload` - Upload a PDF file
  - Request: Form data with file (PDF only)
  - Response: JSON with filename, file_size, file_id, and success message
  - File metadata is automatically stored in the database

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
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "File uploaded successfully"
}
```

The `file_id` is a UUID that uniquely identifies the uploaded file in the database and can be used for future references.

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
```

To view all available commands:
```bash
make help
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
