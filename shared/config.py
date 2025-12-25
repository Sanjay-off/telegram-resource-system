import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
    ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
    
    USER_BOT_TOKEN = os.getenv("USER_BOT_TOKEN")
    USER_BOT_USERNAME = os.getenv("USER_BOT_USERNAME")
    
    STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID", "0"))
    PUBLIC_CHANNEL_USERNAME = os.getenv("PUBLIC_CHANNEL_USERNAME")
    
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("DB_NAME", "telegram_resource_system")
    COVER_PHOTO = os.getenv("COVER_PHOTO", "AgACAgUAAxkBAAIG0mlLncS1vcxKAgJDX3bgqXfR51xCAALOC2sbv5NYVrk-ViWJxqBrAQADAgADeQADNgQ")
    SERVER_HOST = os.getenv("SERVER_HOST", "152.42.212.81")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "5000"))
    SERVER_SECRET_KEY = os.getenv("SERVER_SECRET_KEY", "default_secret_key")
    
    NOT_AUTHORIZED_EFFECT = os.getenv("NOT_AUTHORIZED_EFFECT", "5046589136895476101")
    FIRE_EFFECT = os.getenv("FIRE_EFFECT", "5104841245755180586")
    
    @staticmethod
    def get_url_shorteners():
        shorteners = {}
        env_vars = os.environ
        
        for key in env_vars:
            if key.endswith("_API_TOKEN"):
                name = key.replace("_API_TOKEN", "")
                base_url_key = f"{name}_BASE_URL"
                
                if base_url_key in env_vars:
                    shorteners[name.lower()] = {
                        "api_token": env_vars[key],
                        "base_url": env_vars[base_url_key]
                    }
        
        return shorteners

config = Config()
