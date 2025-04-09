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
                "description": "Greets the user with the given name",
                "endpoint": "/hello",
                "method": "POST",
                "parameters": {
                    "name": {
                        "type": "string",
                        "description": "The name to greet"
                    }
                },
                "required": ["name"]
            }
        ]
    })

@app.route("/call", methods=["POST"])
def hello():
    data = request.json or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing required parameter: name"}), 400
    return jsonify({"message": f"Hello, {name}!"})

if __name__ == "__main__":
    app.run(port=8000)
