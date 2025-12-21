from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.operations import token_ops, config_ops
from database.models import TokenModel
from user_bot.keyboards import get_verification_keyboard
from shared.constants import VERIFICATION_MESSAGE
from shared.utils import format_username, generate_token, generate_unique_id
from shared.url_shortener import url_shortener
from shared.config import config

router = Router()

@router.message(Command("create_new_token"))
async def cmd_create_new_token(message: Message):
    await handle_new_token_request(message)

async def handle_new_token_request(message: Message):
    user_id = message.from_user.id
    
    await token_ops.increment_user_token_count(user_id)
    
    media_access_count = await config_ops.get_media_access_count()
    
    token = generate_token(35)
    unique_id = generate_unique_id(10)
    
    token_data = TokenModel.create_document(
        token=token,
        unique_id=unique_id,
        created_by=user_id
    )
    
    await token_ops.create_token(token_data)
    
    destination_url = f"https://{config.SERVER_HOST}:{config.SERVER_PORT}/redirect?token={token}"
    
    shortened_url = await url_shortener.shorten_url(destination_url)
    
    if not shortened_url:
        shortened_url = destination_url
    
    how_to_verify_link = await config_ops.get_how_to_verify_link()
    
    username = format_username(message.from_user)
    message_text = VERIFICATION_MESSAGE.format(
        username=username,
        media_access_count=media_access_count
    )
    
    await message.answer(
        message_text,
        reply_markup=get_verification_keyboard(shortened_url, how_to_verify_link)
    )
