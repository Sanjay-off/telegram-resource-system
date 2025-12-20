#!/bin/bash

echo "======================================"
echo "System Setup Script"
echo "======================================"
echo ""

check_python() {
    if ! command -v python3.10 &> /dev/null; then
        echo "❌ Python 3.10 not found"
        echo "Please install Python 3.10.11:"
        echo "  sudo apt update"
        echo "  sudo apt install python3.10 python3.10-venv python3.10-dev"
        exit 1
    fi
    echo "✅ Python 3.10 found: $(python3.10 --version)"
}

check_mongodb() {
    if ! command -v mongod &> /dev/null; then
        echo "⚠️  MongoDB not found"
        echo "Installing MongoDB..."
        sudo apt update
        sudo apt install -y mongodb
        sudo systemctl start mongodb
        sudo systemctl enable mongodb
    else
        echo "✅ MongoDB found"
    fi
}

create_venv() {
    if [ -d "venv" ]; then
        echo "⚠️  Virtual environment already exists"
        read -p "Do you want to recreate it? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv
        else
            echo "✅ Using existing virtual environment"
            return
        fi
    fi
    
    echo "📦 Creating virtual environment..."
    python3.10 -m venv venv
    echo "✅ Virtual environment created"
}

install_dependencies() {
    echo ""
    echo "📥 Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
}

setup_env() {
    if [ ! -f ".env" ]; then
        echo ""
        echo "📝 Creating .env file..."
        cp .env.example .env
        echo "✅ .env file created from .env.example"
        echo ""
        echo "⚠️  IMPORTANT: Please edit .env file with your configuration:"
        echo "  - Add your bot tokens"
        echo "  - Add admin user IDs"
        echo "  - Add channel IDs"
        echo "  - Add URL shortener API tokens"
        echo ""
        echo "Run: nano .env"
    else
        echo "✅ .env file already exists"
    fi
}

setup_mongodb_indexes() {
    echo ""
    echo "🗄️  Setting up MongoDB indexes..."
    source venv/bin/activate
    python3 << 'EOF'
from database.connection import db
from pymongo import ASCENDING, DESCENDING

db.connect_sync()

files = db.get_sync_collection('files')
files.create_index([('unique_id', ASCENDING)], unique=True)
files.create_index([('post_no', ASCENDING)], unique=True)

users = db.get_sync_collection('users')
users.create_index([('user_id', ASCENDING)], unique=True)

tokens = db.get_sync_collection('tokens')
tokens.create_index([('token', ASCENDING)], unique=True)
tokens.create_index([('created_by', ASCENDING)])
tokens.create_index([('expires_at', ASCENDING)])

pending_deletions = db.get_sync_collection('pending_deletions')
pending_deletions.create_index([('delete_at', ASCENDING)])

broadcasts = db.get_sync_collection('broadcasts')
broadcasts.create_index([('delete_at', ASCENDING)])

token_generator_count = db.get_sync_collection('token_generator_count')
token_generator_count.create_index([('user_id', ASCENDING), ('date', ASCENDING)])

print("✅ MongoDB indexes created")
db.close_sync()
EOF
}

make_scripts_executable() {
    echo ""
    echo "🔧 Making scripts executable..."
    chmod +x run.sh
    chmod +x setup.sh
    chmod +x admin_bot/main.py
    chmod +x user_bot/main.py
    chmod +x bypass_server/run.py
    chmod +x schedulers/test_schedulers.py
    echo "✅ Scripts are now executable"
}

echo "🔍 Checking system requirements..."
check_python
check_mongodb

create_venv
install_dependencies
setup_env
setup_mongodb_indexes
make_scripts_executable

echo ""
echo "======================================"
echo "✅ Setup completed successfully!"
echo "======================================"
echo ""
echo "📝 Next steps:"
echo "  1. Edit .env file with your configuration"
echo "     nano .env"
echo ""
echo "  2. Start the system:"
echo "     ./run.sh"
echo ""
echo "  3. Or start components individually:"
echo "     python3 admin_bot/main.py"
echo "     python3 user_bot/main.py"
echo "     python3 bypass_server/run.py"
echo ""
