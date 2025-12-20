from typing import List
from datetime import datetime
from database.connection import db
from database.models.pending_deletions import PendingDeletionModel

class DeletionOperations:
    def __init__(self):
        self.collection_name = PendingDeletionModel.COLLECTION_NAME
    
    async def create_pending_deletion(self, deletion_data: dict) -> str:
        collection = db.get_collection(self.collection_name)
        result = await collection.insert_one(deletion_data)
        return str(result.inserted_id)
    
    async def get_due_deletions(self) -> List[dict]:
        collection = db.get_collection(self.collection_name)
        cursor = collection.find({
            "delete_at": {"$lte": datetime.utcnow()}
        })
        return await cursor.to_list(length=None)
    
    async def delete_pending_deletion(self, deletion_id: str):
        collection = db.get_collection(self.collection_name)
        from bson import ObjectId
        await collection.delete_one({"_id": ObjectId(deletion_id)})

deletion_ops = DeletionOperations()
