
import requests
from rich import print_json
import typer
from .config import get_api_url, get_token

class ApiClient:
    def __init__(self):
        self.base_url = get_api_url()
        if self.base_url:
            self.base_url = self.base_url.rstrip('/')
        self.token = get_token()
        if not self.base_url or not self.token:
            print_json(data={"error": "API URL or token not configured. Please run 'privai-cli config set ...'"})
            raise typer.Exit(1)
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json"
        }

    def get(self, endpoint, params=None, stream=False):
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers, params=params, stream=stream)
        response.raise_for_status()
        return response

    def post(self, endpoint, params=None, json_data=None, data=None, files=None, stream=False):
        response = requests.post(f"{self.base_url}{endpoint}", headers=self.headers, params=params, json=json_data, data=data, files=files, stream=stream)
        response.raise_for_status()
        if response.status_code in [202, 204]:
            return None
        return response

    def delete(self, endpoint):
        response = requests.delete(f"{self.base_url}{endpoint}", headers=self.headers)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        return response
