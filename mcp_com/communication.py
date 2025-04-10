import asyncio

import requests
import yaml
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

ARGS = 'args'
URL = 'url'
COMMAND = 'command'
ROUTER = {}


def load_manifest_http(server_url: str) -> dict:
    resp = requests.get(f"{server_url}/manifest")
    resp.raise_for_status()
    return resp.json()


async def load_manifest_stdio(server_params):
    async with stdio_client(server_params) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            manifest = await session.list_tools()
    return manifest


async def manifest_loader(yaml_path: str = "./config/mcp_servers.yaml"):
    tools = []
    with open (yaml_path, 'r') as f:
        servers = yaml.safe_load(f)
    for server in servers:
        if ARGS in server:
            server_params = StdioServerParameters(
                command=server[COMMAND],
                args=server[ARGS],
            )
            manifest= await load_manifest_stdio(server_params)
            for tool in manifest.tools:
                tools.append({'tool': tool.name,
                              'description': tool.description, 'params': tool.inputSchema})
                ROUTER[tool.name] = (server_params, 'stdio')
        elif URL in server:
            manifest=load_manifest_http(server[URL])
            for tool in manifest['tools']:
                tools.append({'tool': tool['tool'],
                              'description': tool['description'], 'params': tool['inputSchema']})
                ROUTER[tool['tool']] = (server[URL], 'http')
    # print(ROUTER)
    return tools


async def call_tool(tool_name, params):
    handler, type = ROUTER[tool_name]
    if type == 'stdio':
        async with stdio_client(handler) as (stdio, write):
            async with ClientSession(stdio, write) as session:
                await session.initialize()
                # print(tool_name, params)
                response = await session.call_tool(tool_name, params)
        return response
    if type == 'http':
        url = handler + "/call"
        resp = requests.post(url, json=params)
        resp.raise_for_status()
        return resp.json()


"""async def main():
    server_params = StdioServerParameters(
        command='python',
        args=["-m", "mcp_server_time", "--local-timezone=America/New_York"],
    )

    # 通过 stdio_client 建立与服务器的连接
    async with stdio_client(server_params) as (stdio, write):
        # 创建客户端会话，用于后续交互
        async with ClientSession(stdio, write) as session:
            # 初始化会话（例如进行版本协商、配置交换等）
            await session.initialize()

            # 获取 manifest，即查询 MCP 服务器上注册的工具列表
            manifest = await session.list_tools()
            print("可用工具清单（Manifest）：")
            for tool in manifest.tools:
                print(f"工具名称：{tool.name}")
                print(f"描述：{tool.description}")
                print(f"输入参数：{tool.inputSchema}")
                print("-" * 30)

            # 示例：调用某个工具（例如假设服务器上注册有一个名称为 "echo" 的工具）
            tool_name = "echo"  # 请确保 MCP 服务器上确实有这个工具
            params = {"message": "Hello, MCP Client!"}
            # 调用该工具，返回结果会根据服务器实现不同而不同
            response = await session.call_tool(tool_name, params)
            print("调用工具返回结果：")
            print(response)"""


if __name__ == '__main__':
    asyncio.run(manifest_loader())
