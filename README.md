# Telegram Resource Distribution System

A comprehensive, production-ready Telegram bot system for distributing resources with verification, force subscription, and bypass detection. Monetize your content delivery through URL shorteners while preventing users from bypassing the verification process.

[![Python Version](https://img.shields.io/badge/python-3.10.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Private-red.svg)]()
[![Status](https://img.shields.io/badge/status-Production%20Ready-green.svg)]()

---

## 🌟 Features

### Core Functionality
- **📦 Resource Management**: Upload and distribute files with unique links
- **📚 Batch Distribution**: Send multiple files with a single link
- **🔐 Force Subscription**: Require channel subscriptions before access
- **✅ Verification System**: Token-based verification through URL shorteners
- **🛡️ Bypass Detection**: Prevent users from bypassing URL shorteners
- **⏰ Auto-deletion**: Automatically delete messages after set time
- **📢 Broadcasting**: Send messages to all users
- **👥 User Management**: Ban/unban users, track statistics
- **💰 Revenue Generation**: Earn through URL shortener views

### Advanced Features
- **Multi-URL Shortener Support**: Use multiple shorteners simultaneously
- **Smart Scheduling**: Background tasks for cleanup and maintenance
- **Persistent Storage**: Messages scheduled for deletion survive bot restarts
- **Join Request Tracking**: Tracks private channel join requests
- **ZIP Password Protection**: Automatic password captions for ZIP files
- **Customizable Settings**: All parameters configurable via admin commands
- **Production Ready**: systemd services, monitoring, backups

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Documentation](#-documentation)
- [Architecture](#-architecture)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/telegram-resource-system.git
cd telegram-resource-system

# 2. Run setup
chmod +x setup.sh
./setup.sh

# 3. Configure environment
nano .env  # Add your bot tokens and settings

# 4. Start system
./run.sh
```

That's it! Your system is now running. 🎉

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+ / Debian 11+ / Any Linux distro
- **Python**: 3.10.11 (exact version)
- **MongoDB**: 4.4+
- **RAM**: 1GB
- **Storage**: 10GB
- **Network**: Public IP or domain (for bypass server)

### Recommended for Production
- **RAM**: 2GB+
- **Storage**: 20GB+
- **CPU**: 2 cores
- **Bandwidth**: Unlimited

---

## 📥 Installation

### Automated Installation (Recommended)

```bash
# Download and extract
tar -xzf telegram-resource-system.tar.gz
cd telegram-resource-system

# Run setup script
./setup.sh
```

The setup script will:
- ✅ Check Python 3.10.11
- ✅ Check/install MongoDB
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Create .env file
- ✅ Setup database indexes
- ✅ Make scripts executable

### Manual Installation

```bash
# Install Python 3.10
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev

# Install MongoDB
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

---

## ⚙️ Configuration

### 1. Create Telegram Bots

Visit [@BotFather](https://t.me/BotFather) and create two bots:

**Admin Bot** - For resource management
**User Bot** - For resource delivery

Save both bot tokens.

### 2. Configure .env File

```bash
nano .env
```

**Required Settings:**

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

# URL Shorteners
AROLINKS_API_TOKEN=your_token
AROLINKS_BASE_URL=https://arolinks.com/api

LINKPAYS_API_TOKEN=your_token
LINKPAYS_BASE_URL=https://linkpays.in/api

# Bypass Server
SERVER_HOST=152.42.212.81
SERVER_PORT=5000
SERVER_SECRET_KEY=your_random_secret_key
```

### 3. Setup Bot Commands

Configure commands via [@BotFather](https://t.me/BotFather):

**Admin Bot**: See [DEPLOYMENT.md](DEPLOYMENT.md) for full command list

**User Bot**:
```
start - Start the bot
help - Get help information
create_new_token - Create new verification token
```

---

## 🎯 Usage

### Starting the System

**All Components at Once:**
```bash
./run.sh
```

**Individual Components:**
```bash
./run_admin_bot.sh       # Admin bot only
./run_user_bot.sh        # User bot only
./run_bypass_server.sh   # Bypass server only
```

**Using tmux (Recommended for servers):**
```bash
tmux new -s telegram-system
# Split window and run each component
./run_admin_bot.sh
./run_user_bot.sh
./run_bypass_server.sh
# Ctrl+B then D to detach
```

### Admin Bot Commands

```bash
# Resource Management
/generate_link          # Generate single resource link
/generate_batch        # Generate batch link
/regenerate_post       # Regenerate existing post

# Broadcasting
/broadcast             # Send message to all users

# Force Subscription
/add_force_sub         # Add channel to force sub
/remove_force_sub      # Remove channel
/list_force_sub        # List all channels

# User Management
/ban_user              # Ban a user
/unban_user            # Unban a user
/verification_stats    # View statistics

# Configuration
/set_free_media_access # Set free media count
/set_paid_access       # Set paid access for user
/set_password          # Set ZIP password
/set_deletion_time     # Set auto-deletion time
/set_token_limit       # Set token generation limit
/set_how_to_verify     # Set verification guide link
```

### User Bot Workflow

1. **User clicks link** in public channel
2. **Force Sub Check**: Must join required channels
3. **Verification Check**: Must verify via URL shortener
4. **Resource Delivery**: Receives files
5. **Auto-deletion**: Files deleted after set time
6. **Re-download**: Can get files again via link

---

## 📚 Documentation

Comprehensive documentation is available:

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[FAQ.md](FAQ.md)** - Frequently asked questions
- **[schedulers/README.md](schedulers/README.md)** - Background scheduler docs
- **[bypass_server/README.md](bypass_server/README.md)** - Bypass server docs

---

## 🏗️ Architecture

```
Admin Bot ──┐
            ├──► Shared Layer ──► Database (MongoDB)
User Bot ───┤                      ▲
            │                      │
Bypass Server ──────────────────────┘

Schedulers (in User Bot):
├── Token Cleanup (2x daily)
├── Message Deleter (every minute)
├── Broadcast Deleter (hourly)
└── Token Count Reset (daily)
```

### Technology Stack

- **Backend**: Python 3.10.11
- **Bot Framework**: aiogram 3.4.1
- **Web Server**: Flask 3.0.0
- **Database**: MongoDB 4.4+
- **Scheduler**: APScheduler 3.10.4
- **Frontend**: HTML5, CSS3, JavaScript

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture.

---

## 🔧 Troubleshooting

### Common Issues

**Bot not responding?**
```bash
# Check if running
ps aux | grep python3

# Check logs
sudo journalctl -u telegram-admin-bot -n 50

# Restart
./run.sh
```

**Database connection error?**
```bash
# Check MongoDB
sudo systemctl status mongodb

# Restart MongoDB
sudo systemctl restart mongodb
```

**Bypass detection issues?**
- Check time threshold (120 seconds)
- Verify URL shortener domains in whitelist
- Check referer header

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

---

## ❓ FAQ

**Q: Do I need coding knowledge?**
A: Minimal. Just follow the setup guide and use bot commands.

**Q: How many users can it handle?**
A: 1,000-5,000 active users with default VPS.

**Q: Can I use different URL shorteners?**
A: Yes! Add any shortener with API support to .env.

**Q: Is it secure?**
A: Yes, with proper configuration. Includes admin middleware, bypass detection, and token validation.

**Q: Can I monetize?**
A: Yes! Earn through URL shortener views.

See [FAQ.md](FAQ.md) for more questions.

---

## 🎯 Production Deployment

### Using systemd Services

Create service files for each component:

```bash
sudo nano /etc/systemd/system/telegram-admin-bot.service
sudo nano /etc/systemd/system/telegram-user-bot.service
sudo nano /etc/systemd/system/telegram-bypass-server.service
```

Enable and start:
```bash
sudo systemctl enable telegram-admin-bot telegram-user-bot telegram-bypass-server
sudo systemctl start telegram-admin-bot telegram-user-bot telegram-bypass-server
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete production setup.

---

## 🔒 Security

- ✅ Admin authentication middleware
- ✅ Token-based verification
- ✅ Bypass detection (time & origin)
- ✅ Environment variable protection
- ✅ Rate limiting
- ✅ Input validation

### Security Best Practices

```bash
# Secure .env file
chmod 600 .env

# Enable MongoDB auth (recommended)
# Edit /etc/mongod.conf

# Use HTTPS for bypass server
# Use Let's Encrypt + Nginx

# Regular backups
mongodump --db telegram_resource_system --out ~/backup
```

---

## 📊 Monitoring

### Health Checks

```bash
# Check services
sudo systemctl status telegram-admin-bot
sudo systemctl status telegram-user-bot
sudo systemctl status telegram-bypass-server

# Check bypass server health
curl http://152.42.212.81:5000/health

# Check database
mongosh --eval "db.adminCommand('ping')"
```

### View Logs

```bash
# Bot logs
sudo journalctl -u telegram-admin-bot -f
sudo journalctl -u telegram-user-bot -f

# Bypass server logs
sudo journalctl -u telegram-bypass-server -f
```

---

## 🔄 Backup & Recovery

### Automated Backups

```bash
# Add to crontab
crontab -e

# Daily backup at 3 AM
0 3 * * * mongodump --db telegram_resource_system --out ~/backups/$(date +\%Y\%m\%d)
```

### Manual Backup

```bash
# Backup database
mongodump --db telegram_resource_system --out ~/backup

# Compress
tar -czf backup_$(date +%Y%m%d).tar.gz ~/backup

# Backup config
cp .env ~/.env.backup
```

### Restore

```bash
# Restore from backup
mongorestore --db telegram_resource_system ~/backup/telegram_resource_system
```

---

## 📈 Performance

### Benchmarks

- **Command Response**: <100ms
- **Resource Delivery**: <500ms
- **Concurrent Users**: 100+
- **Messages/Second**: 20-30

### Optimization Tips

- Use indexes (auto-created)
- Regular database maintenance
- Monitor disk space
- Use SSD storage
- Scale vertically for more users

---

## 🛠️ Development

### Project Structure

```
telegram-resource-system/
├── admin_bot/          # Admin bot code
├── user_bot/           # User bot code
├── bypass_server/      # Bypass detection server
├── database/           # Database models & operations
├── shared/             # Shared utilities
├── schedulers/         # Background tasks
├── .env               # Configuration
└── run.sh             # Launch script
```

### Adding Features

1. Create new handler module
2. Register in main.py
3. Add command to @BotFather
4. Update documentation

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

## 📞 Support

- **Documentation**: Check docs in repo
- **Issues**: Create GitHub issue
- **Questions**: See FAQ.md

---

## 📜 License

Private Project - All Rights Reserved

---

## 🎉 Acknowledgments

Built with:
- [aiogram](https://github.com/aiogram/aiogram) - Telegram Bot Framework
- [Flask](https://flask.palletsprojects.com/) - Web Framework
- [MongoDB](https://www.mongodb.com/) - Database
- [APScheduler](https://github.com/agronholm/apscheduler) - Task Scheduler

---

## 📸 Screenshots

*Add screenshots of your bot in action here*

---

## 🗺️ Roadmap

- [ ] Web dashboard
- [ ] Payment integration
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] CDN integration
- [ ] API endpoints

---

**⭐ Star this repo if you find it useful!**

**🚀 Ready to deploy? Follow [DEPLOYMENT.md](DEPLOYMENT.md)**

---

Made with ❤️ for the Telegram community
