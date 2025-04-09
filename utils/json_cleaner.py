import json
import re


def extract_json_block(text: str):
    start_index = text.find("{")
    if start_index == -1:
        return None  # 没有左大括号

    stack = []
    end_index = -1

    for i in range(start_index, len(text)):
        char = text[i]
        if char == "{":
            stack.append("{")
        elif char == "}":
            if stack:
                stack.pop()
                if not stack:
                    end_index = i
                    break

    if end_index != -1:
        json_substring = text[start_index:end_index + 1]
        return json_substring
    else:
        return None
case = """
Here is the JSON format for the tool call:

```json
{
  "tool_name": "bash",
  "parameters": {
    "commands": "echo 'Comparison of M4A3E2 and M4A3E8 Tanks:\n\n1. M4A3E2:\n   - Developed as a heavy tank variant of the M4 Sherman.\n   - Equipped with a 105 mm howitzer.\n   - Heavier armor compared to standard Shermans.\n   - Limited production and deployment.\n\n2. M4A3E8:\n   - Known as the 'Easy Eight'.\n   - Featured a 76 mm gun for improved firepower.\n   - Enhanced suspension system for better mobility.\n   - More widely produced and used in combat.\n\nOverall, the M4A3E8 was more versatile and effective in combat compared to the M4A3E2.' > ~/Desktop/m4_comparison.txt"
  }
}
```
"""

if __name__ == "__main__":
    print(extract_json_block(case))
