# agent/model_router.py

from coagent.agents import ChatAgent
from coagent.core import AgentSpec, new

from agent.client_builder import build_model_client
from agent.prompt import get_system_prompt


async def build_agent(model_name: str) -> AgentSpec:
    # create ModelClient
    client = build_model_client(model_name)

    # load prompt
    system_prompt = await get_system_prompt()

    # create agent
    agent = AgentSpec(
        f"{model_name}_agent",
        new(
            ChatAgent,
            system=system_prompt,
            client=client,
        ),
    )

    return agent


