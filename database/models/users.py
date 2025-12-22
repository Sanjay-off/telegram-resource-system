from datetime import datetime
from typing import Dict, List

class UserModel:
    COLLECTION_NAME = "users"
    
    @staticmethod
    def create_document(
        user_id: int,
        username: str,
        first_name: str
    ) -> dict:
        return {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "user_access_count": 0,
            "is_banned": False,
            "joined_at": datetime.utcnow(),
            "force_sub_status": {},
            "join_requests": []
        }
    
    @staticmethod
    def update_access_count(increment: int) -> dict:
        return {
            "$inc": {"user_access_count": increment}
        }
    
    @staticmethod
    def set_access_count(count: int) -> dict:
        return {
            "$inc": {"user_access_count": count}
        }
    
    @staticmethod
    def ban_user() -> dict:
        return {
            "$set": {"is_banned": True}
        }
    
    @staticmethod
    def unban_user() -> dict:
        return {
            "$set": {"is_banned": False}
        }
    
    @staticmethod
    def add_join_request(channel_id: int) -> dict:
        return {
            "$addToSet": {"join_requests": channel_id}
        }
    
    @staticmethod
    def update_force_sub_status(channel_id: int, status: bool) -> dict:
        return {
            "$set": {f"force_sub_status.{channel_id}": status}
        }
