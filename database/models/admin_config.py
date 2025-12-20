from typing import Any, List, Dict

class AdminConfigModel:
    COLLECTION_NAME = "admin_config"
    
    KEY_FORCE_SUB_CHANNELS = "force_sub_channels"
    KEY_MEDIA_ACCESS_COUNT = "media_access_count"
    KEY_ZIP_PASSWORD = "zip_password"
    KEY_DELETION_TIME = "deletion_time"
    KEY_HOW_TO_VERIFY_LINK = "how_to_verify_link"
    KEY_TOKEN_GENERATION_LIMIT = "token_generation_limit"
    
    @staticmethod
    def create_config(key: str, value: Any) -> dict:
        return {
            "key": key,
            "value": value
        }
    
    @staticmethod
    def add_force_sub_channel(channel_id: int, placeholder: str) -> Dict:
        return {
            "channel_id": channel_id,
            "placeholder": placeholder
        }
