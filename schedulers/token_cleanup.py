import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.operations import token_ops

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TokenCleanupScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
    
    async def cleanup_expired_tokens(self):
        try:
            logger.info("🧹 Starting token cleanup...")
            
            await token_ops.delete_expired_and_used_tokens()
            
            logger.info(f"✅ Token cleanup completed at {datetime.now()}")
            
        except Exception as e:
            logger.error(f"❌ Error during token cleanup: {e}")
    
    def start(self):
        self.scheduler.add_job(
            self.cleanup_expired_tokens,
            CronTrigger(hour='0,12', minute=0),
            id='token_cleanup',
            name='Token Cleanup Job',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("🚀 Token Cleanup Scheduler started (runs at 00:00 and 12:00)")
    
    def stop(self):
        self.scheduler.shutdown()
        logger.info("⏹ Token Cleanup Scheduler stopped")

token_cleanup_scheduler = TokenCleanupScheduler()
