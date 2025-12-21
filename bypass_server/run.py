#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bypass_server.app import app
from shared.config import config

if __name__ == '__main__':
    print(f"🚀 Starting Bypass Detection Server...")
    print(f"📍 Host: {config.SERVER_HOST}")
    print(f"🔌 Port: {config.SERVER_PORT}")
    
    # Check if SSL certificates exist
    ssl_cert = 'ssl/cert.pem'
    ssl_key = 'ssl/key.pem'
    
    if os.path.exists(ssl_cert) and os.path.exists(ssl_key):
        print(f"🔒 HTTPS Mode: ENABLED")
        print(f"🌐 URL: https://{config.SERVER_HOST}:{config.SERVER_PORT}")
        print(f"✅ Health Check: https://{config.SERVER_HOST}:{config.SERVER_PORT}/health")
        
        # Run with SSL
        app.run(
            host=config.SERVER_HOST,
            port=config.SERVER_PORT,
            debug=False,
            threaded=True,
            ssl_context=(ssl_cert, ssl_key)
        )
    else:
        print(f"⚠️  HTTPS Mode: DISABLED (certificates not found)")
        print(f"🌐 URL: http://{config.SERVER_HOST}:{config.SERVER_PORT}")
        print(f"💡 Generate certificates: ./generate_ssl_cert.sh")
        
        # Run without SSL
        app.run(
            host=config.SERVER_HOST,
            port=config.SERVER_PORT,
            debug=False,
            threaded=True
        )