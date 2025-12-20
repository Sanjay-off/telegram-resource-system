from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from shared.constants import USER_HELP_MESSAGE
from shared.utils import format_username

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    username = format_username(message.from_user)
    help_text = USER_HELP_MESSAGE.format(username=username)
    
    await message.answer(help_text)
