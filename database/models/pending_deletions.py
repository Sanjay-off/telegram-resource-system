from datetime import datetime
from typing import List

class PendingDeletionModel:
    COLLECTION_NAME = "pending_deletions"
    
    @staticmethod
    def create_document(
        user_id: int,
        chat_id: int,
        message_ids: List[int],
        delete_at: datetime,
        unique_id: str
    ) -> dict:
        return {
            "user_id": user_id,
            "chat_id": chat_id,
            "message_ids": message_ids,
            "delete_at": delete_at,
            "unique_id": unique_id,
            "created_at": datetime.utcnow()
        }
