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
    print(f"🌐 URL: http://{config.SERVER_HOST}:{config.SERVER_PORT}")
    print(f"✅ Health Check: http://{config.SERVER_HOST}:{config.SERVER_PORT}/health")
    
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=False,
        threaded=True
    )
