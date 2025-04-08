# hello_world_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/manifest", methods=["GET"])
def manifest():
    return jsonify({
        "name": "hello_world_server",
        "description": "Says hello",
        "capabilities": [
            {
                "name": "hello",
                "description": "Returns hello",
                "endpoint": "/hello",
                "method": "POST",
            }
        ]
    })

@app.route("/hello", methods=["POST"])
def hello():
    data = request.json
    name = data.get("name", "Terry")
    return jsonify({"message": f"Hello, {name}!"})

if __name__ == "__main__":
    app.run(port=8000)
