from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from typing import Literal
import os
import uvicorn

app = FastAPI()

class FileIOParams(BaseModel):
    action: Literal["read", "write"]
    path: str
    content: str | None = None

@app.get("/manifest")
def get_manifest():
    return {
        "name": "file_io",
        "description": "读写本地文件的服务",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["read", "write"],
                    "description": "操作类型：'read' 表示读取文件，'write' 表示写入文件"
                },
                "path": {
                    "type": "string",
                    "description": "文件的绝对路径"
                },
                "content": {
                    "type": "string",
                    "description": "写入文件的内容，仅在 action=write 时需要"
                }
            },
            "required": ["action", "path"],
            "if": {
                "properties": {"action": {"const": "write"}}
            },
            "then": {
                "required": ["content"]
            }
        }
    }

@app.post("/call")
def handle_file_io(params: FileIOParams):
    try:
        if params.action == "read":
            if not os.path.exists(params.path):
                return {"error": f"文件不存在：{params.path}"}
            with open(params.path, "r", encoding="utf-8") as f:
                return {"content": f.read()}
        elif params.action == "write":
            with open(params.path, "w", encoding="utf-8") as f:
                f.write(params.content or "")
            return {"result": f"写入成功：{params.path}"}
        else:
            return {"error": f"未知操作类型：{params.action}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("file_io_http:app", host="0.0.0.0", port=8002)
