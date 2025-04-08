import requests

import requests

TOOL_ROUTING_TABLE = {}


def set_tool_router(router: dict):
    global TOOL_ROUTING_TABLE
    TOOL_ROUTING_TABLE = router


def call_tool(tool_name: str, parameters: dict) -> dict:
    if tool_name not in TOOL_ROUTING_TABLE:
        raise ValueError(f"Tool '{tool_name}' not found in routing table.")

    route = TOOL_ROUTING_TABLE[tool_name]
    url = f"{route['url']}{route['endpoint']}"
    print(f"using {tool_name} → {url}，paras: {parameters}")
    resp = requests.post(url, json=parameters)
    resp.raise_for_status()
    return resp.json()

