from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from shared.config import config
from shared.constants import NOT_AUTHORIZED_MESSAGE

class AdminAuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        
        if user_id not in config.ADMIN_IDS:
            if isinstance(event, Message):
                await event.answer(
                    NOT_AUTHORIZED_MESSAGE,
                    message_effect_id=config.NOT_AUTHORIZED_EFFECT
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(NOT_AUTHORIZED_MESSAGE, show_alert=True)
            return
        
        return await handler(event, data)
