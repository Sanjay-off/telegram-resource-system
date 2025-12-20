# Bypass Detection Server

A Flask-based server that validates verification tokens and prevents users from bypassing URL shorteners.

## Features

- **Token Validation**: Validates tokens from the database
- **Time-based Detection**: Detects if token was accessed too quickly (< 2 minutes)
- **Origin Validation**: Checks HTTP Referer header against whitelist
- **Attractive UI**: Modern, responsive design with animations
- **Auto-redirect**: 3-second countdown before redirecting to Telegram
- **Error Handling**: User-friendly error pages

## How It Works

### Validation Flow

1. **Token Lookup**: Check if token exists in database
2. **Status Check**: Verify token hasn't been used
3. **Time Validation**: Ensure at least 2 minutes have passed since token creation
4. **Origin Validation**: Verify request came from whitelisted URL shortener
5. **Update Status**: Mark token as verified or bypassed
6. **Redirect**: Send user to Telegram bot with verification payload

### Bypass Detection Rules

**BYPASS DETECTED** if:
- Time difference < 2 minutes (120 seconds)
- Referer header is missing
- Referer domain not in whitelist

**VERIFIED** if:
- Time difference >= 2 minutes
- Referer header present
- Referer domain in whitelist
- Token status is "not_used"

## Endpoints

### `/redirect?token={token}`

Main verification endpoint.

**Query Parameters:**
- `token`: 35-character verification token

**Responses:**
- `200`: Success - Shows countdown page
- `400`: Token already used
- `404`: Token not found
- Redirect: On bypass detection

### `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Templates

### error.html

Shown when:
- Token not found
- Token already used
- Token expired

Features:
- Red error icon
- Error message display
- "Get New Token" button

### redirect.html

Shown when:
- Verification successful

Features:
- Green success icon
- 3-second countdown
- Auto-redirect
- Manual redirect button
- Loading animation

## Static Assets

### CSS (style.css)

- Gradient background
- Card-based layout
- Smooth animations
- Responsive design
- Mobile-friendly

### JavaScript (inline)

- Countdown timer
- Auto-redirect logic
- Manual redirect handling

## Configuration

Set in `.env`:

```env
SERVER_HOST=152.42.212.81
SERVER_PORT=5000
SERVER_SECRET_KEY=your_secret_key
USER_BOT_USERNAME=your_bot_username
```

## Running the Server

### Development

```bash
python bypass_server/app.py
```

### Production (with Gunicorn)

```bash
gunicorn -w 4 -b 152.42.212.81:5000 bypass_server.app:app
```

## Integration

### URL Shortener Flow

1. User Bot generates token
2. Creates destination URL: `http://SERVER_HOST:SERVER_PORT/redirect?token={token}`
3. Shortens URL using random URL shortener
4. User clicks shortened URL
5. URL shortener redirects to destination
6. Server validates token
7. Server redirects to Telegram

### Whitelist Domains

Automatically generated from URL shorteners in `.env`:

```python
AROLINKS_BASE_URL=https://arolinks.com/api
LINKPAYS_BASE_URL=https://linkpays.in/api
```

Whitelist includes:
- `arolinks.com`
- `linkpays.in`
- ... (all configured shorteners)

## Security Features

- Token expiration (2 days)
- Time-based bypass detection
- Origin validation
- Status tracking
- One-time use tokens

## Error Handling

All errors show user-friendly pages with:
- Clear error messages
- Visual indicators
- Action buttons
- Consistent design

## Monitoring

Check server status:
```bash
curl http://SERVER_HOST:SERVER_PORT/health
```

## Troubleshooting

### Token always shows "not found"

- Check database connection
- Verify token exists in database
- Check MongoDB is running

### Bypass always detected

- Verify URL shortener domains in whitelist
- Check Referer header is being sent
- Ensure 2+ minutes passed since token creation

### Server not starting

- Check port is not in use
- Verify all dependencies installed
- Check `.env` configuration
- Ensure MongoDB is accessible
