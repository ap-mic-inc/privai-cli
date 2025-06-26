
import typer
from rich import print_json
import requests
import json
from typing import Optional
from ..client import ApiClient

app = typer.Typer()

@app.command("input-schema")
def get_input_schema():
    """Get the input schema for the runnable."""
    client = ApiClient()
    try:
        response = client.get("/v1/input_schema")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("output-schema")
def get_output_schema():
    """Get the output schema for the runnable."""
    client = ApiClient()
    try:
        response = client.get("/v1/output_schema")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("config-schema")
def get_config_schema():
    """Get the config schema for the runnable."""
    client = ApiClient()
    try:
        response = client.get("/v1/config_schema")
        print_json(data=response.json())
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("invoke")
def invoke(input_data: str, config_hash: Optional[str] = None, config: str = '{}', kwargs: str = '{}'):
    """Invoke the runnable with a single request."""
    client = ApiClient()
    params = {}
    if config_hash:
        params['config_hash'] = config_hash
    try:
        input_data_json = json.loads(input_data)
        config_json = json.loads(config)
        kwargs_json = json.loads(kwargs)
        data = {"input": input_data_json, "config": config_json, "kwargs": kwargs_json}
        response = client.post("/v1/invoke", params=params, json_data=data)
        print_json(data=response.json())
    except json.JSONDecodeError:
        print_json(data={"error": "Invalid JSON format for input, config, or kwargs."})
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

@app.command("stream")
def stream(input_data: str, config_hash: Optional[str] = None, config: str = '{}', kwargs: str = '{}'):
    """Stream the runnable execution results."""
    client = ApiClient()
    params = {}
    if config_hash:
        params['config_hash'] = config_hash
    try:
        input_data_json = json.loads(input_data)
        config_json = json.loads(config)
        kwargs_json = json.loads(kwargs)
        data = {"input": input_data_json, "config": config_json, "kwargs": kwargs_json}
        response = client.post("/v1/stream", params=params, json_data=data, stream=True)
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))
    except json.JSONDecodeError:
        print_json(data={"error": "Invalid JSON format for input, config, or kwargs."})
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})
