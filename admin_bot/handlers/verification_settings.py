from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin_bot.states import SetMediaAccessStates, SetPaidAccessStates, SetHowToVerifyStates
from admin_bot.keyboards import get_cancel_keyboard
from database.operations import config_ops, user_ops
from database.models import AdminConfigModel

router = Router()

@router.message(Command("set_free_media_access"))
async def cmd_set_free_media_access(message: Message, state: FSMContext):
    await state.set_state(SetMediaAccessStates.waiting_for_count)
    await message.answer(
        "🔢 Please enter the free media access count (number of resources users get after verification):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(SetMediaAccessStates.waiting_for_count)
async def process_media_access_count(message: Message, state: FSMContext):
    try:
        count = int(message.text)
        if count <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Invalid count. Please enter a positive number.")
        return
    
    await config_ops.set_config(AdminConfigModel.KEY_MEDIA_ACCESS_COUNT, count)
    
    await message.answer(f"✅ Free media access count set to {count}")
    await state.clear()

@router.message(Command("set_paid_access"))
async def cmd_set_paid_access(message: Message, state: FSMContext):
    await state.set_state(SetPaidAccessStates.waiting_for_user_id)
    await message.answer(
        "👤 Please enter the user ID:",
        reply_markup=get_cancel_keyboard()
    )

@router.message(SetPaidAccessStates.waiting_for_user_id)
async def process_paid_user_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer("❌ Invalid user ID. Please enter a valid number.")
        return
    
    user_exists = await user_ops.user_exists(user_id)
    
    if not user_exists:
        await message.answer(f"❌ User with ID {user_id} not found in database.")
        return
    
    await state.update_data(user_id=user_id)
    await state.set_state(SetPaidAccessStates.waiting_for_count)
    await message.answer("🔢 Please enter the media access count to set:")

@router.message(SetPaidAccessStates.waiting_for_count)
async def process_paid_access_count(message: Message, state: FSMContext):
    try:
        count = int(message.text)
        if count < 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Invalid count. Please enter a non-negative number.")
        return
    
    data = await state.get_data()
    user_id = data['user_id']
    
    await user_ops.set_user_access_count(user_id, count)
    
    await message.answer(f"✅ User {user_id} now has {count} media access count.")
    await state.clear()

@router.message(Command("set_how_to_verify"))
async def cmd_set_how_to_verify(message: Message, state: FSMContext):
    await state.set_state(SetHowToVerifyStates.waiting_for_link)
    await message.answer(
        "🔗 Please send the deeplink for 'How to Verify' button (e.g., https://t.me/yourchannel/123):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(SetHowToVerifyStates.waiting_for_link)
async def process_how_to_verify_link(message: Message, state: FSMContext):
    link = message.text.strip()
    
    if not link.startswith('http'):
        await message.answer("❌ Invalid link. Please send a valid URL.")
        return
    
    await config_ops.set_config(AdminConfigModel.KEY_HOW_TO_VERIFY_LINK, link)
    
    await message.answer(f"✅ 'How to Verify' link set to:\n{link}")
    await state.clear()
