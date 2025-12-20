from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from database.operations import file_ops, user_ops, deletion_ops, config_ops
from database.models import PendingDeletionModel
from user_bot.keyboards import get_deleted_message_keyboard
from shared.constants import WARNING_MESSAGE, DELETED_MESSAGE
from shared.utils import get_deletion_time, is_zip_file
from shared.config import config

router = Router()

async def handle_resource_request(message: Message, unique_id: str):
    user_id = message.from_user.id
    bot: Bot = message.bot
    
    file_data = await file_ops.get_file_by_unique_id(unique_id)
    
    if not file_data:
        await message.answer("❌ Resource not found or has been removed.")
        return
    
    user = await user_ops.get_user(user_id)
    user_access_count = user.get('user_access_count', 0)
    
    if user_access_count <= 0:
        await message.answer("❌ You don't have enough access count. Please verify first.")
        return
    
    await user_ops.update_user_access_count(user_id, -1)
    
    deletion_time_minutes = await config_ops.get_deletion_time()
    zip_password = await config_ops.get_zip_password()
    
    sent_messages = []
    
    if file_data.get('is_batch', False):
        batch_files = file_data.get('batch_files', [])
        
        for batch_file in batch_files:
            file_type = batch_file['file_type']
            file_id = batch_file['file_id']
            text_content = batch_file['text_content']
            
            if file_type == "text":
                msg = await message.answer(text_content)
                sent_messages.append(msg.message_id)
            elif file_type == "photo":
                msg = await bot.send_photo(chat_id=message.chat.id, photo=file_id)
                sent_messages.append(msg.message_id)
            elif file_type == "video":
                msg = await bot.send_video(chat_id=message.chat.id, video=file_id)
                sent_messages.append(msg.message_id)
            elif file_type == "audio":
                msg = await bot.send_audio(chat_id=message.chat.id, audio=file_id)
                sent_messages.append(msg.message_id)
            elif file_type == "document":
                msg = await bot.send_document(chat_id=message.chat.id, document=file_id)
                sent_messages.append(msg.message_id)
    else:
        file_type = file_data['file_type']
        file_id = file_data['file_id']
        text_content = file_data['text_content']
        
        caption = None
        
        if file_type == "document" and file_id:
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            filename = file_path.split('/')[-1] if file_path else ""
            
            if is_zip_file(filename):
                caption = f"Password: {zip_password}"
        
        if file_type == "text":
            msg = await message.answer(text_content)
            sent_messages.append(msg.message_id)
        elif file_type == "photo":
            msg = await bot.send_photo(chat_id=message.chat.id, photo=file_id, caption=caption)
            sent_messages.append(msg.message_id)
        elif file_type == "video":
            msg = await bot.send_video(chat_id=message.chat.id, video=file_id, caption=caption)
            sent_messages.append(msg.message_id)
        elif file_type == "audio":
            msg = await bot.send_audio(chat_id=message.chat.id, audio=file_id, caption=caption)
            sent_messages.append(msg.message_id)
        elif file_type == "document":
            msg = await bot.send_document(chat_id=message.chat.id, document=file_id, caption=caption)
            sent_messages.append(msg.message_id)
    
    warning_text = WARNING_MESSAGE.format(deletion_time=deletion_time_minutes)
    warning_msg = await message.answer(warning_text)
    sent_messages.append(warning_msg.message_id)
    
    delete_at = get_deletion_time(deletion_time_minutes)
    
    pending_deletion_data = PendingDeletionModel.create_document(
        user_id=user_id,
        chat_id=message.chat.id,
        message_ids=sent_messages,
        delete_at=delete_at,
        unique_id=unique_id
    )
    
    await deletion_ops.create_pending_deletion(pending_deletion_data)

@router.callback_query(F.data == "close_message")
async def callback_close_message(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

async def send_deleted_notification(bot: Bot, user_id: int, chat_id: int, unique_id: str):
    deleted_text = DELETED_MESSAGE.format(
        link=f"https://t.me/{config.USER_BOT_USERNAME}?start={unique_id}"
    )
    
    await bot.send_message(
        chat_id=chat_id,
        text=deleted_text,
        reply_markup=get_deleted_message_keyboard(config.USER_BOT_USERNAME, unique_id),
        parse_mode="HTML"
    )
