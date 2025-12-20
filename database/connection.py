from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from shared.config import config

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.sync_client = None
        self.sync_db = None
    
    async def connect(self):
        self.client = AsyncIOMotorClient(config.MONGO_URI)
        self.db = self.client[config.DB_NAME]
        print("✅ Connected to MongoDB (Async)")
    
    def connect_sync(self):
        self.sync_client = MongoClient(config.MONGO_URI)
        self.sync_db = self.sync_client[config.DB_NAME]
        print("✅ Connected to MongoDB (Sync)")
    
    async def close(self):
        if self.client:
            self.client.close()
            print("❌ Disconnected from MongoDB (Async)")
    
    def close_sync(self):
        if self.sync_client:
            self.sync_client.close()
            print("❌ Disconnected from MongoDB (Sync)")
    
    def get_collection(self, collection_name: str):
        return self.db[collection_name]
    
    def get_sync_collection(self, collection_name: str):
        return self.sync_db[collection_name]

db = Database()
