from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from admin_bot.states import AddForceSubStates
from admin_bot.keyboards import get_force_sub_channels_keyboard, get_cancel_keyboard
from database.operations import config_ops

router = Router()

@router.message(Command("add_force_sub"))
async def cmd_add_force_sub(message: Message, state: FSMContext):
    await state.set_state(AddForceSubStates.waiting_for_channel_link)
    await message.answer(
        "🔗 Please send the channel/group link or username (e.g., @channelname or https://t.me/channelname):",
        reply_markup=get_cancel_keyboard()
    )

@router.message(AddForceSubStates.waiting_for_channel_link)
async def process_channel_link(message: Message, state: FSMContext, bot: Bot):
    channel_input = message.text.strip()
    
    if channel_input.startswith('@'):
        channel_username = channel_input
    elif 't.me/' in channel_input:
        channel_username = '@' + channel_input.split('/')[-1]
    else:
        await message.answer("❌ Invalid channel link. Please send a valid link or username.")
        return
    
    try:
        chat = await bot.get_chat(channel_username)
        channel_id = chat.id
        channel_title = chat.title or chat.username
        
        await state.update_data(channel_id=channel_id, channel_title=channel_title)
        await state.set_state(AddForceSubStates.waiting_for_placeholder)
        await message.answer(f"✅ Channel found: {channel_title}\n\n📝 Please enter a placeholder name for this channel:")
        
    except Exception as e:
        await message.answer(f"❌ Could not find channel. Make sure:\n1. The bot is added to the channel\n2. The link is correct\n\nError: {str(e)}")

@router.message(AddForceSubStates.waiting_for_placeholder)
async def process_placeholder(message: Message, state: FSMContext):
    placeholder = message.text.strip()
    data = await state.get_data()
    
    await config_ops.add_force_sub_channel(
        channel_id=data['channel_id'],
        placeholder=placeholder
    )
    
    await message.answer(
        f"✅ Force sub channel added successfully!\n\n"
        f"Channel: {data['channel_title']}\n"
        f"Placeholder: {placeholder}"
    )
    
    await state.clear()

@router.message(Command("remove_force_sub"))
async def cmd_remove_force_sub(message: Message):
    channels = await config_ops.get_force_sub_channels()
    
    if not channels:
        await message.answer("❌ No force sub channels configured.")
        return
    
    await message.answer(
        "Select a channel to remove:",
        reply_markup=get_force_sub_channels_keyboard(channels)
    )

@router.callback_query(F.data.startswith("remove_channel_"))
async def process_remove_channel(callback: CallbackQuery):
    channel_id = int(callback.data.split("_")[2])
    
    await config_ops.remove_force_sub_channel(channel_id)
    
    await callback.message.edit_text("✅ Channel removed from force sub list.")
    await callback.answer()

@router.message(Command("list_force_sub"))
async def cmd_list_force_sub(message: Message):
    channels = await config_ops.get_force_sub_channels()
    
    if not channels:
        await message.answer("❌ No force sub channels configured.")
        return
    
    text = "📋 Force Sub Channels:\n\n"
    for idx, channel in enumerate(channels, 1):
        text += f"{idx}. {channel['placeholder']} (ID: {channel['channel_id']})\n"
    
    await message.answer(text)
