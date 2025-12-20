from datetime import datetime
from shared.utils import get_expiry_date

class TokenModel:
    COLLECTION_NAME = "tokens"
    
    @staticmethod
    def create_document(
        token: str,
        unique_id: str,
        created_by: int,
        status: str = "not_used"
    ) -> dict:
        return {
            "created_at": datetime.utcnow(),
            "token": token,
            "unique_id": unique_id,
            "created_by": created_by,
            "status": status,
            "expires_at": get_expiry_date(2)
        }
    
    @staticmethod
    def update_status(status: str) -> dict:
        return {
            "$set": {"status": status}
        }
