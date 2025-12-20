#!/bin/bash

echo "======================================"
echo "Telegram Resource Distribution System"
echo "======================================"
echo ""

check_python() {
    if ! command -v python3.10 &> /dev/null; then
        echo "❌ Python 3.10 not found. Please install Python 3.10.11"
        exit 1
    fi
    echo "✅ Python 3.10 found"
}

check_mongodb() {
    if ! pgrep -x "mongod" > /dev/null; then
        echo "⚠️  MongoDB is not running. Starting MongoDB..."
        sudo systemctl start mongodb
        sleep 2
    fi
    echo "✅ MongoDB is running"
}

check_dependencies() {
    if [ ! -d "venv" ]; then
        echo "⚠️  Virtual environment not found. Please run setup.sh first"
        exit 1
    fi
    echo "✅ Virtual environment found"
}

check_env() {
    if [ ! -f ".env" ]; then
        echo "❌ .env file not found. Please create .env from .env.example"
        exit 1
    fi
    echo "✅ .env file found"
}

start_admin_bot() {
    echo ""
    echo "🤖 Starting Admin Bot..."
    source venv/bin/activate
    python3 admin_bot/main.py &
    ADMIN_PID=$!
    echo "✅ Admin Bot started (PID: $ADMIN_PID)"
}

start_user_bot() {
    echo ""
    echo "👥 Starting User Bot..."
    source venv/bin/activate
    python3 user_bot/main.py &
    USER_PID=$!
    echo "✅ User Bot started (PID: $USER_PID)"
}

start_bypass_server() {
    echo ""
    echo "🔒 Starting Bypass Detection Server..."
    source venv/bin/activate
    python3 bypass_server/run.py &
    SERVER_PID=$!
    echo "✅ Bypass Server started (PID: $SERVER_PID)"
}

cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    
    if [ ! -z "$ADMIN_PID" ]; then
        kill $ADMIN_PID 2>/dev/null
        echo "✅ Admin Bot stopped"
    fi
    
    if [ ! -z "$USER_PID" ]; then
        kill $USER_PID 2>/dev/null
        echo "✅ User Bot stopped"
    fi
    
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null
        echo "✅ Bypass Server stopped"
    fi
    
    echo ""
    echo "👋 All services stopped. Goodbye!"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "🔍 Checking prerequisites..."
check_python
check_mongodb
check_dependencies
check_env

echo ""
echo "🚀 Starting all services..."
echo ""

start_admin_bot
sleep 2

start_user_bot
sleep 2

start_bypass_server
sleep 2

echo ""
echo "======================================"
echo "✅ All services started successfully!"
echo "======================================"
echo ""
echo "📊 Service Status:"
echo "  - Admin Bot: Running (PID: $ADMIN_PID)"
echo "  - User Bot: Running (PID: $USER_PID)"
echo "  - Bypass Server: Running (PID: $SERVER_PID)"
echo ""
echo "💡 Press Ctrl+C to stop all services"
echo ""

wait
