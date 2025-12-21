from datetime import datetime

class TokenGeneratorCountModel:
    COLLECTION_NAME = "token_generator_count"
    
    @staticmethod
    def create_document(user_id: int) -> dict:
        return {
            "user_id": user_id,
            "token_generated": 1,
            "date": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        }
    
    @staticmethod
    def increment_count() -> dict:
        return {
            "$inc": {"token_generated": 1}
        }
