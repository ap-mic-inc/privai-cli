
import typer
from rich import print_json
import requests
import json
from typing_extensions import Annotated
from typing import Optional
from ..client import ApiClient

app = typer.Typer()

@app.command("generate")
def generate_qa_pairs(
    fileset_id: Annotated[str, typer.Option(help="The ID of the fileset to use.")],
    model_name: Annotated[Optional[str], typer.Option(help="The model to use for generation.")] = None,
    extract_model_name: Annotated[Optional[str], typer.Option(help="The model to use for extraction.")] = None,
    temperature: Annotated[Optional[float], typer.Option(help="The temperature for generation.")] = None,
    target_amount: Annotated[Optional[int], typer.Option(help="The target amount of QA pairs.")] = None
):
    """Generate QA pairs from a fileset."""
    client = ApiClient()
    params = {"fileset_id": fileset_id}
    data = {}
    if model_name:
        data['model_name'] = model_name
    if extract_model_name:
        data['extract_model_name'] = extract_model_name
    if temperature is not None:
        data['temperature'] = temperature
    if target_amount is not None:
        data['target_amount'] = target_amount
    
    try:
        response = client.post("/v1/qa/generate", params=params, json_data=data)
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})
