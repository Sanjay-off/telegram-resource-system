from datetime import datetime

class TokenGeneratorCountModel:
    COLLECTION_NAME = "token_generator_count"
    
    @staticmethod
    def create_document(user_id: int) -> dict:
        return {
            "user_id": user_id,
            "token_generated": 1,
            "date": datetime.utcnow().date()
        }
    
    @staticmethod
    def increment_count() -> dict:
        return {
            "$inc": {"token_generated": 1}
        }
