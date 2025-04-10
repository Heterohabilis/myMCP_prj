
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

CLEAN = """
- based on the previous question and the raw response, extract useful info and make it readable:
ex.1: {field_1: val1, field_2: val2, field_3: val3, ...}
You should output: '
field_1 : val1 or "N/A"
field_2 : val2 or "N/A"
field_3 : val3 or "N/A"
field_3 : val3 or "N/A"
...
'
if there is a return value, explain it like: the process finished with / with no error
"""

async def get_system_prompt():
    global TOOLS
    _ = await manifest_loader()
    TOOLS = str(_)
    return PROMPT+' '+TOOLS

if __name__ == "__main__":
    print(get_system_prompt())