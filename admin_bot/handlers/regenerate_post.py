from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin_bot.states import RegeneratePostStates
from admin_bot.keyboards import get_download_button, get_cancel_keyboard
from database.operations import file_ops
from shared.config import config
from shared.constants import POST_TEMPLATE

router = Router()

@router.message(Command("regenerate_post"))
async def cmd_regenerate_post(message: Message, state: FSMContext):
    await state.set_state(RegeneratePostStates.waiting_for_post_no)
    await message.answer(
        "🔢 Please enter the post number to regenerate:",
        reply_markup=get_cancel_keyboard()
    )

@router.message(RegeneratePostStates.waiting_for_post_no)
async def process_regenerate(message: Message, state: FSMContext):
    try:
        post_no = int(message.text)
    except ValueError:
        await message.answer("❌ Invalid post number. Please enter a valid number.")
        return
    
    file_data = await file_ops.get_file_by_post_no(post_no)
    
    if not file_data:
        await message.answer(f"❌ Post number {post_no} does not exist in the database.")
        await state.clear()
        return
    
    template = POST_TEMPLATE.format(
        post_no=file_data['post_no'],
        description=file_data['description'],
        extra_message=file_data['extra_message']
    )
    
    if file_data.get('is_batch', False):
        keyboard = get_download_button(config.USER_BOT_USERNAME, file_data['unique_id'])
        await message.answer(
            f"✅ Batch Post Template:\n\n{template}",
            reply_markup=keyboard
        )
    else:
        keyboard = get_download_button(config.USER_BOT_USERNAME, file_data['unique_id'])
        await message.answer(
            f"✅ Post Template:\n\n{template}",
            reply_markup=keyboard
        )
    
    await state.clear()
