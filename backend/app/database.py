import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/chatbot_db")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
