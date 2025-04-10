def should_summarize(raw_output: str) -> bool:
    return "{" in raw_output or "}" in raw_output
