from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load .env variables once
load_dotenv()

mongo_user = os.getenv("MONGO_USER")
mongo_db_password = os.getenv("MONGO_DB_PASSWORD")
mongo_db_name = os.getenv("MONGO_DB_NAME")
mongo_uri = f"mongodb+srv://jamesrawat575_db_user:3Bo8MmaAdtA8QNbw@cluster0.r1gp4u7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri, server_api=ServerApi('1'), tls=True)

class MongoDBClient:
    def __init__(self):
        pass

    def get_collection(self, collection_name: str):
        try:
            db = client["SYNCFLIX"]
            users = db[collection_name]
            return users
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Singleton instance (import and reuse across services)
mongodb_client = MongoDBClient()
