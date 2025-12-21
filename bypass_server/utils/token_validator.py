from datetime import datetime
from typing import Optional, Tuple
from database.connection import db
from shared.constants import TOKEN_STATUS_BYPASSED, TOKEN_STATUS_VERIFIED, BYPASS_TIME_THRESHOLD
from shared.url_shortener import url_shortener

class TokenValidator:
    def __init__(self):
        self.whitelist_domains = url_shortener.get_whitelist_domains()
    
    def validate_token(self, token: str, referer: Optional[str]) -> Tuple[bool, str, Optional[dict]]:
        """
        Validate token using SYNC database operations
        Returns: (is_valid, status, token_data)
        """
        # Use sync collection
        collection = db.get_sync_collection('tokens')
        
        # Get token from database (SYNC)
        token_data = collection.find_one({"token": token})
        
        if not token_data:
            return False, "not_found", None
        
        created_at = token_data.get('created_at')
        status = token_data.get('status')
        
        # Check if already used
        if status in [TOKEN_STATUS_VERIFIED, TOKEN_STATUS_BYPASSED]:
            return False, "already_used", token_data
        
        # Time-based bypass detection
        time_diff = (datetime.utcnow() - created_at).total_seconds()
        
        if time_diff < BYPASS_TIME_THRESHOLD:
            # Mark as bypassed (SYNC)
            collection.update_one(
                {"token": token},
                {"$set": {"status": TOKEN_STATUS_BYPASSED}}
            )
            return False, "bypass_time", token_data
        
        # Origin-based bypass detection
        if not referer:
            collection.update_one(
                {"token": token},
                {"$set": {"status": TOKEN_STATUS_BYPASSED}}
            )
            return False, "bypass_origin", token_data
        
        # Check if referer is in whitelist
        origin_valid = False
        for domain in self.whitelist_domains:
            if domain in referer:
                origin_valid = True
                break
        
        if not origin_valid:
            collection.update_one(
                {"token": token},
                {"$set": {"status": TOKEN_STATUS_BYPASSED}}
            )
            return False, "bypass_origin", token_data
        
        # Valid - mark as verified
        collection.update_one(
            {"token": token},
            {"$set": {"status": TOKEN_STATUS_VERIFIED}}
        )
        return True, "success", token_data
    
    def get_redirect_url(self, token_data: dict, bot_username: str) -> str:
        """Generate redirect URL to bot"""
        if not token_data:
            return f"https://t.me/{bot_username}?start=newToken"
        
        unique_id = token_data.get('unique_id')
        user_id = token_data.get('created_by')
        return f"https://t.me/{bot_username}?start=verify_{unique_id}_{user_id}"

token_validator = TokenValidator()