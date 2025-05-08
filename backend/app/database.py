from pymongo import mongo_client
import pymongo
from app.config import settings

client = mongo_client.MongoClient(
    settings.DATABASE_URL, serverSelectionTimeoutMS=5000)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect to the MongoDB server.")

db = client[settings.MONGO_INITDB_DATABASE]
Catalog = db.catalog
Catalog.create_index([("name", pymongo.ASCENDING)], unique=True)

Orders = db.order
Orders.create_index([("order_time", pymongo.ASCENDING)], unique=True)
