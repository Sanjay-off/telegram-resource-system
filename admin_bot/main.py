import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from shared.config import config
from database.connection import db
from admin_bot.middlewares import AdminAuthMiddleware
from admin_bot.handlers import cancel
from admin_bot.handlers import (
    start,
    generate_link,
    regenerate_post,
    generate_batch,
    broadcast,
    force_sub_management,
    user_management,
    verification_settings,
    system_config
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="generate_link", description="Generate resource link"),
        BotCommand(command="regenerate_post", description="Regenerate post template"),
        BotCommand(command="generate_batch", description="Generate batch link"),
        BotCommand(command="broadcast", description="Broadcast message to users"),
        BotCommand(command="add_force_sub", description="Add force sub channel"),
        BotCommand(command="remove_force_sub", description="Remove force sub channel"),
        BotCommand(command="list_force_sub", description="List force sub channels"),
        BotCommand(command="verification_stats", description="View verification statistics"),
        BotCommand(command="ban_user", description="Ban a user"),
        BotCommand(command="unban_user", description="Unban a user"),
        BotCommand(command="set_free_media_access", description="Set free media access count"),
        BotCommand(command="set_paid_access", description="Set paid access for user"),
        BotCommand(command="set_password", description="Set ZIP password"),
        BotCommand(command="set_deletion_time", description="Set file deletion time"),
        BotCommand(command="set_token_limit", description="Set token generation limit"),
        BotCommand(command="set_how_to_verify", description="Set how to verify link")
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=config.ADMIN_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.message.middleware(AdminAuthMiddleware())
    dp.callback_query.middleware(AdminAuthMiddleware())
    dp.include_router(cancel.router)
    dp.include_router(start.router)
    dp.include_router(generate_link.router)
    dp.include_router(regenerate_post.router)
    dp.include_router(generate_batch.router)
    dp.include_router(broadcast.router)
    dp.include_router(force_sub_management.router)
    dp.include_router(user_management.router)
    dp.include_router(verification_settings.router)
    dp.include_router(system_config.router)
    
    await db.connect()
    
    await set_bot_commands(bot)
    
    logger.info("Admin Bot started successfully!")
    
    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Admin Bot stopped by user")
