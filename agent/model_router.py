# agent/model_router.py


from coagent.agents import ChatAgent, ModelClient, ChatMessage
from coagent.core import AgentSpec, new, set_stderr_logger


from client_builder import build_model_client
from prompt import get_system_prompt


def build_agent(model_name: str) -> AgentSpec:
    # create ModelClient
    client = build_model_client(model_name)

    # load prompt
    system_prompt = get_system_prompt()

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

