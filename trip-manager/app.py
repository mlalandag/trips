from kafka import KafkaConsumer
import pymongo
import json
import requests
import os

MONGO_DB_URI=os.environ.get("MONGO_DB_URI")
KAFKA_BOOSTRAP_SERVERS=os.environ.get("KAFKA_BOOSTRAP_SERVERS")

client = pymongo.MongoClient(MONGO_DB_URI, tlsAllowInvalidCertificates=True)
db = client.cabifly

consumer = KafkaConsumer(
    'cabifly.trips',
     bootstrap_servers=[KAFKA_BOOSTRAP_SERVERS],
     auto_offset_reset='earliest'
)

# Kafka Directo
for message in consumer:
    item = json.loads(message.value)
    event = item["event"]
    data = item["data"]
    print(f"event >> {event}, data >> {data}")

    if event == "trip-requested":
        drones = requests.get(
            "https://bav1irtppi.execute-api.us-east-1.amazonaws.com/dev/drones",
            params={
                "lon": data["location"][0],
                "lat": data["location"][1],
                "distance": 1000
            }
        ).json()
        
        if len(drones) > 0:
            db.trips.update_one(
                {"trip_id": data["trip_id"]},
                {"$set": {
                    "status": "assigned",
                    "drone_id": drones[0]["drone_id"]
                }}
            )

# Kafka con MongoDB Connect
# for message in consumer:
#     payload = json.loads(json.loads(message.value.decode())["payload"])
#     operationType = payload["operationType"]
#     data = payload["fullDocument"]

#     if data["status"] == "waiting":
#         drones = requests.get(
#             "http://localhost:8000/drones",
#             params={
#                 "lon": data["location"][0],
#                 "lat": data["location"][1],
#                 "distance": 1000
#             }
#         ).json()
        
#         if len(drones) > 0:
#             db.trips.update_one(
#                 {"trip_id": data["trip_id"]},
#                 {"$set": {
#                     "status": "assigned",
#                     "drone_id": drones[0]["drone_id"]
#                 }}
#             )            