
from mcp_com.communication import manifest_loader

with open("agent/prompts/prompt.pmt", 'r') as f:
    PROMPT = f.read()

TOOLS = ""

CLEAN = """
- based on the previous question and the raw response, extract useful info and make it readable:
ex.1: {<field_1>: val1, <field_2>: val2, <field_3>: val3, ...}
You should output: '
<field_1> : val1 or "N/A"
<field_2> : val2 or "N/A"
<field_3> : val3 or "N/A"
<field_3> : val3 or "N/A"
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