import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from database.operations import broadcast_ops, user_ops
from aiogram import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BroadcastDeleterScheduler:
    def __init__(self, bot: Bot):
        self.scheduler = AsyncIOScheduler()
        self.bot = bot
    
    async def delete_expired_broadcasts(self):
        try:
            logger.info("📢 Checking for expired broadcasts...")
            
            expired_broadcasts = await broadcast_ops.get_expired_broadcasts()
            
            if not expired_broadcasts:
                logger.info("✅ No expired broadcasts")
                return
            
            users = await user_ops.get_all_users()
            deleted_count = 0
            failed_count = 0
            
            for broadcast in expired_broadcasts:
                try:
                    message_id = broadcast.get('message_id')
                    
                    for user in users:
                        try:
                            await self.bot.delete_message(
                                chat_id=user['user_id'],
                                message_id=message_id
                            )
                            deleted_count += 1
                        except Exception as e:
                            failed_count += 1
                    
                    await broadcast_ops.delete_broadcast(str(broadcast['_id']))
                    
                except Exception as e:
                    logger.error(f"Error deleting broadcast: {e}")
                    failed_count += 1
            
            logger.info(f"✅ Deleted {deleted_count} broadcast messages, {failed_count} failed at {datetime.now()}")
            
        except Exception as e:
            logger.error(f"❌ Error during broadcast deletion: {e}")
    
    def start(self):
        self.scheduler.add_job(
            self.delete_expired_broadcasts,
            IntervalTrigger(hours=1),
            id='broadcast_deleter',
            name='Broadcast Deleter Job',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("🚀 Broadcast Deleter Scheduler started (runs every hour)")
    
    def stop(self):
        self.scheduler.shutdown()
        logger.info("⏹ Broadcast Deleter Scheduler stopped")

def create_broadcast_deleter_scheduler(bot: Bot):
    return BroadcastDeleterScheduler(bot)
