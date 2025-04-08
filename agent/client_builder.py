import os
import yaml
from coagent.agents import ModelClient

NONE = "None"

def load_model_config(model_name: str) -> dict:
    with open("../config/models.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if model_name not in config:
        raise ValueError(f"Nothing is called '{model_name}' in models.yaml")

    return config[model_name]


# agent/client_builder.py

import os
import yaml
from coagent.agents import ModelClient


def load_model_config(model_name: str) -> dict:
    with open("../config/models.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if model_name not in config:
        raise ValueError(f"'{model_name}' not in models.yaml")

    return config[model_name]


def build_model_client(model_name: str) -> ModelClient:
    cfg = load_model_config(model_name)

    provider = cfg.get("provider")
    if provider == NONE:
        provider = None
    model = cfg.get("model")
    if model == NONE:
        model = None
    base_url = cfg.get("base_url")
    if base_url == NONE:
        base_url = None
    api_key_env = cfg.get("api_key_env")
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise EnvironmentError(f"No env var called '{api_key_env}'")

    return ModelClient(
        model=f"{model}",
        api_key=api_key,
        base_url=base_url,
    )


if __name__ == "__main__":
    build_model_client("gpt-4o-mini")
