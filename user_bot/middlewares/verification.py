from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from database.operations import user_ops, config_ops, token_ops
from database.models import TokenModel
from user_bot.keyboards import get_verification_keyboard
from shared.constants import VERIFICATION_MESSAGE
from shared.utils import format_username, generate_token, generate_unique_id
from shared.url_shortener import url_shortener
from shared.config import config

class VerificationMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.exempt_commands = ['start', 'help', 'create_new_token']
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.text and any(cmd in event.text for cmd in self.exempt_commands):
            return await handler(event, data)
        
        if data.get('force_sub_blocked'):
            return
        
        user_id = event.from_user.id
        
        user = await user_ops.get_user(user_id)
        
        if not user:
            return await handler(event, data)
        
        user_access_count = user.get('user_access_count', 0)
        
        if user_access_count > 0:
            return await handler(event, data)
        
        media_access_count = await config_ops.get_media_access_count()
        
        token = generate_token(35)
        unique_id = generate_unique_id(10)
        
        token_data = TokenModel.create_document(
            token=token,
            unique_id=unique_id,
            created_by=user_id
        )
        
        await token_ops.create_token(token_data)
        
        destination_url = f"http://{config.SERVER_HOST}:{config.SERVER_PORT}/redirect?token={token}"
        
        shortened_url = await url_shortener.shorten_url(destination_url)
        
        if not shortened_url:
            shortened_url = destination_url
        
        how_to_verify_link = await config_ops.get_how_to_verify_link()
        
        username = format_username(event.from_user)
        message_text = VERIFICATION_MESSAGE.format(
            username=username,
            media_access_count=media_access_count
        )
        
        await event.answer(
            message_text,
            reply_markup=get_verification_keyboard(shortened_url, how_to_verify_link)
        )
        
        return
