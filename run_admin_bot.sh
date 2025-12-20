#!/bin/bash

echo "🤖 Starting Admin Bot..."
echo ""

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ .env file not found"
    exit 1
fi

source venv/bin/activate
python3 admin_bot/main.py
