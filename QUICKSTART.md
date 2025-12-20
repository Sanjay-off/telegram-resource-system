# Quick Start Guide

Get your Telegram Resource Distribution System up and running in 10 minutes!

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Ubuntu/Debian Linux server or VPS
- [ ] Root or sudo access
- [ ] Internet connection
- [ ] Two Telegram bot tokens from @BotFather
- [ ] Private Telegram channel for storage
- [ ] At least one URL shortener API token

---

## 5-Step Setup

### Step 1: Download & Extract (1 minute)

```bash
# Download the system
wget https://yourserver.com/telegram-resource-system.tar.gz

# Extract
tar -xzf telegram-resource-system.tar.gz
cd telegram-resource-system
```

### Step 2: Run Setup Script (2 minutes)

```bash
# Make executable
chmod +x setup.sh

# Run setup
./setup.sh
```

This installs Python 3.10, MongoDB, creates virtual environment, and installs dependencies.

### Step 3: Configure Environment (3 minutes)

```bash
# Edit configuration
nano .env
```

**Minimum required configuration:**

```env
# Admin Bot Token (from @BotFather)
ADMIN_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Your Telegram User ID (from @userinfobot)
ADMIN_IDS=123456789

# User Bot Token (from @BotFather)
USER_BOT_TOKEN=789012:XYZ-GHI5678jklMno-pqr90W3v2u456wx22
USER_BOT_USERNAME=your_user_bot

# Storage Channel ID (forward message to @userinfobot)
STORAGE_CHANNEL_ID=-1001234567890

# At least one URL shortener
AROLINKS_API_TOKEN=your_arolinks_token
AROLINKS_BASE_URL=https://arolinks.com/api

# Your server IP (important!)
SERVER_HOST=YOUR_SERVER_IP
SERVER_PORT=5000
```

Save and exit (Ctrl+X, Y, Enter).

### Step 4: Configure Bot Commands (2 minutes)

Go to [@BotFather](https://t.me/BotFather):

**For Admin Bot:**
```
/mybots
→ Select your admin bot
→ Edit Bot
→ Edit Commands
→ Paste all commands from DEPLOYMENT.md
```

**For User Bot:**
```
/mybots
→ Select your user bot
→ Edit Bot
→ Edit Commands
→ Paste:
start - Start the bot
help - Get help information  
create_new_token - Create new verification token
```

### Step 5: Start the System (30 seconds)

```bash
# Start everything
./run.sh
```

**You should see:**
```
🚀 Starting all services...
✅ Admin Bot started
✅ User Bot started
✅ Bypass Server started
✅ All services started successfully!
```

---

## First Steps After Setup

### 1. Test Admin Bot

Open Telegram and start your admin bot:
```
/start
```

You should see the welcome message.

### 2. Add Force Sub Channels

```
/add_force_sub
[Your channel link]
[Placeholder name]
```

Repeat for each channel.

### 3. Configure Settings

```bash
# Set free media access count
/set_free_media_access
10

# Set deletion time (minutes)
/set_deletion_time
30

# Set ZIP password
/set_password
mypassword123

# Set token limit
/set_token_limit
15
```

### 4. Generate Your First Link

```bash
/generate_link
```

Follow the prompts:
1. Upload your resource (file/video/photo)
2. Enter post number (e.g., 1)
3. Enter description
4. Enter extra message

Bot will generate a template with download button!

### 5. Post to Public Channel

Copy the generated template and post it in your public Telegram channel.

---

## Verification

Test the complete flow:

1. **As user**, click the download button in your public channel
2. Bot should check force subscription
3. Bot should ask for verification
4. Click "Verify Now", complete URL shortener
5. Return to bot
6. Receive the resource!

---

## Common Issues

### "Bot not responding"

**Check if running:**
```bash
ps aux | grep python3
```

**Restart:**
```bash
./run.sh
```

### "MongoDB connection error"

**Start MongoDB:**
```bash
sudo systemctl start mongodb
```

### "Not authorized" message

**Check ADMIN_IDS in .env:**
```bash
cat .env | grep ADMIN_IDS
```

Must include your Telegram user ID.

### "Bypass always detected"

**Check SERVER_HOST in .env:**
```bash
cat .env | grep SERVER_HOST
```

Must be your actual server IP, not 152.42.212.81 (example IP).

---

## Production Deployment

For long-term production use:

### 1. Create systemd Services

```bash
# See DEPLOYMENT.md for complete instructions
sudo nano /etc/systemd/system/telegram-admin-bot.service
sudo nano /etc/systemd/system/telegram-user-bot.service
sudo nano /etc/systemd/system/telegram-bypass-server.service
```

### 2. Enable Auto-start

```bash
sudo systemctl enable telegram-admin-bot
sudo systemctl enable telegram-user-bot
sudo systemctl enable telegram-bypass-server
```

### 3. Start Services

```bash
sudo systemctl start telegram-admin-bot
sudo systemctl start telegram-user-bot
sudo systemctl start telegram-bypass-server
```

### 4. Setup Backups

```bash
crontab -e

# Add daily backup at 3 AM
0 3 * * * mongodump --db telegram_resource_system --out ~/backups/$(date +\%Y\%m\%d)
```

---

## Next Steps

- 📖 Read [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production setup
- 🏗️ Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
- ❓ Check [FAQ.md](FAQ.md) for common questions
- 🔧 See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for issues

---

## Monitoring

### Check Service Status

```bash
# systemd services
sudo systemctl status telegram-admin-bot
sudo systemctl status telegram-user-bot
sudo systemctl status telegram-bypass-server

# Or if using ./run.sh
ps aux | grep python3
```

### View Logs

```bash
# systemd
sudo journalctl -u telegram-admin-bot -f
sudo journalctl -u telegram-user-bot -f

# Or check stdout if running directly
```

### Health Check

```bash
# Bypass server
curl http://YOUR_SERVER_IP:5000/health

# Should return: {"status": "ok"}
```

---

## Getting Help

**Problem? Follow this order:**

1. ✅ Check this Quick Start guide
2. ✅ Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. ✅ Check [FAQ.md](FAQ.md)
4. ✅ Review logs for errors
5. ✅ Create GitHub issue with details

---

## Tips for Success

✅ **Start simple**: Use one URL shortener first
✅ **Test thoroughly**: Try the complete flow before going public
✅ **Monitor logs**: Check for errors regularly
✅ **Backup daily**: Automate MongoDB backups
✅ **Update regularly**: Keep dependencies updated
✅ **Read docs**: Everything is documented!

---

## Security Checklist

Before going public, ensure:

- [ ] .env file has secure permissions (chmod 600)
- [ ] MongoDB authentication enabled (optional but recommended)
- [ ] Firewall configured (only necessary ports open)
- [ ] Bot tokens not shared anywhere
- [ ] Admin IDs correct
- [ ] Regular backups configured
- [ ] HTTPS on bypass server (optional but recommended)

---

**🎉 Congratulations! Your system is ready!**

**💰 Start monetizing your content distribution!**

---

Need more details? See complete documentation:
- **Full Setup**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **FAQ**: [FAQ.md](FAQ.md)
