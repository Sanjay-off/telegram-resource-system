from datetime import datetime
from typing import Optional, Tuple
from database.operations import token_ops
from shared.constants import TOKEN_STATUS_BYPASSED, TOKEN_STATUS_VERIFIED, BYPASS_TIME_THRESHOLD
from shared.url_shortener import url_shortener

class TokenValidator:
    def __init__(self):
        self.whitelist_domains = url_shortener.get_whitelist_domains()
    
    async def validate_token(self, token: str, referer: Optional[str]) -> Tuple[bool, str, Optional[dict]]:
        token_data = await token_ops.get_token_by_token(token)
        
        if not token_data:
            return False, "not_found", None
        
        created_at = token_data.get('created_at')
        status = token_data.get('status')
        
        if status in [TOKEN_STATUS_VERIFIED, TOKEN_STATUS_BYPASSED]:
            return False, "already_used", token_data
        
        time_diff = (datetime.utcnow() - created_at).total_seconds()
        
        if time_diff < BYPASS_TIME_THRESHOLD:
            await token_ops.update_token_status(token, TOKEN_STATUS_BYPASSED)
            return False, "bypass_time", token_data
        
        if not referer:
            await token_ops.update_token_status(token, TOKEN_STATUS_BYPASSED)
            return False, "bypass_origin", token_data
        
        origin_valid = False
        for domain in self.whitelist_domains:
            if domain in referer:
                origin_valid = True
                break
        
        if not origin_valid:
            await token_ops.update_token_status(token, TOKEN_STATUS_BYPASSED)
            return False, "bypass_origin", token_data
        
        await token_ops.update_token_status(token, TOKEN_STATUS_VERIFIED)
        return True, "success", token_data
    
    def get_redirect_url(self, token_data: dict, bot_username: str) -> str:
        unique_id = token_data.get('unique_id')
        user_id = token_data.get('created_by')
        return f"https://t.me/{bot_username}?start=verify_{unique_id}_{user_id}"

token_validator = TokenValidator()
