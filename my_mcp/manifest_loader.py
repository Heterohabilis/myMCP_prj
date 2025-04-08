import requests
import yaml
from my_mcp.mcp_invoker import set_tool_router


def load_manifest(server_url: str) -> dict:
    resp = requests.get(f"{server_url}/manifest")
    resp.raise_for_status()
    return resp.json()


def manifest_to_tool_function(manifest: dict) -> list:
    tools = []
    for cap in manifest.get("capabilities", []):
        tools.append({
            "type": "function",
            "function": {
                "name": cap["name"],
                "description": cap.get("description", ""),
                "parameters": {
                    "type": "object",
                    "properties": cap.get("parameters", {}),
                    "required": cap.get("required", [])
                }
            }
        })
    return tools


def load_all_mcp_tools(yaml_path: str = "./config/mcp_servers.yaml") -> list:
    tools, router = [], {}
    with open(yaml_path, "r") as f:
        servers = yaml.safe_load(f)
    for server in servers:
        manifest = load_manifest(server["url"])
        for cap in manifest.get("capabilities", []):
            router[cap["name"]] = {
                "url": server["url"],
                "endpoint": cap["endpoint"]
            }
        server_tools = manifest_to_tool_function(manifest)
        tools.extend(server_tools)
    set_tool_router(router)
    return tools

if __name__ == "__main__":
    print(load_all_mcp_tools())