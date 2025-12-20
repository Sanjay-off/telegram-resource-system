from typing import Optional, Any, List
from database.connection import db
from database.models.admin_config import AdminConfigModel
from shared.constants import (
    DEFAULT_MEDIA_ACCESS_COUNT,
    DEFAULT_DELETION_TIME,
    DEFAULT_TOKEN_GENERATION_LIMIT,
    DEFAULT_ZIP_PASSWORD
)

class ConfigOperations:
    def __init__(self):
        self.collection_name = AdminConfigModel.COLLECTION_NAME
    
    async def get_config(self, key: str) -> Optional[Any]:
        collection = db.get_collection(self.collection_name)
        result = await collection.find_one({"key": key})
        return result["value"] if result else None
    
    async def set_config(self, key: str, value: Any):
        collection = db.get_collection(self.collection_name)
        await collection.update_one(
            {"key": key},
            {"$set": {"value": value}},
            upsert=True
        )
    
    async def get_force_sub_channels(self) -> List[dict]:
        channels = await self.get_config(AdminConfigModel.KEY_FORCE_SUB_CHANNELS)
        return channels if channels else []
    
    async def add_force_sub_channel(self, channel_id: int, placeholder: str):
        channels = await self.get_force_sub_channels()
        channels.append({
            "channel_id": channel_id,
            "placeholder": placeholder
        })
        await self.set_config(AdminConfigModel.KEY_FORCE_SUB_CHANNELS, channels)
    
    async def remove_force_sub_channel(self, channel_id: int):
        channels = await self.get_force_sub_channels()
        channels = [ch for ch in channels if ch["channel_id"] != channel_id]
        await self.set_config(AdminConfigModel.KEY_FORCE_SUB_CHANNELS, channels)
    
    async def get_media_access_count(self) -> int:
        count = await self.get_config(AdminConfigModel.KEY_MEDIA_ACCESS_COUNT)
        return count if count else DEFAULT_MEDIA_ACCESS_COUNT
    
    async def get_deletion_time(self) -> int:
        time = await self.get_config(AdminConfigModel.KEY_DELETION_TIME)
        return time if time else DEFAULT_DELETION_TIME
    
    async def get_zip_password(self) -> str:
        password = await self.get_config(AdminConfigModel.KEY_ZIP_PASSWORD)
        return password if password else DEFAULT_ZIP_PASSWORD
    
    async def get_token_generation_limit(self) -> int:
        limit = await self.get_config(AdminConfigModel.KEY_TOKEN_GENERATION_LIMIT)
        return limit if limit else DEFAULT_TOKEN_GENERATION_LIMIT
    
    async def get_how_to_verify_link(self) -> Optional[str]:
        return await self.get_config(AdminConfigModel.KEY_HOW_TO_VERIFY_LINK)

config_ops = ConfigOperations()
