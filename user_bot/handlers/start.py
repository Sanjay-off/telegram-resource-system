from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from database.operations import user_ops
from database.models import UserModel
from shared.constants import USER_START_MESSAGE
from shared.utils import format_username, extract_deeplink_payload
from shared.config import config

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or "User"
    
    user_exists = await user_ops.user_exists(user_id)
    
    if not user_exists:
        user_data = UserModel.create_document(
            user_id=user_id,
            username=username,
            first_name=first_name
        )
        await user_ops.create_user(user_data)
    
    command_text = message.text
    payload = extract_deeplink_payload(command_text)
    
    if payload:
        from user_bot.handlers.resource_delivery import handle_resource_request
        from user_bot.handlers.verify_handler import handle_verify_callback
        
        if payload.startswith("verify_"):
            await handle_verify_callback(message, payload)
        elif payload == "newToken":
            from user_bot.handlers.token_handler import handle_new_token_request
            await handle_new_token_request(message)
        else:
            await handle_resource_request(message, payload)
    else:
        username_formatted = format_username(message.from_user)
        welcome_text = USER_START_MESSAGE.format(username=username_formatted)
        
        await message.answer(
            welcome_text,
            message_effect_id=config.FIRE_EFFECT
        )
