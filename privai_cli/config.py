
from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".config" / "privai-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config():
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_api_url():
    config = load_config()
    return config.get("api_url")

def get_token():
    config = load_config()
    return config.get("token")
