# Telegram Resource Distribution System

A comprehensive Telegram bot system for distributing resources with verification and bypass detection.

## Features

- **Admin Bot**: Manage resources, force sub channels, user verification, broadcasting
- **User Bot**: Deliver resources with force subscription and verification checks
- **Bypass Detection Server**: Prevent users from bypassing URL shortener verification
- **MongoDB Storage**: Persistent data storage
- **Multiple URL Shorteners**: Support for multiple URL shortening services

## System Requirements

- Python 3.10.11
- MongoDB (local or remote)
- Telegram Bot Tokens (Admin & User)

## Installation

### Step 1: Clone and Setup

```bash
cd telegram-resource-system
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with your values
```

### Step 3: Setup MongoDB

```bash
# Install MongoDB (Ubuntu/Debian)
sudo apt update
sudo apt install -y mongodb

# Start MongoDB
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### Step 4: Configure Telegram Bots

1. Create two bots via @BotFather
2. Get bot tokens
3. Add tokens to .env file
4. Set bot commands via @BotFather

## Bot Commands Setup

### Admin Bot Commands (@BotFather)
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

### User Bot Commands (@BotFather)
```
start - Start the bot
help - Get help information
create_new_token - Create new verification token
```

## Running the System

### Option 1: Run Individually

```bash
# Terminal 1: Admin Bot
python admin_bot/main.py

# Terminal 2: User Bot
python user_bot/main.py

# Terminal 3: Bypass Server
python bypass_server/app.py
```

### Option 2: Run All Together (Coming in Phase 7)

```bash
./run.sh
```

## Project Structure

```
telegram-resource-system/
├── admin_bot/          # Admin bot code
├── user_bot/           # User bot code
├── bypass_server/      # Bypass detection server
├── database/           # Database models and operations
├── shared/             # Shared utilities and config
├── schedulers/         # Background tasks
├── .env               # Environment variables
└── requirements.txt   # Python dependencies
```

## Configuration

All configuration is done via the `.env` file:

- Bot tokens and admin IDs
- MongoDB connection
- URL shortener API credentials
- Server configuration
- Message effects

## URL Shortener Setup

Add multiple URL shorteners by following this pattern in `.env`:

```env
SHORTENER_NAME_API_TOKEN=your_token
SHORTENER_NAME_BASE_URL=https://example.com/api
```

The system will randomly select from available shorteners.

## Database Collections

- `files`: Resource metadata
- `users`: User information
- `tokens`: Verification tokens
- `admin_config`: System configuration
- `broadcasts`: Broadcast messages
- `pending_deletions`: Messages scheduled for deletion
- `token_generator_count`: Daily token generation tracking

## Security Features

- Admin-only access for admin bot
- Token expiration (2 days)
- Bypass detection (time & origin based)
- Daily token generation limits
- User ban system

## Support

For issues or questions, please check the documentation or create an issue.

## License

Private Project - All Rights Reserved
