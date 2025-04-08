import requests

def call_mcp(server_url: str, endpoint: str, payload: dict) -> dict:
    url = f"{server_url}{endpoint}"
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()
