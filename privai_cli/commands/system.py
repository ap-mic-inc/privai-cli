
import typer
from rich import print_json
import requests
from ..client import ApiClient

app = typer.Typer()

@app.command("health")
def health_check():
    """
    Perform a health check.
    """
    client = ApiClient()
    try:
        response = client.get("/")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("settings")
def get_system_settings():
    """
    Get system settings.
    """
    client = ApiClient()
    try:
        response = client.get("/v1/system/settings")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("reindex")
def reindex():
    """
    Trigger a re-indexing of the system.
    """
    client = ApiClient()
    try:
        response = client.post("/v1/system/reindex").json()
        print_json(data=response)
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})
