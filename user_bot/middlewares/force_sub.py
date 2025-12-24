from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message 
from aiogram.enums import ChatMemberStatus
from database.operations import config_ops, user_ops
from user_bot.keyboards import get_force_sub_keyboard
from shared.constants import FORCE_SUB_MESSAGE
from shared.utils import format_username, extract_deeplink_payload
from shared.config import config

class ForceSubMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.exempt_commands = ['start', 'help']
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.text and any(cmd in event.text for cmd in self.exempt_commands):
            return await handler(event, data)
        
        user_id = event.from_user.id
        bot: Bot = data.get('bot')
        
        channels = await config_ops.get_force_sub_channels()
        
        if not channels:
            return await handler(event, data)
        
        not_subscribed = []
        
        for channel in channels:
            channel_id = channel['channel_id']
            
            try:
                member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
                
                if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                    not_subscribed.append(channel)
                elif member.status == ChatMemberStatus.MEMBER:
                    await user_ops.update_force_sub_status(user_id, channel_id, True)
                elif member.status == ChatMemberStatus.RESTRICTED:
                    user = await user_ops.get_user(user_id)
                    if user and channel_id in user.get('join_requests', []):
                        await user_ops.update_force_sub_status(user_id, channel_id, True)
                    else:
                        not_subscribed.append(channel)
                else:
                    await user_ops.update_force_sub_status(user_id, channel_id, True)
                    
            except Exception as e:
                print(f"Error checking channel membership for {channel_id}: {e}")
                not_subscribed.append(channel)
        
        if not_subscribed:
            username = format_username(event.from_user)
            message_text = FORCE_SUB_MESSAGE.format(username=username)
            
            data['force_sub_blocked'] = True
            data['not_subscribed_channels'] = not_subscribed
            
            unique_id = ""
            if event.text and '/start' in event.text:
                payload = extract_deeplink_payload(event.text)
                if payload and not payload.startswith("verify_") and payload != "newToken":
                    unique_id = payload
            
            await event.answer(
                message_text,
                parse_mode="HTML",
                reply_markup=get_force_sub_keyboard(not_subscribed, unique_id, config.USER_BOT_USERNAME)
            )
            return
        
        return await handler(event, data)
