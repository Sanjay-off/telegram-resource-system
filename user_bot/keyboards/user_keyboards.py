from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Optional

def get_force_sub_keyboard(channels: List[dict], unique_id: str, bot_username: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    for channel in channels:
        channel_id = str(channel['channel_id']).replace('-100', '')
        keyboard.add(InlineKeyboardButton(
            text=channel['placeholder'],
            url=f"https://t.me/c/{channel_id}/1"
        ))
    
    deeplink = f"https://t.me/{bot_username}?start={unique_id}"
    keyboard.add(InlineKeyboardButton(
        text="🔄 Try Again",
        url=deeplink
    ))
    
    keyboard.adjust(2)
    return keyboard.as_markup()

def get_verification_keyboard(verify_url: str, how_to_verify_link: Optional[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(
        text="✅ Verify Now",
        url=verify_url
    ))
    
    if how_to_verify_link:
        keyboard.add(InlineKeyboardButton(
            text="❓ How to Verify",
            url=how_to_verify_link
        ))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_deleted_message_keyboard(bot_username: str, unique_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    deeplink = f"https://t.me/{bot_username}?start={unique_id}"
    
    keyboard.row(
        InlineKeyboardButton(
            text="♻️ Click Here",
            url=deeplink
        ),
        InlineKeyboardButton(
            text="❌ Close",
            callback_data="close_message"
        )
    )
    
    return keyboard.as_markup()
