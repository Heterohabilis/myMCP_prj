import asyncio
import json
import sys
import os

from agent.prompt import CLEAN
from mcp_com.communication import call_tool
from utils.json_cleaner import extract_json_block
from utils.ring_memo import naive_memo

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
MODEL = "deepseek-chat"

from coagent.agents import ChatMessage
from coagent.core import set_stderr_logger
from coagent.runtimes import LocalRuntime

from agent.model_router import build_agent


async def agent_start(agent):
    memo = naive_memo(n=50)
    print("Agent is ready; input 'exit' to quit")

    async with LocalRuntime() as runtime:
        await runtime.register(agent)
        while True:
            user_input = input("You：").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Bye！")
                break


            context_prompt = str(memo) + "\nuser: " + user_input
            response = await agent.run(
                ChatMessage(role="user", content=context_prompt).encode(),
                stream=False
            )
            msg = ChatMessage.decode(response)

            try:
                tool_call = msg.content
                if "tool_name" in tool_call and "parameters" in tool_call:
                    tool_call = json.loads(extract_json_block(tool_call))
                    # print(tool_call)
                    raw_result = await call_tool(tool_call["tool_name"], tool_call["parameters"])
                    result = await agent.run(
                        ChatMessage(role="system", content=CLEAN+str(raw_result)).encode(),
                        stream=False
                         )
                    result = ChatMessage.decode(result)
                    print("🤖 ", result.content)

                    memo.add(user_input, json.dumps({
                        "tool_name": tool_call["tool_name"],
                        "result": result.content
                    }, ensure_ascii=False))

                else:
                    print("🤖", msg.content)
                    memo.add(user_input, msg.content)

            except json.JSONDecodeError:
                memo.add(user_input, msg.content)



async def main():
    set_stderr_logger()
    translator = await build_agent(MODEL)
    await agent_start(translator)



if __name__ == "__main__":
    asyncio.run(main())
