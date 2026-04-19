from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

# Celery configuration
celery_app = Celery(
    "pdf_extraction",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
    include=["app.core.tasks"]
)

# Celery settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.core.tasks.extract_pdf_task": {"queue": "pdf_extraction"},
    },
)

if __name__ == "__main__":
    celery_app.start()