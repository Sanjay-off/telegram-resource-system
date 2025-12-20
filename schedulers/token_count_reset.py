import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.operations import token_ops

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TokenCountResetScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
    
    async def reset_token_counts(self):
        try:
            logger.info("🔄 Starting token count reset...")
            
            await token_ops.clear_token_counts()
            
            logger.info(f"✅ Token counts reset completed at {datetime.now()}")
            
        except Exception as e:
            logger.error(f"❌ Error during token count reset: {e}")
    
    def start(self):
        self.scheduler.add_job(
            self.reset_token_counts,
            CronTrigger(hour=0, minute=0),
            id='token_count_reset',
            name='Token Count Reset Job',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("🚀 Token Count Reset Scheduler started (runs at midnight)")
    
    def stop(self):
        self.scheduler.shutdown()
        logger.info("⏹ Token Count Reset Scheduler stopped")

token_count_reset_scheduler = TokenCountResetScheduler()
