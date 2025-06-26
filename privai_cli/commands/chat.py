

import typer
from rich import print_json
import requests
import json
from typing_extensions import Annotated
from typing import Optional
from ..client import ApiClient

app = typer.Typer()

@app.command("completions")
def chat_completions(
    model: Annotated[str, typer.Option(help="The model to use for the chat completion.")],
    messages: Annotated[str, typer.Option(help='The chat messages in JSON format. Ex: "[{\"role\": \"user\", \"content\": \"Hello\"}]"')],
    stream: Annotated[bool, typer.Option(help="Whether to stream the response.")] = False,
    prompt_id: Annotated[Optional[str], typer.Option("--prompt-id", help="The ID of the prompt to use.")] = None,
    fileset_id: Annotated[Optional[str], typer.Option("--fileset-id", help="The ID of the fileset to use.")] = None,
    temperature: Annotated[Optional[float], typer.Option(help="The temperature for the completion.")] = None
):
    """Create a chat completion."""
    client = ApiClient()
    try:
        messages_data = json.loads(messages)
    except json.JSONDecodeError:
        print_json(data={"error": "Invalid JSON format for messages."})
        raise typer.Exit(1)

    data = {
        "model": model,
        "messages": messages_data,
        "stream": stream
    }
    if prompt_id:
        data["prompt_id"] = prompt_id
    if fileset_id:
        data["fileset_id"] = fileset_id
    if temperature is not None:
        data["temperature"] = temperature
    
    try:
        if stream:
            response = client.post("/v1/chat/completions", json_data=data, stream=True)
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith("data: "):
                        json_str = line_str[6:]
                        if json_str.strip() == "[DONE]":
                            print() # Final newline
                            break
                        try:
                            chunk = json.loads(json_str)
                            if chunk['choices'][0]['delta'].get('content'):
                                print(chunk['choices'][0]['delta']['content'], end="", flush=True)
                        except json.JSONDecodeError:
                            pass # Ignore non-json lines
        else:
            response = client.post("/v1/chat/completions", json_data=data).json()
            print_json(data=response)
    except requests.exceptions.RequestException as e:
        print_json(data={"error": str(e)})

