from typing import Optional, List
from database.connection import db
from database.models.users import UserModel

class UserOperations:
    def __init__(self):
        self.collection_name = UserModel.COLLECTION_NAME
    
    async def create_user(self, user_data: dict) -> str:
        collection = db.get_collection(self.collection_name)
        result = await collection.insert_one(user_data)
        return str(result.inserted_id)
    
    async def get_user(self, user_id: int) -> Optional[dict]:
        collection = db.get_collection(self.collection_name)
        return await collection.find_one({"user_id": user_id})
    
    async def user_exists(self, user_id: int) -> bool:
        collection = db.get_collection(self.collection_name)
        count = await collection.count_documents({"user_id": user_id})
        return count > 0
    
    async def update_user_access_count(self, user_id: int, increment: int):
        collection = db.get_collection(self.collection_name)
        await collection.update_one(
            {"user_id": user_id},
            UserModel.update_access_count(increment)
        )
    
    async def set_user_access_count(self, user_id: int, count: int):
        collection = db.get_collection(self.collection_name)
        await collection.update_one(
            {"user_id": user_id},
            UserModel.set_access_count(count)
        )
    
    async def ban_user(self, user_id: int):
        collection = db.get_collection(self.collection_name)
        await collection.update_one(
            {"user_id": user_id},
            UserModel.ban_user()
        )
    
    async def unban_user(self, user_id: int):
        collection = db.get_collection(self.collection_name)
        await collection.update_one(
            {"user_id": user_id},
            UserModel.unban_user()
        )
    
    async def add_join_request(self, user_id: int, channel_id: int):
        collection = db.get_collection(self.collection_name)
        await collection.update_one(
            {"user_id": user_id},
            UserModel.add_join_request(channel_id)
        )
    
    async def update_force_sub_status(self, user_id: int, channel_id: int, status: bool):
        collection = db.get_collection(self.collection_name)
        await collection.update_one(
            {"user_id": user_id},
            UserModel.update_force_sub_status(channel_id, status)
        )
    
    async def get_all_users(self) -> List[dict]:
        collection = db.get_collection(self.collection_name)
        cursor = collection.find({})
        return await cursor.to_list(length=None)
    
    async def count_verified_users(self) -> int:
        collection = db.get_collection(self.collection_name)
        return await collection.count_documents({"user_access_count": {"$gt": 0}})
    
    async def count_unverified_users(self) -> int:
        collection = db.get_collection(self.collection_name)
        return await collection.count_documents({"user_access_count": 0})

user_ops = UserOperations()
