from aiogram import Router
from aiogram.types import Message
from database.operations import token_ops, user_ops, config_ops
from shared.constants import BYPASS_DETECTED_MESSAGE, ACCESS_COUNT_MESSAGE, TOKEN_STATUS_VERIFIED, TOKEN_STATUS_BYPASSED

router = Router()

async def handle_verify_callback(message: Message, payload: str):
    parts = payload.split("_")
    
    if len(parts) != 3:
        await message.answer("❌ ɪɴᴠᴀʟɪᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ")
        return
    
    unique_id = parts[1]
    try:
        user_id = int(parts[2])
    except ValueError:
        await message.answer("❌ ɪɴᴠᴀʟɪᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ")
        return
    
    if message.from_user.id != user_id:
        await message.answer("❌ ᴛʜɪs ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ ɪs ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ.")
        return
    
    token_data = await token_ops.get_token_by_unique_id_and_user(unique_id, user_id)
    
    if not token_data:
        await message.answer("❌ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴛᴏᴋᴇɴ ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ.")
        return
    
    status = token_data.get('status')
    
    if status == TOKEN_STATUS_VERIFIED:
        media_access_count = await config_ops.get_media_access_count()
        
        await user_ops.update_user_access_count(user_id, media_access_count)
        
        await token_ops.delete_token(token_data['token'])
        
        user = await user_ops.get_user(user_id)
        user_access_count = user.get('user_access_count', 0)
        
        await message.answer(
            ACCESS_COUNT_MESSAGE.format(user_access_count=user_access_count),
             parse_mode="HTML"
        )
        
    elif status == TOKEN_STATUS_BYPASSED:
        await message.answer(BYPASS_DETECTED_MESSAGE, parse_mode="HTML")
        
        user = await user_ops.get_user(user_id)
        user_access_count = user.get('user_access_count', 0)
        
        await message.answer(
            ACCESS_COUNT_MESSAGE.format(user_access_count=user_access_count),
            parse_mode="HTML"
        )
    
    else:
        await message.answer("<b>❌ ᴘʟᴇᴀsᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ᴛʜᴇ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴄᴇss ꜰɪʀsᴛ.</b>",parse_mode="HTML")