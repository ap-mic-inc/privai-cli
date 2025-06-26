
import typer
from rich import print_json
import requests
from typing_extensions import Annotated
from typing import List
from ..client import ApiClient

app = typer.Typer()

@app.command("list")
def list_jobs():
    """
    List all jobs.
    """
    client = ApiClient()
    try:
        response = client.get("/v1/jobs")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("create")
def create_job(
    model: Annotated[str, typer.Option(help="The model to use for the job.")],
    fileset_id: Annotated[str, typer.Option(help="The ID of the fileset to process.")],
    redact_pii: Annotated[bool, typer.Option(help="Whether to redact PII.")] = True,
    redact_all_named_entities: Annotated[bool, typer.Option(help="Whether to redact all named entities.")] = False,
    allowed_named_entities: Annotated[List[str], typer.Option("--allowed-named-entities", help="List of allowed named entities.")] = None
):
    """
    Create a new job.
    """
    client = ApiClient()
    redaction_config = {
        "redact_pii": redact_pii,
        "redact_all_named_entities": redact_all_named_entities,
        "allowed_named_entities": allowed_named_entities or []
    }
    data = {
        "model": model,
        "fileset_id": fileset_id,
        "redaction_config": redaction_config
    }
    try:
        job = client.post("/v1/jobs", json_data=data).json()
        print_json(data=job)
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("get")
def get_job(job_id: Annotated[str, typer.Argument(help="The ID of the job to retrieve.")]):
    """
    Get a specific job by its ID.
    """
    client = ApiClient()
    try:
        response = client.get(f"/v1/jobs/{job_id}")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("cancel")
def cancel_job(job_id: Annotated[str, typer.Argument(help="The ID of the job to cancel.")]):
    """
    Cancel a job by its ID.
    """
    client = ApiClient()
    try:
        response = client.post(f"/v1/jobs/{job_id}/cancel").json()
        print_json(data=response)
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})
