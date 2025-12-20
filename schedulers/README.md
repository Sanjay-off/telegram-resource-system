# Background Schedulers

Automated maintenance tasks that run in the background to keep the system clean and functional.

## Overview

The system includes four main schedulers:

1. **Token Cleanup** - Deletes expired and used tokens
2. **Message Deleter** - Deletes scheduled messages after deletion time
3. **Broadcast Deleter** - Deletes expired broadcast messages
4. **Token Count Reset** - Resets daily token generation counts

## Schedulers

### 1. Token Cleanup Scheduler

**Purpose**: Clean up expired and used tokens from the database

**Schedule**: Twice daily (00:00 and 12:00)

**What it does**:
- Queries tokens where `expires_at < current_time`
- Deletes tokens with status "verified" or "bypassed"
- Keeps unused tokens even if expired (for user convenience)

**Database Query**:
```python
{
    "expires_at": {"$lt": datetime.utcnow()},
    "status": {"$in": ["verified", "bypassed"]}
}
```

**Why twice daily?**
- Reduces database bloat
- Happens during off-peak hours
- Balances cleanup frequency with performance

---

### 2. Message Deleter Scheduler

**Purpose**: Delete messages after their scheduled deletion time

**Schedule**: Every minute

**What it does**:
- Queries `pending_deletions` collection for due messages
- Deletes each message from user's chat
- Sends "deleted notification" message with retry button
- Removes deletion record from database

**Why every minute?**
- Provides precise deletion timing
- Users expect deletion "after X minutes"
- Low overhead (only queries when messages are due)

**Flow**:
1. Check `delete_at <= current_time`
2. Delete all messages in `message_ids` array
3. Send deleted notification with "Click Here" button
4. Remove pending deletion record

---

### 3. Broadcast Deleter Scheduler

**Purpose**: Delete broadcast messages after their duration

**Schedule**: Every hour

**What it does**:
- Queries `broadcasts` collection for expired items
- Deletes broadcast message from all users
- Removes broadcast record from database

**Why every hour?**
- Broadcasts have longer durations (hours, not minutes)
- Less frequent checks reduce overhead
- Suitable for broadcast use cases

**Flow**:
1. Check `delete_at <= current_time`
2. Get all users from database
3. Delete message from each user's chat
4. Remove broadcast record

---

### 4. Token Count Reset Scheduler

**Purpose**: Reset daily token generation counts at midnight

**Schedule**: Daily at 00:00

**What it does**:
- Queries `token_generator_count` collection
- Deletes all records older than today
- Allows users to generate new tokens the next day

**Why at midnight?**
- Natural daily boundary
- Users expect daily limits to reset overnight
- Simple to understand

**Database Operation**:
```python
{
    "date": {"$lt": today}
}
```

---

## Integration

### User Bot Integration

Schedulers are automatically started when the User Bot starts:

```python
# In user_bot/main.py
token_cleanup_scheduler.start()
token_count_reset_scheduler.start()

message_deleter = create_message_deleter_scheduler(bot)
message_deleter.start()

broadcast_deleter = create_broadcast_deleter_scheduler(bot)
broadcast_deleter.start()
```

### Graceful Shutdown

Schedulers are properly stopped when the bot shuts down:

```python
try:
    await dp.start_polling(bot)
finally:
    token_cleanup_scheduler.stop()
    token_count_reset_scheduler.stop()
    message_deleter.stop()
    broadcast_deleter.stop()
```

---

## Configuration

Schedulers use configurations from:

**Time-based:**
- Token expiry: `TOKEN_EXPIRY_DAYS = 2`
- Token cleanup hours: `TOKEN_CLEANUP_HOUR = [0, 12]`
- Deletion time: Configurable via admin bot

**No additional configuration needed** - All settings are automatic or set via admin bot commands.

---

## Logging

All schedulers log their activities:

**Success logs:**
```
✅ Token cleanup completed at 2025-12-20 00:00:00
✅ Deleted 15 messages, 0 failed at 2025-12-20 14:35:00
✅ Token counts reset completed at 2025-12-20 00:00:00
```

**Error logs:**
```
❌ Error during token cleanup: [error details]
Failed to delete message 12345: [error details]
```

---

## Performance Considerations

### Token Cleanup (Twice Daily)
- **Database queries**: 1 per run
- **Load**: Very low
- **Impact**: Minimal

### Message Deleter (Every Minute)
- **Database queries**: 1 per run
- **Load**: Low (only when messages are due)
- **Impact**: Minimal

### Broadcast Deleter (Every Hour)
- **Database queries**: 1 + (1 per user)
- **Load**: Moderate (depends on user count)
- **Impact**: Low with rate limiting

### Token Count Reset (Daily)
- **Database queries**: 1 per run
- **Load**: Very low
- **Impact**: Minimal

---

## Error Handling

All schedulers include error handling:

**Try-Catch Blocks:**
- Main scheduler function wrapped in try-catch
- Individual operations wrapped in try-catch
- Errors logged but don't stop scheduler

**Example:**
```python
try:
    await token_ops.delete_expired_and_used_tokens()
    logger.info("✅ Token cleanup completed")
except Exception as e:
    logger.error(f"❌ Error during token cleanup: {e}")
```

---

## Monitoring

### Check Scheduler Status

Schedulers log startup messages:
```
🚀 Token Cleanup Scheduler started (runs at 00:00 and 12:00)
🚀 Message Deleter Scheduler started (runs every minute)
🚀 Broadcast Deleter Scheduler started (runs every hour)
🚀 Token Count Reset Scheduler started (runs at midnight)
```

### Check Logs

Monitor logs for:
- ✅ Success indicators
- ❌ Error indicators
- 🧹 🗑️ 📢 🔄 Task-specific emojis

---

## Testing

### Manual Testing

To test schedulers without waiting:

**1. Token Cleanup:**
```python
# Create expired token in database
# Run scheduler manually
await token_cleanup_scheduler.cleanup_expired_tokens()
```

**2. Message Deleter:**
```python
# Create pending deletion with past delete_at time
# Run scheduler manually
await message_deleter.delete_due_messages()
```

**3. Broadcast Deleter:**
```python
# Create broadcast with past delete_at time
# Run scheduler manually
await broadcast_deleter.delete_expired_broadcasts()
```

**4. Token Count Reset:**
```python
# Create token counts with old date
# Run scheduler manually
await token_count_reset_scheduler.reset_token_counts()
```

---

## Troubleshooting

### Scheduler not running

**Check:**
1. Bot started successfully?
2. Database connected?
3. Check logs for startup messages

### Messages not being deleted

**Check:**
1. `pending_deletions` collection populated?
2. `delete_at` time in past?
3. Bot has permission to delete messages?
4. Check logs for errors

### Tokens not being cleaned up

**Check:**
1. Tokens actually expired?
2. Token status is "verified" or "bypassed"?
3. Check logs at 00:00 and 12:00

### Token counts not resetting

**Check:**
1. Midnight passed?
2. Check logs at 00:00
3. Database connection stable?

---

## Dependencies

**APScheduler**: For scheduling tasks
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
```

**Database Operations**: For data access
```python
from database.operations import token_ops, deletion_ops, broadcast_ops, user_ops
```

**Aiogram Bot**: For message deletion
```python
from aiogram import Bot
```

---

## Best Practices

✅ **Always use try-catch** in scheduler functions
✅ **Log all operations** for monitoring
✅ **Gracefully stop schedulers** on shutdown
✅ **Test schedulers** before deploying
✅ **Monitor logs** regularly
✅ **Set appropriate intervals** based on task urgency
✅ **Handle errors** without stopping scheduler

❌ **Don't block the event loop** with long operations
❌ **Don't forget to stop schedulers** on shutdown
❌ **Don't ignore error logs**
❌ **Don't set intervals too short** (causes overhead)

---

## Future Enhancements

Potential improvements:

1. **Database Statistics Scheduler**
   - Track user growth
   - Monitor resource usage
   - Generate reports

2. **Health Check Scheduler**
   - Check bot connectivity
   - Monitor database health
   - Alert on issues

3. **Backup Scheduler**
   - Automated database backups
   - Export important data
   - Retention management

4. **Analytics Scheduler**
   - Track verification rates
   - Monitor bypass attempts
   - User engagement metrics
