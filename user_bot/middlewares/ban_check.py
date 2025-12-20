from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from database.operations import user_ops

class BanCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        
        user = await user_ops.get_user(user_id)
        
        if user and user.get('is_banned', False):
            await event.answer("🚫 You are banned from using this bot.")
            return
        
        return await handler(event, data)
