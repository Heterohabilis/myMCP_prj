import asyncio
import json
import sys
import os

from my_mcp.mcp_invoker import call_tool

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coagent.agents import ChatMessage
from coagent.core import set_stderr_logger
from coagent.runtimes import LocalRuntime

from agent.model_router import build_agent



async def main(translator):
    async with LocalRuntime() as runtime:
        await runtime.register(translator)

        result = await translator.run(
            ChatMessage(role="user", content="打个招呼").encode(),
            stream=False,
        )
        msg = ChatMessage.decode(result)
        msg_dic = json.loads(msg.content)
        resp = call_tool(msg_dic.get('tool_name', {}), msg_dic.get('parameters', {}))
        print(resp)



if __name__ == "__main__":
    set_stderr_logger()
    asyncio.run(main(build_agent("gpt-4o-mini")))