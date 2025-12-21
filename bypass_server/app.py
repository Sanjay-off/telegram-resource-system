import asyncio
from flask import Flask, request, render_template, redirect
from database.connection import db
from bypass_server.utils import token_validator
from shared.config import config

app = Flask(__name__)
app.secret_key = config.SERVER_SECRET_KEY

db.connect_sync()

def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

@app.route('/redirect', methods=['GET'])
def redirect_endpoint():
    token = request.args.get('token')
    # print(token_validator.whitelist_domains)
    if not token:
        return render_template(
            'error.html',
            error_message="Token invalid or expired or used",
            bot_link=f"https://t.me/{config.USER_BOT_USERNAME}?start=newToken"
        ), 400
    
    referer = request.headers.get('Referer')
    # print(referer,"========")
    try:
        is_valid, status, token_data = token_validator.validate_token(token, referer)
    except Exception as e:
        print(f"Error validating token: {e}")
        import traceback
        traceback.print_exc()
        return render_template(
            'error.html',
            error_message="An error occurred. Please try again.",
            bot_link=f"https://t.me/{config.USER_BOT_USERNAME}?start=newToken"
        ), 500
    
    if not is_valid:
        if status == "not_found":
            return render_template(
                'error.html',
                error_message="Token invalid or expired or used",
                bot_link=f"https://t.me/{config.USER_BOT_USERNAME}?start=newToken"
            ), 404
        
        elif status == "already_used":
            return render_template(
                'error.html',
                error_message="This token has already been used",
                bot_link=f"https://t.me/{config.USER_BOT_USERNAME}?start=newToken"
            ), 400
        
        elif status in ["bypass_time", "bypass_origin"]:
            if token_data:  # ADD THIS CHECK
                redirect_url = token_validator.get_redirect_url(token_data, config.USER_BOT_USERNAME)
                return redirect(redirect_url)
            else:
                return render_template(
                    'error.html',
                    error_message="Token invalid or expired",
                    bot_link=f"https://t.me/{config.USER_BOT_USERNAME}?start=newToken"
                ), 400
    if not token_data:  # ADD THIS CHECK
        return render_template(
            'error.html',
            error_message="Token invalid or expired",
            bot_link=f"https://t.me/{config.USER_BOT_USERNAME}?start=newToken"
        ), 400
    
    redirect_url = token_validator.get_redirect_url(token_data, config.USER_BOT_USERNAME)
    
    return render_template(
        'redirect.html',
        redirect_url=redirect_url
    )

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "ok"}, 200

@app.errorhandler(404)
def not_found(error):
    return render_template(
        'error.html',
        error_message="Page not found",
        bot_link=f"https://t.me/{config.USER_BOT_USERNAME}"
    ), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template(
        'error.html',
        error_message="Internal server error. Please try again later.",
        bot_link=f"https://t.me/{config.USER_BOT_USERNAME}"
    ), 500

if __name__ == '__main__':
    print(f"🚀 Starting Bypass Detection Server...")
    print(f"📍 Host: {config.SERVER_HOST}")
    print(f"🔌 Port: {config.SERVER_PORT}")
    
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=False,
        threaded=True
    )
