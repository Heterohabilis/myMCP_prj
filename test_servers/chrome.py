from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)
PORT = 1509

@app.route("/manifest", methods=["GET"])
def manifest():
    return jsonify({
        "name": "launch_chrome",
        "capabilities": [
            {
                "description": "Launch Chrome to open a specific URL.",
                "parameters": {
                    "url": {
                        "type": "string",
                        "description": "The URL to open in Chrome."
                    }
                },
                "required": ["url"]
            }
        ]
    })

@app.route("/call", methods=["POST"])
def call():
    data = request.get_json(silent=True)
    if not data:
        print("No data")
        return jsonify({"error": "No data provided"}), 400

    url = data.get("url")
    if not url:
        print("No url")
        return jsonify({"error": "Missing 'url' in arguments"}), 400

    try:
        subprocess.Popen(["google-chrome", url])
        return jsonify({"status": "launched", "url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(port=PORT)
