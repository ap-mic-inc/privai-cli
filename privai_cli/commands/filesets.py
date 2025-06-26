
import typer
from rich import print_json
import requests
import json
from typing_extensions import Annotated
from typing import List, Optional
from ..client import ApiClient

app = typer.Typer()

@app.command("list")
def list_filesets(
    limit: int = 100,
    order: str = "desc",
    after: str = None,
    before: str = None
):
    """List filesets."""
    client = ApiClient()
    params = {"limit": limit, "order": order, "after": after, "before": before}
    try:
        response = client.get("/v1/filesets", params=params)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("create")
def create_fileset(
    file_ids: Annotated[List[str], typer.Option("--file-ids", help="A list of file IDs to be included in the fileset.")],
    metadata: Annotated[str, typer.Option("--metadata", help="Metadata for the fileset in JSON format.")] = "{}"
):
    """Create a new fileset and attach files."""
    client = ApiClient()
    try:
        metadata_data = json.loads(metadata)
    except json.JSONDecodeError:
        print_json(data={"error": "Invalid JSON format for metadata."})
        raise typer.Exit(1)
    
    data = {"file_ids": file_ids, "metadata": metadata_data}
    try:
        response = client.post("/v1/filesets", json_data=data)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("get")
def get_fileset(fileset_id: Annotated[str, typer.Argument(help="The ID of the fileset to retrieve.")]):
    """Get a specific fileset by its ID."""
    client = ApiClient()
    try:
        response = client.get(f"/v1/filesets/{fileset_id}")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("update")
def update_fileset(
    fileset_id: Annotated[str, typer.Argument(help="The ID of the fileset to update.")],
    file_ids: Annotated[Optional[List[str]], typer.Option("--file-ids", help="The new list of file IDs for the fileset.")] = None,
    metadata: Annotated[Optional[str], typer.Option("--metadata", help="The new metadata for the fileset in JSON format.")] = None
):
    """Update a fileset's metadata or file list."""
    client = ApiClient()
    data = {}
    if file_ids is not None:
        data['file_ids'] = file_ids
    if metadata is not None:
        try:
            data['metadata'] = json.loads(metadata)
        except json.JSONDecodeError:
            print_json(data={"error": "Invalid JSON format for metadata."})
            raise typer.Exit(1)
    
    if not data:
        print_json(data={"error": "You must provide --file-ids or --metadata to update."})
        raise typer.Exit(1)

    try:
        response = client.put(f"/v1/filesets/{fileset_id}", json_data=data)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("delete")
def delete_fileset(fileset_id: Annotated[str, typer.Argument(help="The ID of the fileset to delete.")]):
    """Delete a fileset by its ID."""
    client = ApiClient()
    try:
        response = client.delete(f"/v1/filesets/{fileset_id}")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("commit")
def commit_fileset(
    fileset_id: Annotated[str, typer.Argument(help="The ID of the fileset to commit.")],
    embedding_model: Annotated[str, typer.Option("--embedding-model", help="The embedding model to use.")]
):
    """Commit a fileset to start the embedding process."""
    client = ApiClient()
    data = {"embedding_model": embedding_model}
    try:
        client.post(f"/v1/filesets/{fileset_id}/commit", json_data=data)
        print_json(data={"status": "success", "message": f"Fileset {fileset_id} commit accepted."})
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("duplicate")
def duplicate_fileset(fileset_id: Annotated[str, typer.Argument(help="The ID of the fileset to duplicate.")]):
    """Create a duplicate of a fileset."""
    client = ApiClient()
    try:
        response = client.post(f"/v1/filesets/{fileset_id}/duplicate")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})
