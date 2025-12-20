from aiogram import Router
from aiogram.types import ChatJoinRequest
from database.operations import user_ops

router = Router()

@router.chat_join_request()
async def handle_chat_join_request(chat_join_request: ChatJoinRequest):
    user_id = chat_join_request.from_user.id
    chat_id = chat_join_request.chat.id
    
    user_exists = await user_ops.user_exists(user_id)
    
    if user_exists:
        await user_ops.add_join_request(user_id, chat_id)
