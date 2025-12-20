# Frequently Asked Questions (FAQ)

Common questions and answers about the Telegram Resource Distribution System.

## General Questions

### What is this system?

A comprehensive Telegram bot system for distributing resources (files, documents, videos, etc.) with verification, force subscription, and bypass detection. It allows you to monetize content delivery through URL shorteners while preventing users from bypassing the verification process.

### What can it do?

- **Resource Management**: Upload and distribute files with unique links
- **Batch Distribution**: Send multiple files with a single link
- **Force Subscription**: Require users to join channels before accessing content
- **Verification System**: Token-based verification through URL shorteners
- **Bypass Detection**: Prevent users from bypassing URL shorteners
- **Auto-deletion**: Automatically delete messages after a set time
- **Broadcasting**: Send messages to all users
- **User Management**: Ban/unban users, track statistics
- **Revenue Generation**: Earn through URL shortener views

### Do I need coding knowledge?

Minimal knowledge required:
- **Setup**: Follow deployment guide (copy/paste commands)
- **Configuration**: Edit .env file with your tokens
- **Usage**: Use bot commands (no coding)
- **Maintenance**: Basic Linux commands helpful

### How much does it cost?

- **Software**: Free and open source
- **Server**: $5-20/month (VPS hosting)
- **Domain**: Optional, ~$10/year
- **Telegram Bots**: Free
- **URL Shorteners**: Free (with ads) or paid plans

---

## Setup Questions

### What are the system requirements?

**Minimum:**
- 1GB RAM
- 10GB storage
- Ubuntu 20.04+
- Python 3.10.11
- MongoDB 4.4+

**Recommended:**
- 2GB+ RAM
- 20GB+ storage
- Public IP or domain

### Why Python 3.10.11 specifically?

The system is developed and tested with Python 3.10.11. Other versions may work but are not guaranteed. Python 3.11+ has some breaking changes that may cause issues.

### Can I use a different database?

The system is designed for MongoDB. Migrating to another database would require significant code changes.

### Do I need a VPS?

Yes, for production use. You need:
- 24/7 uptime
- Public IP (for bypass server)
- Persistent storage

Local testing is possible but not recommended for real users.

### Can I run this on Windows?

The system is designed for Linux. While technically possible on Windows, deployment scripts and commands assume Linux. WSL2 might work but is not officially supported.

---

## Bot Questions

### How do I create Telegram bots?

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Follow prompts to choose name and username
4. Save the bot token
5. Repeat for second bot (admin and user bots)

### Why do I need two bots?

- **Admin Bot**: For admins only, manages resources and settings
- **User Bot**: For end users, delivers resources and handles verification

Separation ensures security and clean organization.

### Can users use admin commands?

No. Admin bot has middleware that blocks non-admin users. Only users with IDs in ADMIN_IDS can use admin bot.

### How many admins can I have?

Unlimited. Add multiple user IDs to ADMIN_IDS in .env:
```env
ADMIN_IDS=123456789,987654321,111222333
```

### Can I use one bot for everything?

Not recommended. Two bots provide:
- Better security (admin functions isolated)
- Clearer organization
- Easier management
- No command conflicts

---

## Resource Management

### What file types are supported?

- Documents (.pdf, .zip, .docx, etc.)
- Videos (.mp4, .mkv, etc.)
- Audio (.mp3, .wav, etc.)
- Photos (.jpg, .png, etc.)
- Text (plain text messages)

### What's the maximum file size?

Telegram's limits:
- Photos: 10MB
- Other files: 2GB

### How do I upload resources?

Via admin bot:
1. `/generate_link` - Single resource
2. Upload file
3. Enter post number (unique)
4. Enter description
5. Enter extra message
6. Bot generates template with download button

### What is a batch?

Multiple resources sent with a single link. Use `/generate_batch` to:
1. Upload multiple files
2. Generate one unique ID
3. Users get all files at once

### Can I edit uploaded resources?

No direct editing. To update:
1. Generate new link with new post number
2. Old resource remains in database
3. Consider using same post number if replacing (delete old first)

### How do I delete resources?

Currently no delete command. Manually via MongoDB:
```bash
mongosh
> use telegram_resource_system
> db.files.deleteOne({post_no: 123})
```

---

## Verification System

### How does verification work?

1. User clicks download link
2. Bot checks if verified (user_access_count > 0)
3. If not verified:
   - Generate token
   - Create shortened URL
   - Show verification button
4. User completes URL shortener
5. Bypass server validates
6. User gets access count
7. Can download resources

### What is user_access_count?

Number of free downloads a user has. Decrements by 1 per resource. When 0, user must verify again.

### How do I set the access count?

Via admin bot:
```
/set_free_media_access
10
```

Users get 10 downloads per verification.

### Can I give specific users more access?

Yes, via admin bot:
```
/set_paid_access
[User ID]
100
```

### What is the token generation limit?

Daily limit of tokens a user can generate. Prevents abuse. Default: 15 per day.

Set via:
```
/set_token_limit
20
```

### Why do tokens expire?

Tokens expire after 2 days to:
- Reduce database bloat
- Force users to verify again
- Prevent token sharing

---

## Bypass Detection

### What is bypass detection?

System that prevents users from using bypass tools to skip URL shorteners. Detects bypasses via:
- **Time check**: Too fast = bypass
- **Origin check**: Wrong source = bypass

### How does time checking work?

If user accesses destination < 2 minutes after token creation, it's marked as bypass. Shorteners typically take 2+ minutes with ads/captchas.

### How does origin checking work?

Server checks HTTP Referer header. Must come from whitelisted URL shortener domains. Direct access = bypass.

### What happens if bypass is detected?

- Token marked as "bypassed"
- User redirected to bot
- Bot shows "bypass detected" message
- User must try again properly
- No access count given

### Can I disable bypass detection?

Not recommended. It's the core anti-abuse feature. However, you can:
- Increase time threshold in constants.py
- Remove origin check (not recommended)

### Why are some legitimate users marked as bypassed?

Possible reasons:
- User very fast (< 2 minutes)
- Browser blocking referer header
- VPN/proxy interference
- URL shortener issue

Adjust BYPASS_TIME_THRESHOLD if needed.

---

## URL Shorteners

### Which URL shorteners are supported?

Any shortener with API that returns:
- `shortenedUrl`
- `shorturl`
- `short_url`
- `url`

Examples: Arolinks, Linkpays, GPLinks, ShrinkMe, etc.

### How do I add URL shorteners?

In .env file:
```env
SHORTENER_NAME_API_TOKEN=your_token
SHORTENER_NAME_BASE_URL=https://shortener.com/api
```

System auto-detects all shorteners.

### How many shorteners should I use?

Recommended: 3-5 shorteners
- Provides redundancy
- Different payout rates
- Better user experience

### Do I need paid URL shortener plans?

No, free plans work. Paid plans offer:
- Higher payouts
- Better support
- More features

### How does the bot choose which shortener?

Randomly selects from configured shorteners each time. Distributes load evenly.

---

## Force Subscription

### What is force subscription?

Requires users to join your Telegram channels/groups before accessing resources. Helps grow your community.

### How many channels can I add?

Unlimited. Add via admin bot:
```
/add_force_sub
```

### Do channels need to be public?

No. Both public and private channels work:
- **Public**: Users join directly
- **Private**: Users request to join, admin approves

### How does the bot check membership?

Via Telegram Bot API:
- Checks user status in channel
- Verifies membership or pending request
- For private channels, tracks join requests

### What if user leaves channel after joining?

Next time they try to access resources, force sub check will trigger again. They must rejoin.

### Can I remove force sub channels?

Yes, via admin bot:
```
/remove_force_sub
```

### Do admins need to approve join requests?

For private channels:
- User requests to join
- Bot tracks request
- Admin must manually approve in channel
- Bot considers approved requests as subscribed

---

## Broadcasting

### What is broadcasting?

Send a message to all users at once. Useful for announcements, promotions, updates.

### How do I broadcast?

Via admin bot:
```
/broadcast
```

Upload message (text/photo/video) and set duration.

### What is broadcast duration?

How long the broadcast stays in user chats before auto-deletion. Set in hours.

### How fast are broadcasts sent?

2 users per second (rate limited) to prevent:
- Telegram API limits
- Bot getting banned
- Server overload

### Can I cancel a broadcast?

Once started, no. Best to:
- Test with small user base first
- Double-check content
- Set appropriate duration

---

## Auto-Deletion

### Why do messages auto-delete?

Per Telegram's terms, prevents chat clutter, encourages timely downloads, creates urgency.

### How do I set deletion time?

Via admin bot:
```
/set_deletion_time
30
```

Time in minutes. Default: 30 minutes.

### What happens after deletion?

User receives notification:
```
Previous Message was Deleted 🗑
Click Here to get files again
[Click Here] [Close]
```

### Do users lose access?

No. They can click "Click Here" to get resources again (costs 1 access count again).

### Can I disable auto-deletion?

Set very high deletion time:
```
/set_deletion_time
10080
```
(7 days = 10080 minutes)

Not recommended due to storage and terms concerns.

---

## User Management

### How do I ban a user?

Via admin bot:
```
/ban_user
[User ID]
```

### How do I find user ID?

User can message [@userinfobot](https://t.me/userinfobot) or check logs when they interact with your bot.

### What happens when user is banned?

- Cannot start user bot
- Cannot access resources
- Cannot verify
- Sees "You are banned" message

### How do I unban?

```
/unban_user
[User ID]
```

### Can I see user statistics?

```
/verification_stats
```

Shows:
- Total users
- Verified users
- Unverified users
- Verification rate

---

## Maintenance

### How often should I backup?

Recommended:
- **Daily**: Automated MongoDB backups
- **Weekly**: Manual full system backup
- **Before updates**: Always backup first

### What needs to be backed up?

- MongoDB database (critical)
- .env file (configuration)
- Custom modifications (if any)

### How do I update the system?

```bash
# Backup first!
mongodump --db telegram_resource_system --out ~/backup

# Pull updates
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart services
./run.sh
```

### Should I monitor the system?

Yes. Monitor:
- Bot uptime
- Database health
- Disk space
- Scheduler activity
- Error logs

### How much disk space do I need?

Depends on:
- Number of resources
- File sizes
- User count
- Log retention

Estimate: 10GB + (resources size × 1.5)

---

## Performance

### How many users can it handle?

With default VPS (2GB RAM):
- **Active users**: 1,000-5,000
- **Total users**: 10,000-50,000
- **Resources**: Unlimited (stored in Telegram)

### What if I have more users?

Scale up:
- Increase RAM
- Use dedicated database server
- Load balancing (advanced)
- Multiple bot instances

### Are there rate limits?

Telegram Bot API limits:
- 30 messages/second per bot
- 20 requests/second per bot
- Broadcast rate: 2 users/second (our limit)

### How can I optimize performance?

- Use indexes (done automatically)
- Regular database maintenance
- Monitor and clean logs
- Optimize MongoDB cache
- Use SSD storage

---

## Security

### Is the system secure?

Yes, with proper configuration:
- Admin middleware blocks unauthorized access
- Token-based verification
- Bypass detection prevents abuse
- Environment variables for secrets
- MongoDB can be password-protected

### Should I enable MongoDB authentication?

Yes, for production:
```bash
# In /etc/mongod.conf
security:
  authorization: enabled
```

### Should I use HTTPS?

Yes, for bypass server. Use:
- Let's Encrypt (free)
- Nginx reverse proxy
- Cloudflare (optional)

### How do I secure .env file?

```bash
chmod 600 .env
```

Never commit to git:
```bash
echo ".env" >> .gitignore
```

### Can users hack the system?

With proper configuration, very difficult:
- No exposed database
- Token validation server-side
- Bypass detection active
- Rate limiting enabled

---

## Troubleshooting

### Bot not responding?

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

Quick checks:
1. Bot running?
2. MongoDB running?
3. Correct bot token?
4. Admin ID configured?

### Database connection errors?

```bash
sudo systemctl restart mongodb
mongosh --eval "db.adminCommand('ping')"
```

### Bypass detection issues?

Check:
- Time threshold (120 seconds)
- Whitelist domains
- Referer header logging

---

## Getting Help

### Where can I get support?

1. Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Check this FAQ
3. Review [DEPLOYMENT.md](DEPLOYMENT.md)
4. Search GitHub issues
5. Create detailed bug report

### How do I report bugs?

Include:
- Error messages (full)
- Steps to reproduce
- System info (OS, Python version)
- Log excerpts
- What you've tried

### Can I request features?

Yes! Create GitHub issue with:
- Feature description
- Use case
- Why it's needed
- Proposed implementation (optional)

---

**Still have questions? Check the documentation or create an issue! 📚**
