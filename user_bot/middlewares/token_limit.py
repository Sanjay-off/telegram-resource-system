from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from database.operations import token_ops, config_ops

class TokenLimitMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not (event.text and 'create_new_token' in event.text):
            return await handler(event, data)
        
        user_id = event.from_user.id
        
        token_count = await token_ops.get_user_token_count_today(user_id)
        token_limit = await config_ops.get_token_generation_limit()
        
        if token_count >= token_limit:
            await event.answer(
                f"❌ You have reached your daily token generation limit ({token_limit} tokens).\n"
                f"Please try again tomorrow."
            )
            return
        
        return await handler(event, data)
