import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from shared.config import config
from database.connection import db
from user_bot.middlewares import (
    BanCheckMiddleware,
    TokenLimitMiddleware,
    ForceSubMiddleware,
    VerificationMiddleware
)
from user_bot.handlers import (
    start,
    help,
    token_handler,
    resource_delivery,
    verify_handler,
    chat_join_request
)
from schedulers import (
    token_cleanup_scheduler,
    create_message_deleter_scheduler,
    create_broadcast_deleter_scheduler,
    token_count_reset_scheduler
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help information"),
        BotCommand(command="create_new_token", description="Create new verification token")
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=config.USER_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.message.middleware(BanCheckMiddleware())
    dp.message.middleware(TokenLimitMiddleware())
    dp.message.middleware(ForceSubMiddleware())
    dp.message.middleware(VerificationMiddleware())
    
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(token_handler.router)
    dp.include_router(resource_delivery.router)
    dp.include_router(verify_handler.router)
    dp.include_router(chat_join_request.router)
    
    await db.connect()
    
    await set_bot_commands(bot)
    
    token_cleanup_scheduler.start()
    token_count_reset_scheduler.start()
    
    message_deleter = create_message_deleter_scheduler(bot)
    message_deleter.start()
    
    broadcast_deleter = create_broadcast_deleter_scheduler(bot)
    broadcast_deleter.start()
    
    logger.info("User Bot started successfully!")
    logger.info("🔧 All schedulers started!")
    
    try:
        await dp.start_polling(bot)
    finally:
        token_cleanup_scheduler.stop()
        token_count_reset_scheduler.stop()
        message_deleter.stop()
        broadcast_deleter.stop()
        
        await db.close()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("User Bot stopped by user")
