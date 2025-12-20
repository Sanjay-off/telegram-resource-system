# Troubleshooting Guide

Common issues and their solutions.

## Table of Contents

1. [Bot Issues](#bot-issues)
2. [Database Issues](#database-issues)
3. [Bypass Server Issues](#bypass-server-issues)
4. [Scheduler Issues](#scheduler-issues)
5. [URL Shortener Issues](#url-shortener-issues)
6. [Force Subscription Issues](#force-subscription-issues)
7. [Verification Issues](#verification-issues)
8. [Message Delivery Issues](#message-delivery-issues)

---

## Bot Issues

### Bot Not Starting

**Symptoms:**
- Bot doesn't respond
- No logs appearing
- Process exits immediately

**Solutions:**

1. **Check bot token:**
```bash
# Verify token in .env
cat .env | grep BOT_TOKEN

# Test token
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

2. **Check Python version:**
```bash
python3.10 --version
# Should show 3.10.11
```

3. **Check dependencies:**
```bash
source venv/bin/activate
pip list | grep aiogram
# Should show aiogram==3.4.1
```

4. **Check logs:**
```bash
# If using systemd
sudo journalctl -u telegram-admin-bot -n 50

# If running directly
python3 admin_bot/main.py
```

### Bot Running But Not Responding

**Symptoms:**
- Bot process running
- No response to commands
- No error logs

**Solutions:**

1. **Check bot commands:**
```bash
# Via @BotFather
/mybots -> Select bot -> Edit Bot -> Edit Commands
```

2. **Check admin permissions:**
```bash
# Verify ADMIN_IDS in .env
cat .env | grep ADMIN_IDS
```

3. **Restart bot:**
```bash
sudo systemctl restart telegram-admin-bot
sudo systemctl restart telegram-user-bot
```

### Import Error / Module Not Found

**Symptoms:**
```
ModuleNotFoundError: No module named 'aiogram'
```

**Solutions:**

1. **Activate virtual environment:**
```bash
source venv/bin/activate
```

2. **Reinstall dependencies:**
```bash
pip install -r requirements.txt
```

3. **Check Python path:**
```bash
which python3
# Should point to venv/bin/python3
```

---

## Database Issues

### MongoDB Not Running

**Symptoms:**
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017
```

**Solutions:**

1. **Start MongoDB:**
```bash
sudo systemctl start mongodb
sudo systemctl status mongodb
```

2. **Check MongoDB port:**
```bash
sudo netstat -tlnp | grep 27017
```

3. **Check MongoDB logs:**
```bash
sudo tail -f /var/log/mongodb/mongod.log
```

### Connection Timeout

**Symptoms:**
```
pymongo.errors.ServerSelectionTimeoutError
```

**Solutions:**

1. **Check MONGO_URI:**
```bash
cat .env | grep MONGO_URI
```

2. **Test connection:**
```bash
mongosh
> db.adminCommand('ping')
```

3. **Check firewall:**
```bash
sudo ufw status
```

### Database Corruption

**Symptoms:**
- Bot crashes randomly
- Data inconsistencies
- MongoDB errors

**Solutions:**

1. **Repair database:**
```bash
mongosh
> use telegram_resource_system
> db.repairDatabase()
```

2. **Restore from backup:**
```bash
mongorestore --db telegram_resource_system ~/backups/latest
```

### Slow Queries

**Symptoms:**
- Slow bot responses
- High CPU usage
- Timeouts

**Solutions:**

1. **Check indexes:**
```bash
mongosh
> use telegram_resource_system
> db.files.getIndexes()
> db.users.getIndexes()
```

2. **Create missing indexes:**
```bash
> db.files.createIndex({unique_id: 1})
> db.users.createIndex({user_id: 1})
```

3. **Compact collections:**
```bash
> db.runCommand({compact: 'files'})
```

---

## Bypass Server Issues

### Server Not Starting

**Symptoms:**
```
Address already in use
```

**Solutions:**

1. **Check port usage:**
```bash
sudo lsof -i :5000
```

2. **Kill existing process:**
```bash
sudo kill -9 <PID>
```

3. **Change port in .env:**
```bash
SERVER_PORT=5001
```

### Token Always Invalid

**Symptoms:**
- All tokens show "invalid"
- Database has tokens

**Solutions:**

1. **Check database connection:**
```bash
# In bypass_server/app.py logs
# Should see "✅ Connected to MongoDB"
```

2. **Check token in database:**
```bash
mongosh
> use telegram_resource_system
> db.tokens.findOne({token: "YOUR_TOKEN"})
```

3. **Check token validator:**
```python
# Test manually
python3 << 'EOF'
from database.connection import db
from bypass_server.utils import token_validator
import asyncio

db.connect_sync()
# Test validation
EOF
```

### Bypass Always Detected

**Symptoms:**
- All verifications marked as bypass
- Valid users can't verify

**Solutions:**

1. **Check time threshold:**
```bash
# In shared/constants.py
BYPASS_TIME_THRESHOLD = 120  # Should be 120 seconds
```

2. **Check referer header:**
```python
# Add logging in token_validator.py
print(f"Referer: {referer}")
```

3. **Check whitelist:**
```python
# In bypass_server/utils/token_validator.py
print(token_validator.whitelist_domains)
```

### 404 Not Found

**Symptoms:**
- Page not found error
- Blank page

**Solutions:**

1. **Check URL:**
```bash
# Should be:
http://SERVER_HOST:SERVER_PORT/redirect?token=...
```

2. **Check templates:**
```bash
ls -la bypass_server/templates/
# Should have error.html and redirect.html
```

3. **Check static files:**
```bash
ls -la bypass_server/static/css/
# Should have style.css
```

---

## Scheduler Issues

### Schedulers Not Running

**Symptoms:**
- Old tokens not deleted
- Messages not auto-deleted
- Logs show no scheduler activity

**Solutions:**

1. **Check user bot logs:**
```bash
sudo journalctl -u telegram-user-bot | grep Scheduler
# Should show "Scheduler started"
```

2. **Check APScheduler:**
```bash
pip list | grep apscheduler
# Should show apscheduler==3.10.4
```

3. **Restart user bot:**
```bash
sudo systemctl restart telegram-user-bot
```

### Messages Not Being Deleted

**Symptoms:**
- Messages stay after deletion time
- No deletion notification

**Solutions:**

1. **Check pending_deletions:**
```bash
mongosh
> use telegram_resource_system
> db.pending_deletions.find().pretty()
```

2. **Check delete_at time:**
```javascript
// Should be in past for deletion to trigger
> db.pending_deletions.find({
    delete_at: {$lte: new Date()}
})
```

3. **Check bot permissions:**
- Bot needs permission to delete messages
- User must not have deleted chat

4. **Manual trigger:**
```bash
python3 schedulers/test_schedulers.py
# Select Message Deleter test
```

### Token Cleanup Not Working

**Symptoms:**
- Old tokens accumulating
- Database growing

**Solutions:**

1. **Check token expiry:**
```bash
mongosh
> use telegram_resource_system
> db.tokens.find({
    expires_at: {$lt: new Date()}
}).count()
```

2. **Manual cleanup:**
```bash
python3 schedulers/test_schedulers.py
# Select Token Cleanup test
```

3. **Check cron schedule:**
```bash
# Should run at 00:00 and 12:00
sudo journalctl -u telegram-user-bot | grep "Token Cleanup"
```

---

## URL Shortener Issues

### Shortened URL Not Working

**Symptoms:**
- URL returns error
- Can't access destination

**Solutions:**

1. **Check API token:**
```bash
cat .env | grep API_TOKEN
```

2. **Test API manually:**
```bash
curl "https://arolinks.com/api?api=YOUR_TOKEN&url=https://google.com"
```

3. **Check API response:**
```python
# Should return JSON with shortened URL
{"shortenedUrl": "https://..."}
```

### No URL Shortener Selected

**Symptoms:**
- Destination URL shown directly
- No shortening happening

**Solutions:**

1. **Check config:**
```bash
cat .env | grep BASE_URL
# Should have at least one shortener
```

2. **Verify format:**
```env
SHORTENER_NAME_API_TOKEN=token
SHORTENER_NAME_BASE_URL=https://...
```

3. **Check whitelist:**
```python
from shared.url_shortener import url_shortener
print(url_shortener.get_whitelist_domains())
```

---

## Force Subscription Issues

### Force Sub Not Triggering

**Symptoms:**
- Users can access without joining
- No force sub message

**Solutions:**

1. **Check channels configured:**
```bash
# Via admin bot
/list_force_sub
```

2. **Check bot in channel:**
- Bot must be admin in channel
- Bot needs member checking permission

3. **Check middleware order:**
```python
# In user_bot/main.py
# ForceSubMiddleware should be before resource delivery
```

### Users Can't Join Channel

**Symptoms:**
- "Request to join" not working
- Join button doesn't work

**Solutions:**

1. **For private channels:**
- Enable "Approve new members" in channel settings
- Bot must be admin

2. **For public channels:**
- Users can join directly
- Check channel link correct

3. **Check join request handler:**
```python
# user_bot/handlers/chat_join_request.py should be registered
```

### Try Again Button Not Working

**Symptoms:**
- Button doesn't redirect
- No parameter passed

**Solutions:**

1. **Check deeplink format:**
```python
# Should be: https://t.me/bot?start=unique_id
```

2. **Check unique_id extraction:**
```python
# In force_sub middleware
# unique_id should be extracted from /start command
```

---

## Verification Issues

### Users Always See Verification

**Symptoms:**
- Verified users still asked to verify
- Access count not increasing

**Solutions:**

1. **Check user access count:**
```bash
mongosh
> use telegram_resource_system
> db.users.findOne({user_id: 123456})
# Check user_access_count field
```

2. **Check verification middleware:**
```python
# Should check: user_access_count > 0
```

3. **Manual fix:**
```bash
> db.users.updateOne(
    {user_id: 123456},
    {$set: {user_access_count: 10}}
)
```

### Token Generation Limit Reached

**Symptoms:**
```
You have reached your daily token generation limit
```

**Solutions:**

1. **Check current count:**
```bash
mongosh
> db.token_generator_count.findOne({user_id: 123456})
```

2. **Reset manually:**
```bash
> db.token_generator_count.deleteOne({user_id: 123456})
```

3. **Wait for midnight:**
- Counts reset automatically at 00:00

4. **Increase limit:**
```bash
# Via admin bot
/set_token_limit
20
```

### Bypass Detection False Positives

**Symptoms:**
- Valid users marked as bypassed
- Verification always fails

**Solutions:**

1. **Increase time threshold:**
```python
# In shared/constants.py
BYPASS_TIME_THRESHOLD = 300  # 5 minutes instead of 2
```

2. **Check URL shortener timing:**
- Some shorteners have captcha
- Users may take longer

3. **Check referer header:**
```python
# Add logging in token_validator
print(f"Referer: {request.headers.get('Referer')}")
```

---

## Message Delivery Issues

### Resources Not Sending

**Symptoms:**
- No message after verification
- Error in logs

**Solutions:**

1. **Check file in database:**
```bash
mongosh
> db.files.findOne({unique_id: "YOUR_UNIQUE_ID"})
```

2. **Check storage channel:**
- Bot must be admin
- Message must exist
- File ID must be valid

3. **Check bot permissions:**
```bash
# Via @BotFather
/mybots -> Select bot -> Bot Settings -> Group Privacy: OFF
```

### ZIP Password Not Showing

**Symptoms:**
- ZIP files sent without caption
- No password mentioned

**Solutions:**

1. **Check file detection:**
```python
# In shared/utils.py
# is_zip_file() should detect .zip files
```

2. **Check password config:**
```bash
mongosh
> db.admin_config.findOne({key: "zip_password"})
```

3. **Set password:**
```bash
# Via admin bot
/set_password
mypassword123
```

### Messages Not Deleting

**See Scheduler Issues > Messages Not Being Deleted**

---

## General Debugging

### Enable Debug Logging

```python
# In any main.py file
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Check All Services

```bash
# Quick health check script
echo "Checking services..."

# MongoDB
if pgrep -x "mongod" > /dev/null; then
    echo "✅ MongoDB running"
else
    echo "❌ MongoDB not running"
fi

# Admin Bot
if pgrep -f "admin_bot/main.py" > /dev/null; then
    echo "✅ Admin Bot running"
else
    echo "❌ Admin Bot not running"
fi

# User Bot
if pgrep -f "user_bot/main.py" > /dev/null; then
    echo "✅ User Bot running"
else
    echo "❌ User Bot not running"
fi

# Bypass Server
if pgrep -f "bypass_server" > /dev/null; then
    echo "✅ Bypass Server running"
else
    echo "❌ Bypass Server not running"
fi
```

### Database Integrity Check

```bash
mongosh << 'EOF'
use telegram_resource_system

print("Files:", db.files.countDocuments())
print("Users:", db.users.countDocuments())
print("Tokens:", db.tokens.countDocuments())
print("Pending Deletions:", db.pending_deletions.countDocuments())
print("Broadcasts:", db.broadcasts.countDocuments())

print("\nIndexes:")
print("Files indexes:", db.files.getIndexes().length)
print("Users indexes:", db.users.getIndexes().length)
print("Tokens indexes:", db.tokens.getIndexes().length)
EOF
```

---

## Getting Help

If you've tried everything and still have issues:

1. **Check logs thoroughly**
2. **Search GitHub issues**
3. **Create detailed bug report with:**
   - Error messages
   - Steps to reproduce
   - System info
   - Log excerpts
4. **Join support channel** (if available)

---

**Most issues are configuration-related. Double-check .env file! 📝**
