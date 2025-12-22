from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin_bot.states import BroadcastStates
from admin_bot.keyboards import get_cancel_keyboard
from database.operations import user_ops, broadcast_ops
from database.models import BroadcastModel
from shared.utils import get_file_type, get_file_id
from shared.config import config
from shared.constants import BROADCAST_RATE_LIMIT
import asyncio

router = Router()

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, state: FSMContext):
    await state.set_state(BroadcastStates.waiting_for_message)
    await message.answer(
        "📢 Please send the message to broadcast (can be text, photo with caption, video, document, etc.):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(BroadcastStates.waiting_for_message)
async def process_broadcast_message(message: Message, state: FSMContext, bot: Bot):
    file_type = get_file_type(message)
    file_id = get_file_id(message)
    text = message.text if file_type == "text" else None
    caption = message.caption if message.caption else None
    
    forwarded = await bot.forward_message(
        chat_id=config.STORAGE_CHANNEL_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
    
    await state.update_data(
        file_type=file_type,
        file_id=file_id,
        text=text,
        caption=caption,
        channel_message_id=forwarded.message_id,
        temp_message=message
    )
    
    await state.set_state(BroadcastStates.waiting_for_duration)
    await message.answer("⏱ Please enter the duration in hours (after which the broadcast will be deleted):")

@router.message(BroadcastStates.waiting_for_duration)
async def process_broadcast_duration(message: Message, state: FSMContext, bot: Bot):
    try:
        duration_hours = int(message.text)
        if duration_hours <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Invalid duration. Please enter a positive number.")
        return
    
    data = await state.get_data()
    temp_message = data['temp_message']
    
    users = await user_ops.get_all_users()
    
    status_msg = await message.answer(f"📤 Broadcasting to {len(users)} users...")
    
    success = 0
    failed = 0
    
    broadcast_data = BroadcastModel.create_document(
        message_id=temp_message.message_id,
        file_id=data['file_id'],
        text=data['text'],
        caption=data['caption'],
        duration_hours=duration_hours,
        channel_message_id=data['channel_message_id']
    )
    
    await broadcast_ops.create_broadcast(broadcast_data)
    
    user_bot = Bot(token=config.USER_BOT_TOKEN)
    
    for user in users:
        try:
            if data['file_type'] == "text":
                await user_bot.send_message(  # ← Use USER BOT now!
                    chat_id=user['user_id'],
                    text=data['text']
                )
            elif data['file_type'] == "photo":
                await user_bot.send_photo(  # ← Use USER BOT
                    chat_id=user['user_id'],
                    photo=data['file_id'],
                    caption=data['caption']
                )
            elif data['file_type'] == "video":
                await user_bot.send_video(  # ← Use USER BOT
                    chat_id=user['user_id'],
                    video=data['file_id'],
                    caption=data['caption']
                )
            elif data['file_type'] == "document":
                await user_bot.send_document(  # ← Use USER BOT
                    chat_id=user['user_id'],
                    document=data['file_id'],
                    caption=data['caption']
                )
            elif data['file_type'] == "audio":
                await user_bot.send_audio(  # ← Use USER BOT
                    chat_id=user['user_id'],
                    audio=data['file_id'],
                    caption=data['caption']
                )
            
            success += 1
            await asyncio.sleep(1 / BROADCAST_RATE_LIMIT)
            
        except Exception as e:
            failed += 1
            print(f"Failed to send broadcast to user {user['user_id']}: {e}")

    # Close user bot session after broadcast
    await user_bot.session.close()
    
    await status_msg.edit_text(
        f"✅ Broadcast completed!\n\n"
        f"✅ Sent: {success}\n"
        f"❌ Failed: {failed}\n"
        f"⏱ Will be deleted after {duration_hours} hours"
    )
    
    await state.clear()
