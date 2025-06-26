
import typer
from rich import print_json
import requests
import json
from typing_extensions import Annotated
from typing import Optional
from ..client import ApiClient

app = typer.Typer()

@app.command("create")
def create_prompt(
    value: Annotated[str, typer.Argument(help="The value of the prompt.")],
    metadata: Annotated[str, typer.Option("--metadata", help="Metadata for the prompt in JSON format.")] = "{}"
):
    """Create a new prompt."""
    client = ApiClient()
    try:
        metadata_data = json.loads(metadata)
    except json.JSONDecodeError:
        print_json(data={"error": "Invalid JSON format for metadata."})
        raise typer.Exit(1)

    data = {"value": value, "metadata": metadata_data}
    try:
        response = client.post("/v1/prompt", json_data=data)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("list")
def list_prompts(
    limit: int = 20,
    order: str = "desc",
    after: str = None,
    before: str = None
):
    """List all prompts."""
    client = ApiClient()
    params = {"limit": limit, "order": order, "after": after, "before": before}
    try:
        response = client.get("/v1/prompt", params=params)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("get")
def get_prompt(prompt_id: Annotated[str, typer.Argument(help="The ID of the prompt to retrieve.")]):
    """Get a specific prompt by its ID."""
    client = ApiClient()
    try:
        response = client.get(f"/v1/prompt/{prompt_id}")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("delete")
def delete_prompt(prompt_id: Annotated[str, typer.Argument(help="The ID of the prompt to delete.")]):
    """Delete a prompt by its ID."""
    client = ApiClient()
    try:
        client.delete(f"/v1/prompt/{prompt_id}")
        print_json(data={"status": "success", "prompt_id": prompt_id, "message": "Prompt deleted."})
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("optimize-auto")
def optimize_auto(
    prompt_id: Annotated[str, typer.Argument(help="The ID of the prompt to optimize.")],
    model: Annotated[Optional[str], typer.Option(help="The model to use for optimization.")] = None
):
    """Automatically optimize a prompt."""
    client = ApiClient()
    params = {}
    if model:
        params['model'] = model
    try:
        response = client.post(f"/v1/prompt/{prompt_id}/optimize/auto", params=params)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("optimize-instruct")
def optimize_instruct(
    prompt_id: Annotated[str, typer.Argument(help="The ID of the prompt to optimize.")],
    current_issue: Annotated[str, typer.Option(help="The current issue.")],
    desired_behavior: Annotated[str, typer.Option(help="The desired behavior.")]
):
    """Optimize a prompt based on instructions."""
    client = ApiClient()
    params = {"current_issue": current_issue, "desired_behavior": desired_behavior}
    try:
        response = client.post(f"/v1/prompt/{prompt_id}/optimize/instruct", params=params)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})
