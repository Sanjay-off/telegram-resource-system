from datetime import datetime
from typing import Optional, List

class FileModel:
    COLLECTION_NAME = "files"
    
    @staticmethod
    def create_document(
        unique_id: str,
        post_no: int,
        description: str,
        extra_message: str,
        file_type: str,
        file_id: Optional[str],
        text_content: Optional[str],
        channel_message_id: int,
        is_batch: bool = False,
        batch_files: Optional[List[dict]] = None
    ) -> dict:
        return {
            "unique_id": unique_id,
            "post_no": post_no,
            "description": description,
            "extra_message": extra_message,
            "file_type": file_type,
            "file_id": file_id,
            "text_content": text_content,
            "channel_message_id": channel_message_id,
            "is_batch": is_batch,
            "batch_files": batch_files or [],
            "created_at": datetime.utcnow()
        }
    
    @staticmethod
    def create_batch_file_entry(
        file_type: str,
        file_id: Optional[str],
        text_content: Optional[str],
        channel_message_id: int
    ) -> dict:
        return {
            "file_type": file_type,
            "file_id": file_id,
            "text_content": text_content,
            "channel_message_id": channel_message_id
        }
