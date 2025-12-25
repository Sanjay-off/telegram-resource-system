from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from admin_bot.states import GenerateBatchStates
from admin_bot.keyboards import get_download_button, get_finish_batch_keyboard, get_cancel_keyboard
from database.operations import file_ops
from database.models import FileModel
from shared.utils import generate_unique_id, get_file_type, get_file_id
from shared.config import config
from shared.constants import POST_TEMPLATE

router = Router()

@router.message(Command("generate_batch"))
async def cmd_generate_batch(message: Message, state: FSMContext):
    await state.set_state(GenerateBatchStates.waiting_for_post_no)
    await message.answer(
        "🔢 Please enter the post number for this batch (must be unique):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(GenerateBatchStates.waiting_for_post_no)
async def process_batch_post_no(message: Message, state: FSMContext):
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
    await state.set_state(GenerateBatchStates.waiting_for_description)
    await message.answer("📝 Please enter the batch description:")

@router.message(GenerateBatchStates.waiting_for_description)
async def process_batch_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(GenerateBatchStates.waiting_for_extra_message)
    await message.answer("💬 Please enter the extra message:")

@router.message(GenerateBatchStates.waiting_for_extra_message)
async def process_batch_extra_message(message: Message, state: FSMContext):
    await state.update_data(extra_message=message.text, batch_files=[])
    await state.set_state(GenerateBatchStates.waiting_for_resources)
    await message.answer(
        "📤 Please upload resources one by one. Click 'Finish Batch' when done.",
        reply_markup=get_finish_batch_keyboard()
    )

@router.message(GenerateBatchStates.waiting_for_resources)
async def process_batch_resource(message: Message, state: FSMContext, bot: Bot):
    file_type = get_file_type(message)
    
    if file_type == "unknown":
        await message.answer("❌ Invalid file type. Please send a valid resource.")
        return
    
    file_id = get_file_id(message)
    text_content = message.text if file_type == "text" else None
    
    forwarded = await bot.forward_message(
        chat_id=config.STORAGE_CHANNEL_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
    
    data = await state.get_data()
    batch_files = data.get('batch_files', [])
    
    batch_file_entry = FileModel.create_batch_file_entry(
        file_type=file_type,
        file_id=file_id,
        text_content=text_content,
        channel_message_id=forwarded.message_id
    )
    
    batch_files.append(batch_file_entry)
    await state.update_data(batch_files=batch_files)
    
    await message.answer(
        f"✅ Resource {len(batch_files)} added. Upload more or click 'Finish Batch'.",
        reply_markup=get_finish_batch_keyboard()
    )

@router.callback_query(F.data == "finish_batch")
async def finish_batch(callback: CallbackQuery, state: FSMContext,bot: Bot):
    data = await state.get_data()
    batch_files = data.get('batch_files', [])
    
    if not batch_files:
        await callback.answer("❌ No resources uploaded yet!", show_alert=True)
        return
    
    unique_id = generate_unique_id(30)
    
    file_data = FileModel.create_document(
        unique_id=unique_id,
        post_no=data['post_no'],
        description=data['description'],
        extra_message=data['extra_message'],
        file_type="batch",
        file_id=None,
        text_content=None,
        channel_message_id=batch_files[0]['channel_message_id'],
        is_batch=True,
        batch_files=batch_files
    )
    
    await file_ops.create_file(file_data)
    
    template = POST_TEMPLATE.format(
        post_no=data['post_no'],
        description=data['description'],
        extra_message=data['extra_message']
    )
    
    await callback.message.edit_text(
        template,
        parse_mode="HTML",
        reply_markup=get_download_button(config.USER_BOT_USERNAME, unique_id)
    )

    await bot.send_photo(
            chat_id=config.PUBLIC_CHANNEL_USERNAME,
            photo=config.COVER_PHOTO,
            caption=template,
            parse_mode="HTML",
            reply_markup=get_download_button(
                config.USER_BOT_USERNAME,
                unique_id
            )
        )
    
    await state.clear()
    await callback.answer()
