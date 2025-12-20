from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List

def get_download_button(bot_username: str, unique_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="Download",
        url=f"https://t.me/{bot_username}?start={unique_id}"
    ))
    return keyboard.as_markup()

def get_force_sub_channels_keyboard(channels: List[dict]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    for channel in channels:
        keyboard.add(InlineKeyboardButton(
            text=f"Remove {channel['placeholder']}",
            callback_data=f"remove_channel_{channel['channel_id']}"
        ))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="❌ Cancel",
        callback_data="cancel"
    ))
    return keyboard.as_markup()

def get_finish_batch_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="✅ Finish Batch", callback_data="finish_batch"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")
    )
    return keyboard.as_markup()
