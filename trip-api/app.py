import pymongo
from flask import Flask, request, jsonify
import os

MONGO_DB_URI=os.environ.get("MONGO_DB_URI")

client = pymongo.MongoClient(MONGO_DB_URI, tlsAllowInvalidCertificates=True)
db = client.cabifly

app = Flask(__name__)

@app.route("/users/<user_id>/trips", methods=["GET"])
def get_trips(user_id):
    
    items = list(db.trips.find({"user_id": user_id}, {"_id": 0}).sort(("created_at"), (-1)).limit(3))
    
    return jsonify([
        {k:v for k,v in i.items() if k != "_id"} 
        for i in items
    ])


@app.route("/users/<user_id>/trips", methods=["POST"])
def post_trips(user_id):
    
    body = request.json
    
    item = {
        "trip_id": str(uuid4()),
        "user_id": user_id,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "location": [body["lon"], body["lat"]],
        "status": "waiting"
    }
    
    db.trips.insert_one(item)
    
    # Use mongo connect, but this can be used as a failover
    message = {
        "event": "trip-requested",
        "data": {k:v for k,v in item.items() if k != "_id"}
    }
    
    producer.send(
        'cabifly.trips', 
        key=item["trip_id"].encode(), 
        value=json.dumps(message).encode()
    )
    
    return jsonify({k:v for k,v in item.items() if k != "_id"})