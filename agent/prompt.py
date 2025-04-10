
from mcp_com.communication import manifest_loader

PROMPT = """
You are an smart assistant. You must decide whether to respond directly without a tool or call a tool.
When calling a tool:
1. Choose the correct tool name;
2. Fill in all required parameters accurately;
3. Return ONLY a valid JSON object in this format:
{
  "tool_name": "name_of_the_tool",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  }
}
Do NOT include any extra text. Do NOT hallucinate tools. Ask clarifying questions if needed.
Remember: If the user says "save the previous response", you must treat your own last reply as the content to save, and pass it to the appropriate tool.
"""

TOOLS = ""

CLEAN = "based on the previous question and the raw response, extract useful info and compile it to a sentence: "

async def get_system_prompt():
    global TOOLS
    _ = await manifest_loader()
    TOOLS = str(_)
    return PROMPT+' '+TOOLS

if __name__ == "__main__":
    print(get_system_prompt())