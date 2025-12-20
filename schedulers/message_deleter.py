import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from database.operations import deletion_ops
from aiogram import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageDeleterScheduler:
    def __init__(self, bot: Bot):
        self.scheduler = AsyncIOScheduler()
        self.bot = bot
    
    async def delete_due_messages(self):
        try:
            logger.info("🗑️ Checking for messages to delete...")
            
            due_deletions = await deletion_ops.get_due_deletions()
            
            if not due_deletions:
                logger.info("✅ No messages to delete")
                return
            
            deleted_count = 0
            failed_count = 0
            
            for deletion in due_deletions:
                try:
                    chat_id = deletion['chat_id']
                    message_ids = deletion['message_ids']
                    unique_id = deletion['unique_id']
                    user_id = deletion['user_id']
                    
                    for message_id in message_ids:
                        try:
                            await self.bot.delete_message(
                                chat_id=chat_id,
                                message_id=message_id
                            )
                            deleted_count += 1
                        except Exception as e:
                            logger.warning(f"Failed to delete message {message_id}: {e}")
                            failed_count += 1
                    
                    from user_bot.handlers.resource_delivery import send_deleted_notification
                    await send_deleted_notification(self.bot, user_id, chat_id, unique_id)
                    
                    await deletion_ops.delete_pending_deletion(str(deletion['_id']))
                    
                except Exception as e:
                    logger.error(f"Error processing deletion: {e}")
                    failed_count += 1
            
            logger.info(f"✅ Deleted {deleted_count} messages, {failed_count} failed at {datetime.now()}")
            
        except Exception as e:
            logger.error(f"❌ Error during message deletion: {e}")
    
    def start(self):
        self.scheduler.add_job(
            self.delete_due_messages,
            IntervalTrigger(minutes=1),
            id='message_deleter',
            name='Message Deleter Job',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("🚀 Message Deleter Scheduler started (runs every minute)")
    
    def stop(self):
        self.scheduler.shutdown()
        logger.info("⏹ Message Deleter Scheduler stopped")

def create_message_deleter_scheduler(bot: Bot):
    return MessageDeleterScheduler(bot)
