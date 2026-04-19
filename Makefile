dev:
	uv run uvicorn app.main:app --reload

celery:
	uv run celery -A app.core.celery_app worker --loglevel=info --queues=pdf_extraction	