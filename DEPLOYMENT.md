# Deployment Guide

Complete guide for deploying the Telegram Resource Distribution System.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Bot Configuration](#bot-configuration)
6. [Running the System](#running-the-system)
7. [Production Deployment](#production-deployment)
8. [Monitoring](#monitoring)
9. [Backup & Recovery](#backup--recovery)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **OS**: Ubuntu 20.04+ / Debian 11+ / Any Linux distro
- **Python**: 3.10.11 (exact version)
- **MongoDB**: 4.4+ (local or remote)
- **RAM**: Minimum 1GB, Recommended 2GB+
- **Storage**: 10GB+ free space
- **Network**: Public IP or domain (for bypass server)

### Software Requirements

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10
sudo apt install -y python3.10 python3.10-venv python3.10-dev

# Install MongoDB
sudo apt install -y mongodb

# Install additional tools
sudo apt install -y git curl wget nano
```

---

## Initial Setup

### 1. Clone or Extract Project

```bash
# If using git
git clone https://github.com/yourusername/telegram-resource-system.git
cd telegram-resource-system

# Or extract archive
tar -xzf telegram-resource-system.tar.gz
cd telegram-resource-system
```

### 2. Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install dependencies
- Create .env file
- Setup MongoDB indexes
- Make scripts executable

---

## Configuration

### 1. Create Telegram Bots

Go to [@BotFather](https://t.me/BotFather) and create two bots:

**Admin Bot:**
```
/newbot
Name: Your Admin Bot
Username: your_admin_bot
```

**User Bot:**
```
/newbot
Name: Your User Bot
Username: your_user_bot
```

Save both bot tokens.

### 2. Configure Bot Commands

**Admin Bot Commands** (via @BotFather):
```
start - Start the bot
generate_link - Generate resource link
regenerate_post - Regenerate post template
generate_batch - Generate batch link
broadcast - Broadcast message to users
add_force_sub - Add force sub channel
remove_force_sub - Remove force sub channel
list_force_sub - List force sub channels
verification_stats - View verification statistics
ban_user - Ban a user
unban_user - Unban a user
set_free_media_access - Set free media access count
set_paid_access - Set paid access for user
set_password - Set ZIP password
set_deletion_time - Set file deletion time
set_token_limit - Set token generation limit
set_how_to_verify - Set how to verify link
```

**User Bot Commands** (via @BotFather):
```
start - Start the bot
help - Get help information
create_new_token - Create new verification token
```

### 3. Edit .env File

```bash
nano .env
```

**Required Configuration:**

```env
# Admin Bot
ADMIN_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ADMIN_IDS=123456789,987654321

# User Bot
USER_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
USER_BOT_USERNAME=your_user_bot

# Channels
STORAGE_CHANNEL_ID=-1001234567890
PUBLIC_CHANNEL_USERNAME=@your_public_channel

# MongoDB
MONGO_URI=mongodb://localhost:27017/
DB_NAME=telegram_resource_system

# URL Shorteners (add as many as you have)
AROLINKS_API_TOKEN=your_token_here
AROLINKS_BASE_URL=https://arolinks.com/api

LINKPAYS_API_TOKEN=your_token_here
LINKPAYS_BASE_URL=https://linkpays.in/api

# Add more shorteners as needed
GPLINKS_API_TOKEN=your_token_here
GPLINKS_BASE_URL=https://gplinks.co/api

# Bypass Server
SERVER_HOST=152.42.212.81
SERVER_PORT=5000
SERVER_SECRET_KEY=your_random_secret_key_here

# Message Effects
NOT_AUTHORIZED_EFFECT=5046589136895476101
FIRE_EFFECT=5104841245755180586
```

### 4. Get Required IDs

**Storage Channel ID:**
1. Create a private channel
2. Add your admin bot as admin
3. Forward a message from the channel to [@userinfobot](https://t.me/userinfobot)
4. Copy the channel ID (e.g., -1001234567890)

**Admin User IDs:**
1. Message [@userinfobot](https://t.me/userinfobot)
2. Copy your user ID
3. Add to ADMIN_IDS in .env

---

## Database Setup

### 1. Start MongoDB

```bash
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### 2. Verify MongoDB

```bash
mongosh
> show dbs
> exit
```

### 3. Create Indexes

Indexes are automatically created by setup.sh, but you can manually create them:

```bash
source venv/bin/activate
python3 << 'EOF'
from database.connection import db
from pymongo import ASCENDING

db.connect_sync()

# Create indexes
db.get_sync_collection('files').create_index([('unique_id', ASCENDING)], unique=True)
db.get_sync_collection('users').create_index([('user_id', ASCENDING)], unique=True)
db.get_sync_collection('tokens').create_index([('token', ASCENDING)], unique=True)

print("✅ Indexes created")
db.close_sync()
EOF
```

---

## Bot Configuration

### 1. Add Bots to Channels

**User Bot:**
- Add to all force subscription channels/groups
- Give admin permissions to check members
- Enable "Join requests" permission for private channels

**Admin Bot:**
- Add to storage channel as admin
- Give permission to post messages

### 2. Configure Force Sub Channels

Use admin bot:
```
/add_force_sub
```

Follow prompts to add each channel.

### 3. Set Initial Configuration

Via admin bot:
```
/set_free_media_access
10

/set_deletion_time
30

/set_token_limit
15

/set_password
mypassword123

/set_how_to_verify
https://t.me/your_channel/123
```

---

## Running the System

### Method 1: Run All Components (Recommended)

```bash
./run.sh
```

Press Ctrl+C to stop all services.

### Method 2: Run Individually

**Terminal 1 - Admin Bot:**
```bash
./run_admin_bot.sh
```

**Terminal 2 - User Bot:**
```bash
./run_user_bot.sh
```

**Terminal 3 - Bypass Server:**
```bash
./run_bypass_server.sh
```

### Method 3: Using tmux (Recommended for servers)

```bash
# Install tmux
sudo apt install -y tmux

# Start tmux session
tmux new -s telegram-system

# Split windows
Ctrl+B then %  # Split vertically
Ctrl+B then "  # Split horizontally
Ctrl+B then arrow keys  # Navigate

# In each pane, run:
./run_admin_bot.sh
./run_user_bot.sh
./run_bypass_server.sh

# Detach from session
Ctrl+B then D

# Reattach later
tmux attach -t telegram-system
```

---

## Production Deployment

### 1. Using systemd Services

**Create service files:**

`/etc/systemd/system/telegram-admin-bot.service`:
```ini
[Unit]
Description=Telegram Admin Bot
After=network.target mongodb.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/telegram-resource-system
ExecStart=/home/ubuntu/telegram-resource-system/venv/bin/python3 admin_bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

`/etc/systemd/system/telegram-user-bot.service`:
```ini
[Unit]
Description=Telegram User Bot
After=network.target mongodb.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/telegram-resource-system
ExecStart=/home/ubuntu/telegram-resource-system/venv/bin/python3 user_bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

`/etc/systemd/system/telegram-bypass-server.service`:
```ini
[Unit]
Description=Telegram Bypass Server
After=network.target mongodb.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/telegram-resource-system
ExecStart=/home/ubuntu/telegram-resource-system/venv/bin/python3 bypass_server/run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start services:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-admin-bot
sudo systemctl enable telegram-user-bot
sudo systemctl enable telegram-bypass-server

sudo systemctl start telegram-admin-bot
sudo systemctl start telegram-user-bot
sudo systemctl start telegram-bypass-server

# Check status
sudo systemctl status telegram-admin-bot
sudo systemctl status telegram-user-bot
sudo systemctl status telegram-bypass-server
```

### 2. Using Gunicorn for Bypass Server

For better performance with bypass server:

```bash
pip install gunicorn

# Create systemd service with gunicorn
ExecStart=/home/ubuntu/telegram-resource-system/venv/bin/gunicorn -w 4 -b 152.42.212.81:5000 bypass_server.app:app
```

### 3. Nginx Reverse Proxy (Optional)

If you want to use domain name:

```bash
sudo apt install -y nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/bypass-server
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/bypass-server /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Monitoring

### 1. Check Logs

**Using journalctl (systemd services):**
```bash
# Admin Bot logs
sudo journalctl -u telegram-admin-bot -f

# User Bot logs
sudo journalctl -u telegram-user-bot -f

# Bypass Server logs
sudo journalctl -u telegram-bypass-server -f
```

**Using tail (direct run):**
```bash
tail -f admin_bot.log
tail -f user_bot.log
tail -f bypass_server.log
```

### 2. Monitor Schedulers

Check logs for scheduler activity:
```bash
sudo journalctl -u telegram-user-bot | grep -E "Token Cleanup|Message Deleter|Broadcast Deleter|Token Count Reset"
```

### 3. Database Monitoring

```bash
mongosh

> use telegram_resource_system
> db.users.countDocuments()
> db.files.countDocuments()
> db.tokens.countDocuments()
> db.pending_deletions.countDocuments()
```

### 4. Health Checks

```bash
# Check bypass server
curl http://152.42.212.81:5000/health

# Check bots (via logs)
sudo systemctl status telegram-admin-bot
sudo systemctl status telegram-user-bot
```

---

## Backup & Recovery

### 1. Database Backup

```bash
# Create backup directory
mkdir -p ~/backups

# Backup MongoDB
mongodump --db telegram_resource_system --out ~/backups/$(date +%Y%m%d)

# Compress backup
tar -czf ~/backups/backup_$(date +%Y%m%d).tar.gz ~/backups/$(date +%Y%m%d)
```

### 2. Automated Backups

Create cron job:
```bash
crontab -e

# Add line for daily backup at 3 AM
0 3 * * * mongodump --db telegram_resource_system --out ~/backups/$(date +\%Y\%m\%d) && tar -czf ~/backups/backup_$(date +\%Y\%m\%d).tar.gz ~/backups/$(date +\%Y\%m\%d)
```

### 3. Restore from Backup

```bash
# Extract backup
tar -xzf ~/backups/backup_20251220.tar.gz

# Restore
mongorestore --db telegram_resource_system ~/backups/20251220/telegram_resource_system
```

### 4. Configuration Backup

```bash
# Backup .env and important configs
cp .env ~/.env.backup
```

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed troubleshooting guide.

### Quick Fixes

**Bots not starting:**
```bash
# Check .env file
cat .env | grep TOKEN

# Check MongoDB
sudo systemctl status mongodb

# Check logs
sudo journalctl -u telegram-admin-bot -n 50
```

**Database connection errors:**
```bash
# Restart MongoDB
sudo systemctl restart mongodb

# Check connection
mongosh --eval "db.adminCommand('ping')"
```

**Scheduler not running:**
```bash
# Check user bot logs
sudo journalctl -u telegram-user-bot | grep Scheduler
```

---

## Security Considerations

### 1. Environment Variables

- Never commit .env to git
- Use strong passwords
- Rotate API tokens regularly

### 2. MongoDB Security

```bash
# Enable authentication
sudo nano /etc/mongod.conf

# Add:
security:
  authorization: enabled

# Create admin user
mongosh
> use admin
> db.createUser({
    user: "admin",
    pwd: "strong_password",
    roles: ["root"]
})
```

### 3. Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 5000/tcp # Bypass server
sudo ufw enable
```

### 4. SSL/TLS (Optional)

Use Let's Encrypt with Nginx for HTTPS on bypass server.

---

## Performance Optimization

### 1. MongoDB Optimization

```bash
# Increase cache size in /etc/mongod.conf
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1
```

### 2. Bot Optimization

- Use polling instead of webhooks (already configured)
- Limit concurrent message sending
- Use connection pooling

### 3. Server Resources

- Monitor CPU/RAM usage
- Scale vertically if needed
- Consider load balancing for high traffic

---

## Updates & Maintenance

### 1. Update System

```bash
# Pull latest code
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart services
sudo systemctl restart telegram-admin-bot
sudo systemctl restart telegram-user-bot
sudo systemctl restart telegram-bypass-server
```

### 2. Database Maintenance

```bash
# Compact database
mongosh
> use telegram_resource_system
> db.runCommand({ compact: 'tokens' })
> db.runCommand({ compact: 'users' })
```

---

## Support

For issues and questions:
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Check [FAQ.md](FAQ.md)
- Review logs
- Check GitHub issues

---

## Production Checklist

Before going live:

- [ ] All bot tokens configured
- [ ] Admin IDs set correctly
- [ ] Storage channel created and bot added
- [ ] Force sub channels added
- [ ] URL shortener APIs configured
- [ ] MongoDB running and indexed
- [ ] Bypass server accessible from internet
- [ ] All services running
- [ ] Health checks passing
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Logs being captured
- [ ] Security hardened
- [ ] Test resource delivery
- [ ] Test verification flow
- [ ] Test force sub
- [ ] Test bypass detection

---

**You're now ready to deploy! Good luck! 🚀**
