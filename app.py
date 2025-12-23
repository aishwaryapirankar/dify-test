# Import required modules
import os
import json
from flask import Flask, request, jsonify
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()
DB_USERNAME = quote_plus(os.getenv("DB_USERNAME"))
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))

# MongoDB connection Setup
uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@dify.9bbcbl1.mongodb.net/?appName=dify"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["dify"]

def parse_json(data):
    return json.loads(json_util.dumps(data))

# Find products or chat history (Evaluation case 1 and 5)
@app.route("/db/query", methods=["POST"])
def run_query():
    data = request.json
    
    # Check if request body is empty or collection is missing
    if not data or "collection" not in data or not data["collection"]:
        return jsonify({
            "error": "Missing or invalid 'collection' name. It must be a non-empty string."
        })

    try:
        collection_name = data.get("collection")
        collection = db[collection_name]
        filter_query = data.get("filter", {})
        limit = data.get("limit", 0)
        sort = data.get("sort", None)
        
        search = collection.find(filter_query).limit(limit)
        if sort:
            sort_list = [(k, v) for k, v in sort.items()] 
            search = search.sort(sort_list)
        results = list(search)
        return jsonify(parse_json(results))
    except Exception as e:
        return jsonify({"error": str(e)})

# Insert lead details and insurance request (Evaluation case 2 and 6)
@app.route("/db/insert", methods=["POST"])
def insert_doc():
    data = request.json
    collection_name = data.get("collection")
    collection = db[collection_name]
    input_data = data.get("data")
    
    # Validation for leads
    if collection_name == "leads" and "phone" in input_data:
        if not str(input_data["phone"]).startswith("+"):
            return jsonify({"error": "Invalid phone format"})
    result = collection.insert_one(input_data)
    return jsonify({"inserted_id": str(result.inserted_id)})

# Update order and ticket status (Evaluation case 3 - part 1 and case 7)
@app.route("/db/update", methods=["POST"])
def update_doc():
    data = request.json
    collection_name = data.get("collection")
    collection = db[collection_name]
    filter_query = data.get("filter")
    update_data = data.get("update")

    # Deny update if ticket is closed
    if collection_name == "tickets":
        current = collection.find_one(filter_query)
        if current and current.get("status") == "Closed":
            return jsonify({"reason": "Update blocked: Ticket is already Closed"})
    result = collection.update_many(filter_query, update_data)
    return jsonify({
        "matched_count": result.matched_count,
        "modified_count": result.modified_count
    })

# Delete order (Evaluation case 3 - part 2)
@app.route("/db/delete", methods=["POST"])
def delete_doc():
    data = request.json
    collection = db[data.get("collection")]
    result = collection.delete_one(data.get("filter"))
    return jsonify({"deleted_count": result.deleted_count})

# Query & business logic for customer segmentation (Evaluation case 4)
@app.route("/db/aggregate", methods=["POST"])
def aggregate_query():
    data = request.json
    collection = db[data.get("collection")]
    pipeline = data.get("pipeline")
    results = list(collection.aggregate(pipeline))
    return jsonify(parse_json(results))

# Error handler to convert 405 Method Not Allowed into a JSON response
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "error": "Method Not Allowed",
        "message": "This endpoint requires a POST request. Check your Postman/Dify settings."
    }), 405

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Server starting on port {port}...")
    app.run(host="0.0.0.0", port=port)
