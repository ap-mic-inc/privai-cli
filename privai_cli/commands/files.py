import typer
from rich import print_json
import requests
from typing_extensions import Annotated
from typing import Optional
from pathlib import Path
import sys
import mimetypes
from ..client import ApiClient

app = typer.Typer()

@app.command("list")
def list_files(
    fileset_id: Annotated[Optional[str], typer.Option("--fileset-id", help="Filter by fileset ID.")] = None,
    limit: int = 1000,
    order: str = "desc",
    after: str = None,
    before: str = None,
    purpose: Annotated[Optional[str], typer.Option(help="Filter by file purpose.")] = None
):
    """List files with filtering and pagination."""
    client = ApiClient()
    params = {
        "limit": limit,
        "order": order,
        "after": after,
        "before": before,
    }
    if fileset_id:
        params['fileset_id'] = fileset_id
    if purpose:
        params['purpose'] = purpose
    
    try:
        response = client.get("/v1/files", params=params)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("upload")
def upload_file(
    file_path: Annotated[Path, typer.Argument(help="The path to the file to upload.")],
    purpose: Annotated[Optional[str], typer.Option(help="The purpose of the file.")] = None,
    extra_metadata: Annotated[str, typer.Option(help="Extra metadata in JSON format.")] = "{}"
):
    """Upload a file with optional purpose and metadata."""
    if not file_path.exists() or not file_path.is_file():
        print_json(data={"error": f"File not found at: {file_path}"})
        raise typer.Exit(1)
    
    client = ApiClient()
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = "application/octet-stream"

    files = {"file": (file_path.name, open(file_path, "rb"), content_type)}
    params = {}
    data = {}
    if purpose:
        params['purpose'] = purpose
    data['extra_metadata'] = extra_metadata

    try:
        response = client.post("/v1/files", params=params, data=data, files=files)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})
    finally:
        files["file"][1].close()

@app.command("get")
def get_file(file_id: Annotated[str, typer.Argument(help="The ID of the file to retrieve.")]):
    """Get a specific file's metadata by its ID."""
    client = ApiClient()
    try:
        response = client.get(f"/v1/files/{file_id}")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("delete")
def delete_file(file_id: Annotated[str, typer.Argument(help="The ID of the file to delete.")]):
    """Delete a file by its ID."""
    client = ApiClient()
    try:
        client.delete(f"/v1/files/{file_id}")
        print_json(data={"status": "success", "file_id": file_id, "message": "File deleted."})
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("content")
def get_file_content(
    file_id: Annotated[str, typer.Argument(help="The ID of the file whose content to download.")],
    file_type: Annotated[Optional[str], typer.Option(help="The desired file format.")] = None
):
    """Download the content of a specific file."""
    client = ApiClient()
    params = {}
    if file_type:
        params['file_type'] = file_type
    try:
        response = client.get(f"/v1/files/{file_id}/content", params=params, stream=True)
        for chunk in response.iter_content(chunk_size=8192):
            sys.stdout.buffer.write(chunk)
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})