from datetime import datetime, timedelta
from typing import Optional

class BroadcastModel:
    COLLECTION_NAME = "broadcasts"
    
    @staticmethod
    def create_document(
        message_id: int,
        file_id: Optional[str],
        text: Optional[str],
        caption: Optional[str],
        duration_hours: int,
        channel_message_id: int
    ) -> dict:
        created_at = datetime.utcnow()
        delete_at = created_at + timedelta(hours=duration_hours)
        
        return {
            "message_id": message_id,
            "file_id": file_id,
            "text": text,
            "caption": caption,
            "duration_hours": duration_hours,
            "channel_message_id": channel_message_id,
            "created_at": created_at,
            "delete_at": delete_at
        }
