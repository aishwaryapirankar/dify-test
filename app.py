from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route("/openapi.yaml")
def serve_openapi_spec():
    return send_from_directory(os.getcwd(), 'openapi.yaml')

@app.route("/dify-plugin/hello", methods=["POST"])
def hello_plugin():
    data = request.json
    name = data.get("name", "stranger")
    return jsonify({ "message": f"Hello, {name}! This is a response from your Dify plugin."
})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333)
