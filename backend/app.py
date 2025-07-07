from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import pickle


# Load env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

# Helper: serialize Mongo _id to string
def serialize(threat):
    threat["_id"] = str(threat["_id"])
    return threat


@app.route("/api/threats", methods=["GET"])
def get_threats():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    category = request.args.get("category")
    search = request.args.get("search")

    query = {}

    if category:
        query["threat_category"] = category

    if search:
        query["$or"] = [
            {"cleaned_description": {"$regex": search, "$options": "i"}},
            {"threat_category": {"$regex": search, "$options": "i"}}
        ]

    skip = (page - 1) * limit
    threats = list(collection.find(query).skip(skip).limit(limit))
    threats = [serialize(t) for t in threats]

    total = collection.count_documents(query)

    return jsonify({
        "data": threats,
        "total": total,
        "page": page,
        "limit": limit
    })


@app.route("/api/threats/<id>", methods=["GET"])
def get_threat_by_id(id):
    try:
        threat = collection.find_one({"_id": ObjectId(id)})
        if not threat:
            return jsonify({"error": "Threat not found"}), 404
        return jsonify(serialize(threat))
    except Exception:
        return jsonify({"error": "Invalid ID"}), 400


@app.route("/api/threats/stats", methods=["GET"])
def get_stats():
    total = collection.count_documents({})
    
    category_pipeline = [
        {"$group": {"_id": "$threat_category", "count": {"$sum": 1}}}
    ]
    category_counts = list(collection.aggregate(category_pipeline))

    severity_pipeline = [
        {"$group": {"_id": "$severity_score", "count": {"$sum": 1}}}
    ]
    severity_counts = list(collection.aggregate(severity_pipeline))

    return jsonify({
        "total_threats": total,
        "category_counts": category_counts,
        "severity_counts": severity_counts
    })

# Load the trained pipeline
model_pipeline = None
model_file = os.path.join(os.path.dirname(__file__), "model", "threat_model.pkl")
with open(model_file, "rb") as f:
    model_pipeline = pickle.load(f)


@app.route("/api/analyze", methods=["POST"])
def analyze_threat():
    data = request.get_json()
    desc = data.get("description", "").strip()
    if not desc:
        return jsonify({"error": "Description is required"}), 400

    # Predict category
    try:
        pred = model_pipeline.predict([desc])[0]
        return jsonify({"predicted_category": pred})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5050, host='0.0.0.0')  # ADD host='0.0.0.0'

