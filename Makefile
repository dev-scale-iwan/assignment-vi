dev:
	uv run uvicorn app.main:app --reload

celery:
	uv run celery -A app.core.celery_app worker --loglevel=info --queues=pdf_extraction	

mcp:
	uv run python -m app.core.mcp

mcp-dev:
	PYTHONPATH=. uv run mcp dev app/core/mcp.py