import typer
from rich import print_json
from typing_extensions import Annotated

from .config import save_config
from .commands import models, filesets, files, chat, prompt, qa, langserve

app = typer.Typer()

# Config App
config_app = typer.Typer()
app.add_typer(config_app, name="config")

@config_app.command("set")
def set_config(
    api_url: Annotated[str, typer.Option("--api-url", help="The API URL for PrivAI.")],
    token: Annotated[str, typer.Option("--token", help="The bearer token for authentication.")]
):
    """
    Set the API URL and bearer token.
    """
    config = {"api_url": api_url, "token": token}
    save_config(config)
    print_json(data={"status": "success", "message": "Configuration saved successfully."})

# Add command modules
app.add_typer(models.app, name="models")
app.add_typer(filesets.app, name="filesets")
app.add_typer(files.app, name="files")
app.add_typer(chat.app, name="chat")
app.add_typer(prompt.app, name="prompt")
app.add_typer(qa.app, name="qa")
app.add_typer(langserve.app, name="langserve")

if __name__ == "__main__":
    app()