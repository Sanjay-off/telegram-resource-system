from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin_bot.states import BanUserStates, UnbanUserStates
from admin_bot.keyboards import get_cancel_keyboard
from database.operations import user_ops

router = Router()

@router.message(Command("ban_user"))
async def cmd_ban_user(message: Message, state: FSMContext):
    await state.set_state(BanUserStates.waiting_for_user_id)
    await message.answer(
        "🚫 Please enter the user ID to ban:",
        reply_markup=get_cancel_keyboard()
    )

@router.message(BanUserStates.waiting_for_user_id)
async def process_ban_user(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer("❌ Invalid user ID. Please enter a valid number.")
        return
    
    user_exists = await user_ops.user_exists(user_id)
    
    if not user_exists:
        await message.answer(f"❌ User with ID {user_id} not found in database.")
        await state.clear()
        return
    
    await user_ops.ban_user(user_id)
    
    await message.answer(f"✅ User {user_id} has been banned successfully.")
    await state.clear()

@router.message(Command("unban_user"))
async def cmd_unban_user(message: Message, state: FSMContext):
    await state.set_state(UnbanUserStates.waiting_for_user_id)
    await message.answer(
        "✅ Please enter the user ID to unban:",
        reply_markup=get_cancel_keyboard()
    )

@router.message(UnbanUserStates.waiting_for_user_id)
async def process_unban_user(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer("❌ Invalid user ID. Please enter a valid number.")
        return
    
    user_exists = await user_ops.user_exists(user_id)
    
    if not user_exists:
        await message.answer(f"❌ User with ID {user_id} not found in database.")
        await state.clear()
        return
    
    await user_ops.unban_user(user_id)
    
    await message.answer(f"✅ User {user_id} has been unbanned successfully.")
    await state.clear()

@router.message(Command("verification_stats"))
async def cmd_verification_stats(message: Message):
    verified_count = await user_ops.count_verified_users()
    unverified_count = await user_ops.count_unverified_users()
    total_users = verified_count + unverified_count
    
    stats_text = f"""📊 Verification Statistics:

✅ Verified Users: {verified_count}
❌ Unverified Users: {unverified_count}
👥 Total Users: {total_users}

Verification Rate: {(verified_count/total_users*100) if total_users > 0 else 0:.2f}%"""
    
    await message.answer(stats_text)
