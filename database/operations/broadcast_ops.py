from typing import List
from datetime import datetime
from database.connection import db
from database.models.broadcasts import BroadcastModel

class BroadcastOperations:
    def __init__(self):
        self.collection_name = BroadcastModel.COLLECTION_NAME
    
    async def create_broadcast(self, broadcast_data: dict) -> str:
        collection = db.get_collection(self.collection_name)
        result = await collection.insert_one(broadcast_data)
        return str(result.inserted_id)
    
    async def get_expired_broadcasts(self) -> List[dict]:
        collection = db.get_collection(self.collection_name)
        cursor = collection.find({
            "delete_at": {"$lte": datetime.utcnow()}
        })
        return await cursor.to_list(length=None)
    
    async def delete_broadcast(self, broadcast_id: str):
        collection = db.get_collection(self.collection_name)
        from bson import ObjectId
        await collection.delete_one({"_id": ObjectId(broadcast_id)})

broadcast_ops = BroadcastOperations()
