from app.router.pdf import pdf_router
from app.router.search import search_router
from fastapi import FastAPI
from app.core.setting import settings
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

app.include_router(pdf_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {"hallo": "Iwan Susanto", "description": "Assignment 6"}

@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
