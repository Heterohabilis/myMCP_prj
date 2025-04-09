from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)
PORT = 1510
DESCRIPTION = ("Accepts user intent and runs bash commands accordingly. "
               "The model should analyze the user's request, "
               "identify the most appropriate bash solution "
               "(possibly from multiple options), and return one complete,"
               " executable, multi-line bash script string inside the 'commands' field. "
               "The script must not include any 'sudo' commands, "
               "and must be syntactically valid and ready to execute in a non-root environment. "
               "Commands should be separated by line breaks if multiple lines are needed."
               "Uses heredoc (cat <<EOF > filename) to write source code when needed"
               )


@app.route("/manifest", methods=["GET"])
def manifest():
    return jsonify({
        "name": "bash",
        "capabilities": [
            {
                "description": DESCRIPTION,
                "parameters": {
                    "commands": {
                        "type": "string",
                        "description": "The bash commands to run"
                    }
                },
                "required": ["commands"]
            }
        ]
    })

@app.route("/call", methods=["POST"])
def call():
    data = request.get_json(silent=False)
    print(data)
    if not data:
        print("No data")
        return jsonify({"error": "No data provided"}), 400

    commands = data.get("commands")
    if not commands:
        print("No command")
        return jsonify({"error": "Missing 'commands' in arguments"})

    try:
        result = subprocess.run(
            ["bash", "-c", commands],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1000,
            text=True,
        )

        return jsonify({
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command execution timed out"}), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=PORT)
