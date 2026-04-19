import os

from fastapi.testclient import TestClient
from mcp.server.fastmcp import FastMCP

from app.core.setting import settings
from app.main import app
from dotenv import load_dotenv

load_dotenv()

mcp_port = os.getenv("MCP_PORT")

mcp = FastMCP(name="pdf-mcp", json_response=True, port=mcp_port)

client = TestClient(app)


@mcp.tool()
def get_root():
    """Get the root response of the API."""
    response = client.get("/")
    return response.json()


@mcp.tool()
def list_files(limit: int = 10, offset: int = 0):
    """List all uploaded PDF files with pagination."""
    response = client.get(f"/pdf/?limit={limit}&offset={offset}")
    return response.json()


@mcp.tool()
def get_file_detail(file_id: str):
    """Get detailed information about a specific PDF file using its UUID."""
    response = client.get(f"/pdf/{file_id}")
    return response.json()


@mcp.tool()
def search_pdf(query: str, n_results: int = 3):
    """Search for content across uploaded PDF files using vector search."""
    response = client.get(f"/search/{query}?n_results={n_results}")
    return response.json()


@mcp.tool()
def upload_pdf(file_path: str):
    """
    Upload a PDF file from a local path to the system.
    The system will automatically start the extraction process.
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    with open(file_path, "rb") as f:
        response = client.post("/pdf/upload", files={"file": f})
    return response.json()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
