from typing import Optional
from datetime import datetime
from database.connection import db
from database.models.tokens import TokenModel
from database.models.token_generator_count import TokenGeneratorCountModel

class TokenOperations:
    def __init__(self):
        self.collection_name = TokenModel.COLLECTION_NAME
        self.count_collection = TokenGeneratorCountModel.COLLECTION_NAME
    
    async def create_token(self, token_data: dict) -> str:
        collection = db.get_collection(self.collection_name)
        result = await collection.insert_one(token_data)
        return str(result.inserted_id)
    
    async def get_token_by_token(self, token: str) -> Optional[dict]:
        collection = db.get_collection(self.collection_name)
        return await collection.find_one({"token": token})
    
    async def get_token_by_unique_id_and_user(self, unique_id: str, user_id: int) -> Optional[dict]:
        collection = db.get_collection(self.collection_name)
        return await collection.find_one({
            "unique_id": unique_id,
            "created_by": user_id
        })
    
    async def update_token_status(self, token: str, status: str):
        collection = db.get_collection(self.collection_name)
        await collection.update_one(
            {"token": token},
            TokenModel.update_status(status)
        )
    
    async def delete_token(self, token: str):
        collection = db.get_collection(self.collection_name)
        await collection.delete_one({"token": token})
    
    async def delete_expired_and_used_tokens(self):
        collection = db.get_collection(self.collection_name)
        await collection.delete_many({
            "expires_at": {"$lt": datetime.utcnow()},
            "status": {"$in": ["verified", "bypassed"]}
        })
    
    async def get_user_token_count_today(self, user_id: int) -> int:
        collection = db.get_collection(self.count_collection)
        today = datetime.utcnow().date()
        
        result = await collection.find_one({
            "user_id": user_id,
            "date": today
        })
        
        return result["token_generated"] if result else 0
    
    async def increment_user_token_count(self, user_id: int):
        collection = db.get_collection(self.count_collection)
        today = datetime.utcnow().date()
        
        existing = await collection.find_one({
            "user_id": user_id,
            "date": today
        })
        
        if existing:
            await collection.update_one(
                {"user_id": user_id, "date": today},
                TokenGeneratorCountModel.increment_count()
            )
        else:
            await collection.insert_one(
                TokenGeneratorCountModel.create_document(user_id)
            )
    
    async def clear_token_counts(self):
        collection = db.get_collection(self.count_collection)
        yesterday = datetime.utcnow().date()
        await collection.delete_many({"date": {"$lt": yesterday}})

token_ops = TokenOperations()
