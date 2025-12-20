from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    admin_name = message.from_user.first_name
    
    welcome_text = f"""👋 Welcome, {admin_name}!

You are now in the Admin Panel.

Use the menu commands to manage:
• Generate Links
• Manage Resources
• Configure Settings
• Manage Users
• Broadcast Messages

Type /help for command list."""
    
    await message.answer(welcome_text)
