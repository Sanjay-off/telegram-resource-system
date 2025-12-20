from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin_bot.states import SetPasswordStates, SetDeletionTimeStates, SetTokenLimitStates
from admin_bot.keyboards import get_cancel_keyboard
from database.operations import config_ops
from database.models import AdminConfigModel

router = Router()

@router.message(Command("set_password"))
async def cmd_set_password(message: Message, state: FSMContext):
    await state.set_state(SetPasswordStates.waiting_for_password)
    await message.answer(
        "🔐 Please enter the new password for ZIP files:",
        reply_markup=get_cancel_keyboard()
    )

@router.message(SetPasswordStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip()
    
    if len(password) < 4:
        await message.answer("❌ Password must be at least 4 characters long.")
        return
    
    await config_ops.set_config(AdminConfigModel.KEY_ZIP_PASSWORD, password)
    
    await message.answer(f"✅ ZIP password set to: {password}")
    await state.clear()

@router.message(Command("set_deletion_time"))
async def cmd_set_deletion_time(message: Message, state: FSMContext):
    await state.set_state(SetDeletionTimeStates.waiting_for_time)
    await message.answer(
        "⏱ Please enter the deletion time in minutes (resources will be auto-deleted after this time):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(SetDeletionTimeStates.waiting_for_time)
async def process_deletion_time(message: Message, state: FSMContext):
    try:
        deletion_time = int(message.text)
        if deletion_time <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Invalid time. Please enter a positive number.")
        return
    
    await config_ops.set_config(AdminConfigModel.KEY_DELETION_TIME, deletion_time)
    
    await message.answer(f"✅ Deletion time set to {deletion_time} minutes")
    await state.clear()

@router.message(Command("set_token_limit"))
async def cmd_set_token_limit(message: Message, state: FSMContext):
    await state.set_state(SetTokenLimitStates.waiting_for_limit)
    await message.answer(
        "🎫 Please enter the daily token generation limit per user:",
        reply_markup=get_cancel_keyboard()
    )

@router.message(SetTokenLimitStates.waiting_for_limit)
async def process_token_limit(message: Message, state: FSMContext):
    try:
        limit = int(message.text)
        if limit <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Invalid limit. Please enter a positive number.")
        return
    
    await config_ops.set_config(AdminConfigModel.KEY_TOKEN_GENERATION_LIMIT, limit)
    
    await message.answer(f"✅ Daily token generation limit set to {limit}")
    await state.clear()
