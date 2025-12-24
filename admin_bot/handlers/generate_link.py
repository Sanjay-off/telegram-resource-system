from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from admin_bot.states import GenerateLinkStates
from admin_bot.keyboards import get_download_button, get_cancel_keyboard
from database.operations import file_ops
from database.models import FileModel
from shared.utils import generate_unique_id, get_file_type, get_file_id
from shared.config import config
from shared.constants import POST_TEMPLATE

router = Router()

@router.message(Command("generate_link"))
async def cmd_generate_link(message: Message, state: FSMContext):
    await state.set_state(GenerateLinkStates.waiting_for_resource)
    await message.answer(
        "📤 Please upload the resource (document/video/audio/photo/text):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(GenerateLinkStates.waiting_for_resource)
async def process_resource(message: Message, state: FSMContext):
    file_type = get_file_type(message)
    
    if file_type == "unknown":
        await message.answer("❌ Invalid file type. Please send a valid resource.")
        return
    
    file_id = get_file_id(message)
    text_content = message.text if file_type == "text" else None
    
    await state.update_data(
        file_type=file_type,
        file_id=file_id,
        text_content=text_content,
        temp_message=message
    )
    
    await state.set_state(GenerateLinkStates.waiting_for_post_no)
    await message.answer("🔢 Please enter the post number (must be unique):")

@router.message(GenerateLinkStates.waiting_for_post_no)
async def process_post_no(message: Message, state: FSMContext):
    try:
        post_no = int(message.text)
    except ValueError:
        await message.answer("❌ Invalid post number. Please enter a valid number.")
        return
    
    exists = await file_ops.check_post_no_exists(post_no)
    if exists:
        await message.answer(f"❌ Post number {post_no} already exists. Please use a different number.")
        return
    
    await state.update_data(post_no=post_no)
    await state.set_state(GenerateLinkStates.waiting_for_description)
    await message.answer("📝 Please enter the description:")

@router.message(GenerateLinkStates.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(GenerateLinkStates.waiting_for_extra_message)
    await message.answer("💬 Please enter the extra message:")

@router.message(GenerateLinkStates.waiting_for_extra_message)
async def process_extra_message(message: Message, state: FSMContext, bot: Bot):
    extra_message = message.text
    data = await state.get_data()
    
    temp_message = data['temp_message']
    file_type = data['file_type']
    file_id = data['file_id']
    text_content = data['text_content']
    post_no = data['post_no']
    description = data['description']
    
    forwarded = await bot.forward_message(
        chat_id=config.STORAGE_CHANNEL_ID,
        from_chat_id=temp_message.chat.id,
        message_id=temp_message.message_id
    )
    
    unique_id = generate_unique_id(30)
    
    file_data = FileModel.create_document(
        unique_id=unique_id,
        post_no=post_no,
        description=description,
        extra_message=extra_message,
        file_type=file_type,
        file_id=file_id,
        text_content=text_content,
        channel_message_id=forwarded.message_id,
        is_batch=False
    )
    
    await file_ops.create_file(file_data)
    
    template = POST_TEMPLATE.format(
        post_no=post_no,
        description=description,
        extra_message=extra_message
    )
    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="AgACAgUAAxkBAAIG0mlLncS1vcxKAgJDX3bgqXfR51xCAALOC2sbv5NYVrk-ViWJxqBrAQADAgADeQADNgQ",
        caption=template,
        parse_mode="HTML",
        reply_markup=get_download_button(config.USER_BOT_USERNAME, unique_id)
    )
    
    await state.clear()

@router.callback_query(F.data == "cancel")
async def cancel_operation(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Operation cancelled.")
    await callback.answer()
