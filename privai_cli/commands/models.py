
import typer
from rich import print_json
import requests
from ..client import ApiClient

app = typer.Typer()

@app.command("list")
def list_models():
    """
    Get a list of available models.
    """
    client = ApiClient()
    try:
        response = client.get("/v1/models")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})
